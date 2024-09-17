from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=500,null=False,blank=False)
    description = models.TextField(null=False,blank=False)
    price = models.CharField(max_length=200,null=False,blank=False)
    image = CloudinaryField('project_image/', blank=False, null=False)
    project_url = models.URLField(null=False, blank=False)

    def __str__(self):
        return self.title