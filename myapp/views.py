from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from .forms import MyUserCreationForm,PostForm
from django.contrib import messages
from .models import Posts,Like,comment,User,Dislike,Friend_request,Group,joingroup
from django.db.models import Q
import re
from django.urls import reverse
from django.http import HttpResponse
# Create your views here.


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    print(q);
    user=request.user
    if request.user.is_authenticated:
        chunks=q.split()
        print(chunks)

        posts=[];
        if len(chunks)==0:
            posts.extend(Posts.objects.filter( Q(tags__icontains=q),Q(group_id=0)))
        else :    
            for chunk in chunks:
                posts.extend(Posts.objects.filter(Q(tags__icontains=chunk),Q(group_id=0)))
        
        # if len(chunks)==0:
        #     posts=Posts.objects.filter(Q(tags__icontains=q)).order_by('-posted')
           
        # elif len(chunks)==1:
        #     posts=Posts.objects.filter(Q(tags__icontains=chunks[0])).order_by('-posted')

        # elif len(chunks)==2:
        #      posts=Posts.objects.filter(Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])).order_by('-posted')

        # elif len(chunks)==3:
        #     posts=Posts.objects.filter(Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])).order_by('-posted')

        # elif len(chunks)==4:
        #     posts=Posts.objects.filter(Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])|Q(tags__icontains=chunks[3])).order_by('-posted')

        # elif len(chunks)==5:           
        #     posts=Posts.objects.filter(Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])|Q(tags__icontains=chunks[3])|Q(tags__icontains=chunks[4])).order_by('-posted')
        #     post=Posts.objects.filter(Q(tags__icontains=chunk))
        #     for pos in post:
                
        #         posts.append(pos)
        posts.sort(key= lambda x : x.posted )
        posts.reverse()
        posts=[*set(posts)]
        groups=Group.objects.filter(~Q(admin=user),~Q(participants=user))[0:5];
        users=User.objects.all()[0:5];
        print(users)
        context={'posts':posts,'user':user,'groups':groups,'users':users}
        return render(request,'home.html',context)
    else :
        context={'page':login}
        return render(request,'accounts/Login_SignUp.html',context)




def createPost(request):
    
    form=PostForm();
    if request.method=='POST':
        
        image=request.FILES['image'] 
        print(image) 
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
    print(user)
    if request.user.is_authenticated:
        chunks=q.split()
        print(len(chunks))

        posts=[];
        if len(chunks)==0:
            posts.extend(Posts.objects.filter(Q(userId=user) , Q(tags__icontains=q),Q(group_id=0)))
        else :    
            for chunk in chunks:
                posts.extend(Posts.objects.filter(Q(userId=user) , Q(tags__icontains=chunk),Q(group_id=0)))
        
        # if len(chunks)==0:
        #     posts=Posts.objects.filter(Q(userId=user) , (Q(tags__icontains=q))).order_by('-posted')
           
        # elif len(chunks)==1:
        #     posts=Posts.objects.filter(Q(userId=user) , Q(tags__icontains=chunks[0])).order_by('-posted')

        # elif len(chunks)==2:
        #      posts=Posts.objects.filter(Q(userId=user) , (Q(tags__icontains=chunks[0]) | Q(tags__icontains=chunks[1]))).order_by('-posted')

        # elif len(chunks)==3:
        #     posts=Posts.objects.filter(Q(userId=user) ,  (Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2]))).order_by('-posted')

        # elif len(chunks)==4:
        #     posts=Posts.objects.filter(Q(userId=user) , (Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])|Q(tags__icontains=chunks[3]))).order_by('-posted')

        # elif len(chunks)==5:           
        #     posts=Posts.objects.filter(Q(userId=user) ,  (Q(tags__icontains=chunks[0])|Q(tags__icontains=chunks[1])|Q(tags__icontains=chunks[2])|Q(tags__icontains=chunks[3])|Q(tags__icontains=chunks[4]))).order_by('-posted')  
        

        #sorting the posts accorting to the posted time
        posts.sort(key= lambda x : x.posted )
        posts.reverse()
        # to prevent form the duplicate
        posts=[*set(posts)] 
    groups=Group.objects.filter(~Q(admin=user),~Q(participants=user))[0:5];
    users=User.objects.all()[0:5];
    # for post in posts:
    #     print(post.posted )
    followercount=user.followers.count
    followingcount=user.followings.count
    is_follow=None
    if request.user != user:
        is_follow = User.objects.filter(followings__id=user.id)
        print(is_follow)
    
   
    context={'user':user,'posts':posts,'path':request.path,'followercount':followercount,'followingcount':followingcount,'is_follow':is_follow,'groups':groups,'users':users}
    return render(request,'Dashboard.html',context)    



def deletePost(request,pk):
    
    if request.method =="POST":
        print('hii')
        post=Posts.objects.filter(id=pk)
        post.delete();
        return redirect('home')  
     
    return render(request,'delete.html') 


def editPost(request,pk):
    post=Posts.objects.get(id=pk);
    if request.method=='POST':
        post.img=request.FILES['image']
        post.tags=request.POST['tags']
        post.content=request.POST['content']
        post.userId=request.user
        post.save();
        return redirect('home')
    context={'post':post}
    return render(request,'post.html',context)    


def createGroup(request,pk):
    user=User.objects.get(id=pk)
    context={'user':user}
    if request.method =="POST":
        a= Group.objects.create(
        name=request.POST['name'],
        avatar=request.FILES['image'],
        description=request.POST['description'],
        admin=request.user,
        is_public=request.POST.get('is_public',False)
        )
        print(a.is_public)
        return redirect('dashboard',request.user.id)

    return render(request,'create_group.html',context)


def already_liked_post(user,post_id):
    post=Posts.objects.get(id=post_id)
    return Like.objects.filter(userId=user,postId=post).exists()
 
def already_disliked_post(user,post_id):
    post=Posts.objects.get(id=post_id)
    return Dislike.objects.filter(userId=user,postId=post).exists() 

def fun2(request,post_id):
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

def like_clicked(request,post_id,pk):
    

    fun2(request,post_id)
   
    return redirect(reverse('dashboard',args=pk))       


def like_clicked1(request,post_id):
    fun2(request,post_id) 
    print(request.path)
    if request.path == "/like/{post_id}".format(post_id=post_id):
        return redirect('home')  

def fun(request,post_id):
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
    

def dislike_clicked(request,post_id,pk):
    

   fun(request,post_id)
   
   return redirect(reverse('dashboard',args=pk)) 




def dislike_clicked1(request,post_id):
    fun(request,post_id) 
    print(request.path)
    if request.path == "/dislike/{post_id}".format(post_id=post_id):
        return redirect('home')  





def send_friend_request(request,userId):
    from_user=request.user
    to_user=User.object.get(id=userId)
    friend_request,created=Friend_request.objects.get_or_create(
  from_user=from_user,to_user=to_user
    ) 
    if created:
        return HttpResponse('friend request sent')
    else :
        return HttpResponse('friend request was already sent')



def accept_friend_request(request,requestID):
    friend_request =Friend_request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.followers.add(friend_request.from_user)
        friend_request.from_user.followings.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')

    else :

        return HttpResponse('friend request not accepted')   



def Notification(request,userId):
    user=User.objects.get(id=userId)
    print(user)
    requests=Friend_request.objects.filter(to_user=user)
    print(requests)
    
    requestGroups=joingroup.objects.filter(to_group__admin=user)
    context={'requests':requests,'requestGroups':requestGroups}

    return render(request,'Notification.html',context)




def followers(request,userId):
    user=User.objects.get(id=userId)
    followerss=user.followers
    context={'followerss':followerss}
    return render(request,'followers.html',context)




def followings(request,userId):
    user=User.objects.get(id=userId)
    followingss=user.followings
    context={'followingss':followingss}

    return render(request,'followings.html',context)




def unfollow(request,userId):

    user=request.user
    from_user=User.objects.get(id=userId)

    a=user.followings.remove(from_user)

    
    b=from_user.followers.remove(user)
 

    return redirect('home')




def updateUser(request,userId): 
    user=User.objects.get(id=userId)
    if request.method == 'POST':

        user.avatar=request.FILES['image'];
        user.bio=request.POST['bio'];
        user.save();
        return redirect('dashboard',user.id)

    context={'user':user}
    return render(request,'updateUser.html',context) 




def UserGroup(request,pk):
    user=User.objects.get(id=pk)
    print(user)
    groups=[]
    groups.extend(list(Group.objects.filter(admin = user)))
    groups.extend(list(Group.objects.filter(participants = user)))
    print("hii")
    print(groups)
   
    context={'groups':groups}
    return render(request,'Groups.html',context);







def joinGroup(request,pk):
    group= Group.objects.get(id=pk);
    if group.is_public==True:
       group.participants.add(request.user)
    else:
        admin=group.admin;
        user=request.user;
        context={'user':user,'group':group}
        return render(request,'Groupjoin.html',context)
       
    return redirect('home')



def sendjoinrequest(request,pk):
    if request.method=="POST":
        from_user=request.user
        to_group=Group.objects.get(id=pk)
        message=request.POST['reason']
        join_request,created=joingroup.objects.get_or_create(
          from_user=from_user, to_group=to_group,message=message
        )
     
    return redirect('home');
    



def Approvejoining(request,userId,groupid):

    group=Group.objects.get(id=groupid)
    user=User.objects.get(id=userId)
    group.participants.add(user)
    requestgroup=joingroup.objects.filter(from_user=user,to_group=group);
    requestgroup.delete();
    return redirect('home')



def comments(request,postid):
    print("aund")
    post=Posts.objects.get(id=postid)
    if request.method=='POST':
        comment.objects.create(
            userId=request.user,
            postId=post,
            text=request.POST['text']
        )
   
    allcomments=comment.objects.filter(postId=post)
    
    context={'allcomments':allcomments}
    return render(request,'comments.html',context)

def deletecomment(request,commentid):
    a=comment.objects.get(id=commentid)
    if request.method=="POST":
        a.delete();
        return redirect('home')
    return render(request,'delete.html')  





def groupdashboard(request,groupid):

    group=Group.objects.get(id=groupid)
    print(group.admin)
    print(request.user)
    participants=group.participants.all()
    
    context={'group':group,'participants':participants}
    return render(request,'Group_dashboard.html',context)






def createGrouppost(request,groupid,userid):
    group=Group.objects.get(id=groupid)
    context={'group':group}
    if request.method == "POST":
        a=Posts.objects.create(
          
        img=request.FILES["image"],
         
        tags=request.POST['tags'],
        content=request.POST['content'],
        userId=request.user,
        group_id=groupid
            
        )
        group.postId.add(a)
        
        
        
        return redirect('groupdashboard',group.id)
   
    return render(request,'post.html',context)   






def allgroups(request):
    groups = Group.objects.filter(~Q(admin=request.user),~Q(participants=request.user));
   
    context={'groups': groups}
    return render(request,'allgroup.html',context) 


def deleteGroup(request,groupid):
    group=Group.objects.filter(id=groupid)
    if request.method =="POST":
        
       
        group.delete();
        return redirect('home')  
    context={'group':group} 
    return render(request,'delete.html',context)   



def leaveGroup(request,groupid):
    group=Group.objects.get(id=groupid)
    if request.method =="POST":
        
       user=group.participants.get(id=request.user.id)
       group.participants.remove(user); 
       return redirect('home')  
    context={'group':group} 
    return render(request,'delete.html',context)       

    






