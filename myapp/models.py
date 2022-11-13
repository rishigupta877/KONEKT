
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manage import UserManager
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=45,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(unique=True)
    bio=models.TextField(null=True,blank=True)
    #avatar=models.ImageField()
    
    USERNAME_FIELD='email'
    object = UserManager()
    REQUIRED_FIELDS=[]
   

    def __str__(self):
        return str(self.email)
    

class Userfriends(models.Model):
    followers=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followes')
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')



class Posts(models.Model):
   posted=models.DateTimeField(editable=False)
   edited=models.DateTimeField()
   tags=models.TextField(null=True,blank=True)
   userId=models.ForeignKey(User,on_delete=models.CASCADE)
   img=models.ImageField(upload_to='images',null=True,blank=True)
   content=models.TextField(null=True,blank=True)
   likecount=models.IntegerField(default=0)
   dislikecount=models.IntegerField(default=0)
   def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.posted = timezone.now()
        self.edited = timezone.now()
        return super(Posts, self).save(*args, **kwargs)
   


class Like(models.Model):
    postId=models.ForeignKey(Posts,on_delete=models.CASCADE,null=True)
    userId=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
   



class Dislike(models.Model):
    postId=models.ForeignKey(Posts,on_delete=models.CASCADE,null=True)
    userId=models.ForeignKey(User,on_delete=models.CASCADE,null=True)





class comment(models.Model):

     comment_date=models.DateTimeField(auto_now=True);
     comment_edited=models.DateTimeField(auto_now_add=True)
     postId=models.ForeignKey(Posts,on_delete=models.CASCADE)
     userId=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)




class room(models.Model):
   
   useId=models.ManyToManyField(User,related_name="participants",blank=True);
   postid=models.ForeignKey(Posts,on_delete=models.SET_NULL,null=True)

         




