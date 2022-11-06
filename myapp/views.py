from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from .forms import MyUserCreationForm,PostForm
from django.contrib import messages
from .models import Posts,Like,comment
# Create your views here.


def home(request):
    
    if request.user.is_authenticated:
        posts=Posts.objects.all()
        context={'posts':posts}
        return render(request,'home.html',context)
    else :
        context={'page':login}
        return render(request,'accounts/Login_SignUp.html',context)




def createPost(request):
    form=PostForm();
    if request.method=='POST':

        form =PostForm(request.POST)
        if form.is_valid():
            form.save();
            return redirect('home')
        messages.error('atleast Fill the mandatory Fields')
    context= {'form':form}
    return render(request,'Post.html',context)       