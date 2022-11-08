from dataclasses import field
from django.forms import ModelForm

from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from .models import User,Posts

from django.forms import ModelForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['name','username','email','password1','password2']



class PostForm(ModelForm):
    class Meta:
        model=Posts
        fields='__all__'
        exclude=[

            'posted',
            'edited',
            'userId',
        ]      