from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
# Register your models here




admin.site.register(models.User)
admin.site.register(models.comment)
admin.site.register(models.Dislike)
admin.site.register(models.Like)
admin.site.register(models.Posts)
admin.site.register(models.room)
admin.site.register(models.Friend_request)
admin.site.register(models.Group)
admin.site.register(models.joingroup)
