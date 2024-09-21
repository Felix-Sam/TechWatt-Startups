from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.CharField(max_length=12, null=False, blank=False)
    image = CloudinaryField('project_image/', blank=False, null=False)
    project_url = models.URLField(null=False, blank=False)
    project_zip = models.FileField(upload_to='project_zips/', blank=False, null=False) 

    def __str__(self):
        return self.title
    

class ProjectPayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')  # Linking payment to project
    reference = models.CharField(max_length=255, unique=True)  # Unique reference from Paystack
    currency = models.CharField(max_length=10, default='GHC')  # Currency (default to Ghanaian Cedis)
    amount = models.CharField(max_length=12,null=False, blank=False)  # Price for the project
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when payment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when payment was last updated

    def __str__(self):
        return f"{self.reference} - {self.amount} {self.currency} ({self.status})"
