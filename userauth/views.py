from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login ,logout
from .models import User , UserFeedback
from django.urls import reverse 

# Create your views here.
def homepage(request):
    
    feedback = UserFeedback.objects.all()[:6] #taking first six feedbacks

    return render(request, 'userauth/homepage.html', {'feedback': feedback})


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


# USER FEED BACK DATA
def user_feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        occupation = request.POST.get('occupation')
        social_url = request.POST.get('social_url')
        heading = request.POST.get('heading')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # Save feedback to database
        UserFeedback.objects.create(
            name = name,
            occupation=occupation,
            social_url=social_url,
            heading=heading,
            content=content,
            image=image
        )
        
        return redirect(reverse('homepage')) 
    return render(request, 'userauth/userfeedback.html')


def privacy(request):
    return render(request, 'userauth/privacy.html')

def termsofservice(request):
    return render(request, 'userauth/termsofservice.html')

def education(request):
    return render(request, 'userauth/education.html')