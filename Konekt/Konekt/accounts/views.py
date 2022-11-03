from http.client import HTTPResponse
from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm
from  django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib import messages
# Create your views here.




def registerUser(request):
    
   
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save();
            print(user)
            login(request,user)
            return redirect('home');
        else:
            messages.error(request,'An error occured during registration')
    form=UserCreationForm();
    context={'form':form}
    return render(request,'SignUp.html',context)



 
def loginUser(request):
    return render(request,'Login.html')