from django.contrib import admin
from django.urls import path
from django.contrib.auth import get_user_model
from . import views 



urlpatterns=[



  path('login',views.loginUser,name="login"),
  path('register',views.registerUser,name="register"),
  path('logout',views.logoutUser,name="logout"),
  path('activate/<uidb64>/<token>/',views.actiavte,name='activate'),
  path('password_reset/',views.password_reset_request,name="password_reset"),

  path('password_reset_confirm/<token>/',views.password_reset_confirm,name="password_reset_confirm"),

]