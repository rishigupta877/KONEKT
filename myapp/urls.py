
from django.contrib import admin
from django.urls import path
from . import views 


urlpatterns=[



    path('',views.home,name="home"),
    path('dashboard/<str:pk>/' ,views.dashboard,name="dashboard"),
    path('createpost',views.createPost,name="createpost"),
    path('delete_post/<str:pk>/',views.deletePost,name="delete"),
    path('creategroup',views.createGroup,name="creategroup"),

    path('like/<str:post_id>',views.like_clicked,name="like_clicked"),
    
    path('dashboard/<str:pk>/like/<str:post_id>/',views.like_clicked,name='like_clicked2'),



]