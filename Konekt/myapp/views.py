from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from .forms import MyUserCreationForm
from django.contrib import messages
# Create your views here.


def home(request):
    
    if request.user.is_authenticated:
        return render(request,'home.html')
    else :
        context={'page':login}
        return render(request,'accounts/Login_SignUp.html',context)



