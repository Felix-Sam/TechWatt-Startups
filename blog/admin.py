from django.contrib import admin
from .models import BlogPost,BlogImage
# Register your models here.
admin.site.register(BlogPost)
admin.site.register(BlogImage)