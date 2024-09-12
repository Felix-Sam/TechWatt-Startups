from django.urls import path
from . import views

urlpatterns = [
    path('consultation/' ,views.consultation,name='consultation'),
    path('consultation/callback/', views.consultation_callback, name='consultation_callback'),
    
    path('payment/' ,views.Payments,name='payments'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),

    path('paymentsucess/',views.paymentsucessful,name='paymentsucess'),
    path('paymentunsucess/',views.paymentunsucessful,name='paymentunsucess'),
    
]