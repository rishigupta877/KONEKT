from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from .forms import MyUserCreationForm
from django.contrib import messages
# Create your views here.


def home(request):

    return render(request,'home.html')




