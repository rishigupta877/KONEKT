from http.client import HTTPResponse
from django.shortcuts import render,redirect

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from  django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from myapp.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from .tokens import account_activation_token
UserModel=get_user_model()
# Create your views here.




def registerUser(request):
    
    
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username,email=email).exists():
                    user=User.objects.get(username__exact=username,email__exact=email)
                    if user.is_active() == False:
                        messages.error(request,'Verify your email')
                    else :
                        return redirect('login')    
            elif User.objects.filter(username=username).exists():
                messages.error(request,'Username Taken')
                
            elif User.objects.filter(email=email).exists():

                
                    messages.error(request,'email taken')     
               
            else :
                user=User.objects.create_user(username=username,password=password1,email=email)
                user.is_active= False
                user.save()
                current_site=get_current_site(request)
                mail_subject='Actiate Your account'
                message= render_to_string('accounts/acc_active_email.html',{

                    'user':user,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })
                
                to_email=email
                email=EmailMessage(mail_subject,message,to=[to_email])
                email.send()
                
                # returning to the home after login
                return HttpResponse('Please confirm your email address to complete registeration')
             
        else :
            messages.error(request,'password not matching')   
        return redirect('home')    
    context={}
    return render(request,'Login_SignUp.html',context)



 
def loginUser(request):

    if request.method =="POST":
       print('hii')
       email=request.POST.get('email')
       password=request.POST.get('password') 
       if User.objects.filter(email=email).exists():    
            user=authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                print('sorryr')
                messages.error(request,'email Or passWord dosenot match')
       else:
            print('lorrry')
            messages.error(request,'user does not exist') 
    context={ 'page' :login}     
    return redirect('home')





def logoutUser(request):  
    
    logout(request)
    return redirect('home')


def actiavte(request,uidb64, token):
    try:
        
        uid=urlsafe_base64_decode(uidb64).decode()
        user=UserModel._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()  
        return HttpResponse('Thank You for your email confirmation Now you can Login')
    else:
        return HttpResponse('Activation Link invalid!')

