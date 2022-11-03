from django.contrib import admin
from . import models
# Register your models here.


# admin.site.register(models.User)
admin.site.register(models.comment)
admin.site.register(models.Friends)
admin.site.register(models.Like)
admin.site.register(models.Posts)
admin.site.register(models.room)