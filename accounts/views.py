from http.client import HTTPResponse
from django.shortcuts import render,redirect
from .models import Profile
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

from .helpers import send_forget_password_mail
UserModel=get_user_model()
# Create your views here.

from django.core.mail import send_mail,BadHeaderError

from django.http import  HttpResponse
# important
from django.contrib.auth.forms import PasswordResetForm 
from django.db.models.query_utils import Q

def registerUser(request):
    
    
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        bio=request.POST['bio']
        if password1 == password2:
            if User.objects.filter(username=username,email=email).exists():
                    user=User.objects.get(username=username,email=email)
                    print(user.is_active)
                    if user.is_active:
                        messages.error(request,'your account is active you can login now')
                    else :    
                        messages.error(request,'Verify your email')
                    return redirect('home')    
                    
                       
            elif User.objects.filter(username=username).exists():
                messages.error(request,'Username Taken')
                return redirect('home')
                
            elif User.objects.filter(email=email).exists():

                
                    messages.error(request,'email taken') 
                    return redirect('home')    
               
            else :
                user=User.objects.create_user(username=username,password=password1,email=email,bio=bio)
                user.is_active= False
                user.save()
                current_site=get_current_site(request)
                print(current_site.domain)
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
                profile_obj = Profile.objects.create(user = user )
                profile_obj.save()
                
                # returning to the home after login
                messages.success(request,'Email sent ,verify ')
                return redirect('home')
             
        else :
            messages.error(request,'password not matching')   
            return redirect('home')
    context={}
    return render(request,'login.html',context)

def password_reset_confirm(request , token):
    context = {}
    # print(request)
    # print("cbkdscbdscbjldsfbcjls")
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()

        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.error(request, 'No user id found.')
                return render(request , 'password_reset_confirm.html' , context)
                
            
            if  new_password != confirm_password:
                messages.error(request, 'both should  be equal.')
                return render(request , 'password_reset_confirm.html' , context)
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            profile_obj.forget_password_token = 0
            profile_obj.save()
            messages.success(request,'Password changed')
            return redirect('home')
            
            
            
        
        
    except Exception as e:
        print(e)
        messages.error(request,'acitvation Link invalid send email again')
        logout(request)
        return redirect('home')
    return render(request , 'password_reset_confirm.html' , context)



import uuid
def password_reset_request(request):
    try:
     if request.method=="POST":
            email= request.POST['email']
        
            
           
        
            user_email=User.object.filter(Q(email=email))
            print(user_email)
            if user_email.exists():
               for user in user_email:
                    print(user)
                    token= str(uuid.uuid4())
                    profile_obj= Profile.objects.get(user = user)
                    print(profile_obj)
                    if profile_obj is not None:
                        profile_obj.forget_password_token = token
                        profile_obj.save()
                        send_forget_password_mail(user,token)
                        messages.success(request, 'An email is sent.')
                        return redirect('home')
                        
                    else :
                        messages.error(request, 'No register user with this email id.')
                        return redirect('passsword_reset')      

                    
                    
                 
                   
            else:  
                messages.error(request, 'Not user found with this Email.')
                return redirect('password_reset')     
                     
    except Exception as e:
        print(e)
    return render(request,'password_reset.html')
 
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
                print('sorry')
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
    print(request)
    print("vshjdvhjsh")
    try:
        
        uid=urlsafe_base64_decode(uidb64).decode()
        user=UserModel._default_manager.get(pk=uid)
        print(user)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()  
        messages.success(request,'Email Verified ! Login Now')
        return redirect('login')
    else:
        messages.error(request,'Activation Link invalid!')
        return redirect('login')





