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
    start_time = models.DateTimeField(null = False , blank = False)
    end_time = models.DateTimeField(null = False , blank = False)
    note = models.TextField(null = True,blank = True)
    status = models.IntegerField(default = 1)

class Reviews(models.Model):
    review = models.TextField(null = False,blank = False)
    createdby = models.ForeignKey(User , on_delete = models.CASCADE,null=False,blank=False)
    createdtme = models.DateTimeField(auto_now_add=True,null=False,blank=False)
    task = models.ForeignKey(Tasks , on_delete = models.CASCADE,null=False,blank=False)