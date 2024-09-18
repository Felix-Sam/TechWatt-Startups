from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    username = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=400, unique=True,null=False)
    password = models.CharField(max_length=100,null=False, blank=False)
    date_joined = models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserFeedback(models.Model):
    name = models.CharField(max_length=100,blank=False,null=True)
    occupation = models.CharField(max_length=100, null=False, blank=False)
    social_url = models.URLField(null=False, blank=False)
    heading = models.CharField(max_length=200)
    content = models.TextField(null=False, blank=False)
    image = CloudinaryField('profile_image', blank=False, null=False)

    def __str__(self):
        return self.occupation