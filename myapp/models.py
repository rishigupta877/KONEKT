
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manage import UserManager
# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=45,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True)
    bio=models.TextField(null=True)
    #avatar=models.ImageField()
   
    USERNAME_FIELD='email'
    object = UserManager()
    REQUIRED_FIELDS=[]
   

    def __str__(self):
        return str(self.email)
    




class Posts(models.Model):
   posted=models.DateTimeField(auto_now=True)
   edited=models.DateTimeField(auto_now_add=True)
   tags=models.TextField(null=True,blank=True)
   userId=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

   


class Like(models.Model):
    postId=models.ForeignKey(Posts,on_delete=models.SET_NULL,null=True)
    userId=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)



class comment(models.Model):

     comment_date=models.DateTimeField(auto_now=True);
     comment_edited=models.DateTimeField(auto_now_add=True)
     postId=models.ForeignKey(Posts,on_delete=models.SET_NULL,null=True)
     userId=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)




class room(models.Model):
   
   useId=models.ManyToManyField(User,related_name="participants",blank=True);
   postid=models.ForeignKey(Posts,on_delete=models.SET_NULL,null=True)

         



