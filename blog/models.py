from django.db import models
from userauth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=400, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)  # Link to the BlogPost
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional image caption

    def __str__(self):
        return f"Image for {self.blog_post.title}"
