from http.client import HTTPResponse
from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm
from  django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from myapp.models import User

# Create your views here.




def registerUser(request):
    
    
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username Taken')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'email taken')  
            else :
                user=User.objects.create_user(username=username,password=password1,email=email)
                user.save();
                
                # returning to the home after login
                return redirect('home')
             
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
