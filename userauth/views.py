from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login ,logout
from .models import User 
from django.urls import reverse 

# Create your views here.
def homepage(request):

    return render(request,'userauth/homepage.html')


def UserLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Login the user
            login(request, user)
            return redirect(reverse('homepage'))
        else:
            HttpResponse('Invalid email or password')
            return redirect(reverse('login'))
    
    return render(request,'userauth/login.html')


def UserLogout(request):
    logout(request)
    return redirect(reverse('homepage'))

def UserSignup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

     
        if password != confirmpassword:
            return HttpResponse('Passwords do not match')

        if User.objects.filter(email=email).exists():
            return HttpResponse('Email is already registered')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        login(request, user)
        login(request, user)
        return redirect(reverse('homepage'))

    return render(request,'userauth/signup.html')

def aboutus(request):
    return render(request,'userauth/about.html')