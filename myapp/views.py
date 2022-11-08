from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from .forms import MyUserCreationForm,PostForm
from django.contrib import messages
from .models import Posts,Like,comment,User
from django.db.models import Q
import re
# Create your views here.


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''

    if request.user.is_authenticated:
        chunks=re.split('[+]',q)
        print(chunks[0])
        # posts=[Posts]
        # for chunk in chunks:
        #     post=Posts.objects.filter(Q(tags__icontains=chunk))
        #     for pos in post:
                
        #         posts.append(pos)
   
        posts=Posts.objects.filter(Q(tags__icontains=q))
        
        context={'posts':posts}
        return render(request,'home.html',context)
    else :
        context={'page':login}
        return render(request,'accounts/Login_SignUp.html',context)




def createPost(request):
    
    form=PostForm();
    if request.method=='POST':
       
        form =PostForm(request.POST,request.FILES)
        if form.is_valid():
            
            post=form.save(commit=False)
            post.userId=request.user;
            # user.id=pk;
            post.save();

            
            
            return redirect('home')
        messages.error('atleast Fill the mandatory Fields')
    context= {'form':form}
    return render(request,'Post.html',context)       



def dashboard(request,pk):
    user=User.objects.get(id=pk)
    #print(user.id);
    print(request.user.id)
    posts=Posts.objects.filter(userId=user.id)
    
    
    context={'user':user,'posts':posts}
    return render(request,'Dashboard.html',context)    



def deletePost(request,pk):
    
    if request.method =="POST":
        print('hii')
        post=Posts.objects.filter(id=pk)
        post.delete();
        return redirect('home')  
     
    return render(request,'delete.html') 