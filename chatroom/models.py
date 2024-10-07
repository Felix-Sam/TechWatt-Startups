from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
# Create your models here.


class ChatFormData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=500,blank=False,null=False)
    image = CloudinaryField('profile_image', blank=False, null=False)
    
    def __str__ (self):
        return self.name

class Message(models.Model):
    user_data = models.ForeignKey(ChatFormData, on_delete=models.CASCADE)
    message = models.TextField()
    # file = CloudinaryField('chat_files/', blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    def __str__ (self):
        return self.message[:50]
