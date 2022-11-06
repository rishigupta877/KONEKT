from dataclasses import field
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from .models import User,Posts




class MyUserCreationForm(UserCreationForm):
    class meta:
        model=User
        fields=['name','username','email','password1','password2']



class PostForm(ModelForm):
    class meta:
        model=Posts
        fields='__all__'
        exclude=[

            'posted',
            'edited',
            'userId',
        ]      