import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


from . import choices
# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'SA')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    user_type = models.CharField(max_length=4,choices=choices.User_type,null = False,blank = False)
    objects = UserManager()



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