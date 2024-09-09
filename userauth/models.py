from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class User(AbstractUser):
    username = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=400, unique=True,null=False)
    password = models.CharField(max_length=100,null=False, blank=False)
    date_joined = models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
