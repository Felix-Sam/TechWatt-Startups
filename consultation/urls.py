from django.urls import path
from . import views

urlpatterns = [
    path('consultation/' ,views.consultation,name='consultation'),
    path('payment/' ,views.initialize_payment,name='initialize_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('paymentsucess/',views.paymentsucessful,name='paymentsucess'),
    path('paymentunsucess/',views.paymentunsucessful,name='paymentunsucess'),
]