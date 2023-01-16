
from django.contrib import admin
from django.urls import path
from . import views 


urlpatterns=[



    path('',views.home,name="home"),
    path('dashboard/<str:pk>/' ,views.dashboard,name="dashboard"),
    path('createpost',views.createPost,name="createpost"),
    path('delete_post/<str:pk>/',views.deletePost,name="delete"),
    path('editpost/<str:pk>/',views.editPost,name="editpost"),
    path('creategroup/<str:pk>/',views.createGroup,name="creategroup"),

    path('like/<str:post_id>',views.like_clicked1,name="like_clicked"),
    
    path('dashboard/<str:pk>/like/<str:post_id>/',views.like_clicked,name='like_clicked2'),
    
    path('dislike/<str:post_id>',views.dislike_clicked1,name="dislike_clicked"),
    
    path('dashboard/<str:pk>/dislike/<str:post_id>/',views.dislike_clicked,name='dislike_clicked2'),
    path('Notification/<str:userId>/',views.Notification,name='Notification'),
    path('send_friend_request/<str:userId>/',views.send_friend_request,name='send_request'),
    path('accept_friend_request/<str:requestID>/',views.accept_friend_request,name='accept_request'),
    path('followers/<str:userId>/',views.followers,name='followers'),
    path('following/<str:userId>/',views.followings,name='following'),
    path('unfollow/<str:userId>/',views.unfollow,name='unfollow'),
    path('updateUser/<str:userId>/',views.updateUser,name='updateuser'),
    path('groups/<str:pk>/',views.UserGroup,name='UserGroup'),
    path('joinGroup/<str:pk>/',views.joinGroup,name="joinGroup"),
    path('sendjoinrequest/<str:pk>/',views.sendjoinrequest,name="sendjoinrequest"),
    path('Approvejoining/<str:userId>/<str:groupid>/',views.Approvejoining,name="Approvejoining"),
    path('comment/<str:postid>/',views.comments,name="comment"),
    path('delete_comment/<str:commentid>/',views.deletecomment,name="deletecomment"),


    path('groupdashboard/<str:groupid>/',views.groupdashboard,name="groupdashboard"),
    path('grouppost/<str:groupid>/<str:userid>/',views.createGrouppost,name="grouppost"),
    path('Allgroups',views.allgroups,name="Allgroups"),
    path('deletegroup/<str:groupid>',views.deleteGroup,name="deletegroup"),
    
        path('leavegroup/<str:groupid>',views.leaveGroup,name="leavegroup")

]