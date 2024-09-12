from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)
from .models import Payment , Consultation


@login_required(login_url = 'login')
def consultation(request):
    if request.method == 'POST':
        amount = int(request.POST.get('price'))
        callback_url = request.build_absolute_uri('/consultation/callback/')

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "amount": amount*100,
            'email': request.user.email,
            "callback_url": callback_url
        }

        try:
            response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)
            response_data = response.json()

            if response_data.get('status'):
                Consultation.objects.create(
                    user=request.user,
                    reference=response_data['data']['reference'],
                    amount=amount, 
                    status='pending'
                )
                return redirect(response_data['data']['authorization_url'])
            else:
                logger.error(f"Paystack error: {response_data.get('message')}")
                return redirect(reverse('paymentunsucess'))
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return redirect(reverse('paymentunsucess'))
    return render(request, 'consultation/consult.html')


def consultation_callback(request):
    reference = request.GET.get('reference')

    if not reference:
        return JsonResponse({"message": "Missing reference parameter."})

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
        response_data = response.json()

        if response_data.get('status') and response_data['data'].get('status') == 'success':
            Consultation.objects.filter(reference=reference).update(status='completed')
            return redirect(reverse('paymentsucess'))
        else:
            Consultation.objects.filter(reference=reference).update(status='failed')
            return redirect(reverse('paymentunsucess'))
        
    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return redirect(reverse('paymentunsucess'))





@login_required(login_url = 'login')
def paymentsucessful(request):
    return render(request, 'consultation/paymentsucess.html')


@login_required(login_url = 'login')
def paymentunsucessful(request):
    return render(request, 'consultation/paymentunsucess.html')



@login_required(login_url = 'login')
def Payments(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        amount = int(request.POST.get('amount'))
        name = request.POST.get('name')
        payment_description = request.POST.get('payment-description')
        callback_url = request.build_absolute_uri('/payment/callback/')

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "email": email,
            "amount": amount*100,
            'name': name,
            'payment-description': payment_description,
            "callback_url": callback_url
        }

        try:
            response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)
            response_data = response.json()

            if response_data.get('status'):
                Payment.objects.create(
                    user=request.user,
                    reference=response_data['data']['reference'],
                    amount=amount, 
                    description=payment_description,
                    status='pending'
                )
                return redirect(response_data['data']['authorization_url'])
            else:
                logger.error(f"Paystack error: {response_data.get('message')}")
                return redirect(reverse('paymentunsucess'))
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return redirect(reverse('paymentunsucess'))

    return render(request, 'consultation/payment.html')

def payment_callback(request):
    reference = request.GET.get('reference')

    if not reference:
        return JsonResponse({"message": "Missing reference parameter."})

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
        response_data = response.json()

        if response_data.get('status') and response_data['data'].get('status') == 'success':
            Payment.objects.filter(reference=reference).update(status='completed')
            return redirect(reverse('paymentsucess'))
        else:
            Payment.objects.filter(reference=reference).update(status='failed')
            return redirect(reverse('paymentunsucess'))
        
    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return redirect(reverse('paymentunsucess'))












