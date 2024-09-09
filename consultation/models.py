from django.db import models
from django.conf import settings



class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reference = models.CharField(max_length=255, unique=True)  # Unique reference from Paystack
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Amount in local currency (e.g., Naira)
    currency = models.CharField(max_length=10, default='GHC')  # Currency (default to Ghanainan Cedis)
    description = models.TextField(blank=True, null=True)  # Optional description of the payment
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')  # Status of the payment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when payment was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when payment was last updated

    def __str__(self):
        return f"{self.reference} - {self.amount} {self.currency} ({self.status})"
