from dataclasses import field
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from .models import User




class MyUserCreationForm(UserCreationForm):
    class meta:
        model=User
        fields=['name','username','email','password1','password2']