from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from .forms import MyUserCreationForm,PostForm
from django.contrib import messages
from .models import Posts,Like,comment,User,Dislike
from django.db.models import Q
import re
from django.urls import reverse
# Create your views here.


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    print(q);
    
    if request.user.is_authenticated:
        chunks=q.split()
        print(chunks)
        
        if len(chunks)==0:
            posts=Posts.objects.filter(Q(tags__icontains=q)).order_by('-posted')
           
        elif len(chunks)==1:
            posts=Posts.objects.filter(Q(tags__icontains=chunks[0])).order_by('-posted')

        elif len(chunks)==2:
             posts=Posts.objects.filter(Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])).order_by('-posted')

        elif len(chunks)==3:
            posts=Posts.objects.filter(Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])).order_by('-posted')

        elif len(chunks)==4:
            posts=Posts.objects.filter(Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])|Q(tags__icontains=chunks[3])).order_by('-posted')

        elif len(chunks)==5:           
            posts=Posts.objects.filter(Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])|Q(tags__icontains=chunks[3])|Q(tags__icontains=chunks[4])).order_by('-posted')
        #     post=Posts.objects.filter(Q(tags__icontains=chunk))
        #     for pos in post:
                
        #         posts.append(pos)
   
      
        
        context={'posts':posts}
        return render(request,'home.html',context)
    else :
        context={'page':login}
        return render(request,'accounts/Login_SignUp.html',context)




def createPost(request):
    
    form=PostForm();
    if request.method=='POST':
        
           
        Posts.objects.create(
          
        img=request.FILES["image"],
         
        tags=request.POST['tags'],
        content=request.POST['content'],
        userId=request.user,
            
        )
        

      
            
      

            
            
        return redirect('home')
        messages.error(request,'atleast Fill the mandatory Fields')
    context= {'form':form}
    return render(request,'Post.html',context)       



def dashboard(request,pk):


    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    print(q);
    user=User.objects.get(id=pk)
    if request.user.is_authenticated:
        chunks=q.split()
        print(len(chunks))
        posts=Posts.objects.all()
        if len(chunks)==0:
            posts=Posts.objects.filter(userId=user.id and (Q(tags__icontains=q))).order_by('-posted')
           
        elif len(chunks)==1:
            posts=Posts.objects.filter(userId=user.id and Q(tags__icontains=chunks[0])).order_by('-posted')

        elif len(chunks)==2:
             posts=Posts.objects.filter(userId=user.id and (Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1]))).order_by('-posted')

        elif len(chunks)==3:
            posts=Posts.objects.filter(userId=user.id and (Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2]))).order_by('-posted')

        elif len(chunks)==4:
            posts=Posts.objects.filter(userId=user.id and (Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])|Q(tags__icontains=chunks[3]))).order_by('-posted')

        elif len(chunks)==5:           
            posts=Posts.objects.filter(userId=user.id and (Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])|Q(tags__icontains=chunks[3])|Q(tags__icontains=chunks[4]))).order_by('-posted')  


    
    #print(user.id);
   
    
    
    context={'user':user,'posts':posts,'path':request.path}
    return render(request,'Dashboard.html',context)    



def deletePost(request,pk):
    
    if request.method =="POST":
        print('hii')
        post=Posts.objects.filter(id=pk)
        post.delete();
        return redirect('home')  
     
    return render(request,'delete.html') 




def createGroup(request):

    return render(request,'create_group.html')


def already_liked_post(user,post_id):
    post=Posts.objects.get(id=post_id)
    return Like.objects.filter(userId=user,postId=post).exists()
 
def already_disliked_post(user,post_id):
    post=Posts.objects.get(id=post_id)
    return Dislike.objects.filter(userId=user,postId=post).exists() 

def like_clicked(request,post_id,pk):
    post = Posts.objects.get(id=post_id)
    currliked=post.likecount
    print(request.user)
    if not already_liked_post(request.user,post_id):
        Like.objects.create(userId=request.user,postId=post)
        currliked=currliked+1

    else:
        
        Like.objects.filter(userId=request.user,postId=post).delete(); 
        currliked=currliked-1;
  
    post.likecount=currliked
 
    
    post.save()  

    user=post.userId.id
   
    return redirect(reverse('dashboard',args=pk))       


def like_clicked1(request,post_id):
    post = Posts.objects.get(id=post_id)
    currliked=post.likecount
    if not already_liked_post(request.user,post_id):
        Like.objects.create(userId=request.user,postId=post)
        currliked=currliked+1

    else:
        Like.objects.filter(userId=request.user,postId=post).delete(); 
        currliked=currliked-1;
    post.likecount=currliked
   
   
    post.save()  
    print(request.path)
    if request.path == "/like/{post_id}".format(post_id=post_id):
        return redirect('home')  



def dislike_clicked(request,post_id,pk):
    post = Posts.objects.get(id=post_id)
    currdisliked=post.dislikecount
    print(request.user)
    if not already_disliked_post(request.user,post_id):
        Dislike.objects.create(userId=request.user,postId=post)
        currdisliked=currdisliked+1

    else:
        
            Dislike.objects.filter(userId=request.user,postId=post).delete(); 
            currdisliked=currdisliked-1
  
    post.dislikecount=currdisliked
 
    
    post.save()  

    user=post.userId.id
   
    return redirect(reverse('dashboard',args=pk)) 




def dislike_clicked1(request,post_id):
    post = Posts.objects.get(id=post_id)
    currdisliked=post.dislikecount
    if not already_disliked_post(request.user,post_id):
        Dislike.objects.create(userId=request.user,postId=post)
        currdisliked=currdisliked+1

    else:
        Dislike.objects.filter(userId=request.user,postId=post).delete(); 
        currdisliked=currdisliked-1;
    post.dislikecount=currdisliked
   
   
    post.save()  
    print(request.path)
    if request.path == "/dislike/{post_id}".format(post_id=post_id):
        return redirect('home')  