from contextlib import nullcontext
from unittest import TextTestRunner
from django.db import models
from django.contrib.auth.models import AbstractUser,User
# Create your models here.



# class User(AbstractUser):
#     name=models.CharField(max_length=200,null=True)
#     email=models.EmailField(unique=True)
#     #bio=models.Field(null=True)
#     #avatar=models.ImageField()
#     #friends=models.ManyToManyField(User,related_name="Friends",on_delete=models.SET_NULL)
    
#     # USERNAME_FIELD='email'
#     REQUIRED_FIELDS=[]

#     def __str__(self):
#         return self.email


class Friends(models.Model):
    friends=models.ManyToManyField(User,related_name="friends",blank=True)


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

         



