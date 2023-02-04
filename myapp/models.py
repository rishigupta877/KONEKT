
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manage import UserManager
from django.utils import timezone
from cloudinary.models import CloudinaryField
# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=45,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(unique=True)
    bio=models.TextField(null=True,blank=True)
    avatar=CloudinaryField('images',null=True,default='avatar.svg')
    followers=models.ManyToManyField('self',symmetrical=False,related_name='follower',blank=True)
    followings=models.ManyToManyField('self',symmetrical=False,related_name='following',blank=True)
    USERNAME_FIELD='email'
    object = UserManager()
    REQUIRED_FIELDS=[]
   

    def __str__(self):
        return str(self.email)
    

class Friend_request(models.Model):
    from_user=models.ForeignKey(User,related_name='from_user',on_delete=models.CASCADE)
    to_user=models.ForeignKey(User,related_name='to_user',on_delete=models.CASCADE)


class Posts(models.Model):
   posted=models.DateTimeField(editable=False)
   edited=models.DateTimeField()
   tags=models.TextField(null=True,blank=True)
   userId=models.ForeignKey(User,on_delete=models.CASCADE)
   img=CloudinaryField('images',null=True,blank=True)
   content=models.TextField(null=True,blank=True)
   likecount=models.IntegerField(default=0)
   dislikecount=models.IntegerField(default=0)
   group_id=models.IntegerField(default=0)
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
     text=models.TextField();




class room(models.Model):
   
   useId=models.ManyToManyField(User,related_name="participants",blank=True);
   postid=models.ForeignKey(Posts,on_delete=models.SET_NULL,null=True)

         

class Group(models.Model):
    admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
 
    name=models.CharField(max_length=200)
    avatar=CloudinaryField('images',null=True,blank=True,default='th.jpeg')
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='Participants',symmetrical=False,blank=True)
    postId=models.ManyToManyField(Posts,symmetrical=False ,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    is_public=models.BooleanField(default=False)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return str(self.name)



class joingroup(models.Model):
   message=models.TextField(null=True); 
   from_user=models.ForeignKey(User,on_delete=models.CASCADE)
   to_group=models.ForeignKey(Group,on_delete=models.CASCADE)
    
   








