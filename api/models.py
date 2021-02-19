import json
from django.db import models
from django.contrib.auth.models import AbstractUser


from . import choices
# Create your models here.
class User(AbstractUser):
    user_type = models.CharField(max_length=4,choices=choices.User_type,null = False,blank = False)

class Tasks(models.Model):
    name = models.CharField(max_length = 250 , null = False,blank = False)
    createdby = models.ForeignKey(User , on_delete = models.CASCADE,null=False,blank=False)
    createdtme = models.DateTimeField(auto_now_add=True,null=False,blank=False)
    last_updated = models.DateTimeField(auto_now_add=True,null=False,blank=False)
    start_time = models.DateTimeField(null = True , blank = True)
    end_time = models.DateTimeField(null = True , blank = True)
    note = models.TextField(null = True,blank = True)
    status = models.IntegerField(default = 1)

class TaskAssign(models.Model):
    task = models.ForeignKey(Tasks , on_delete = models.CASCADE,null=False,blank=False)
    assigned_to = models.ForeignKey(User , on_delete = models.CASCADE,null=False,blank=False)

class Reviews(models.Model):
    review = models.TextField(null = False,blank = False)
    createdby = models.ForeignKey(User , on_delete = models.CASCADE,null=False,blank=False)
    createdtme = models.DateTimeField(auto_now_add=True,null=False,blank=False)
    task = models.ForeignKey(Tasks , on_delete = models.CASCADE,null=False,blank=False)

class Notification(models.Model):
    note = models.TextField(null = False,blank = False)
    notification_type = models.IntegerField(null = False,blank = False)
    object_id = models.IntegerField(null = True,blank = True)
    notifi_to = models.CharField(max_length=4,choices=choices.User_type,null = False,blank = False)