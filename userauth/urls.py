from django.urls import path 
from . import views 

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('login/',views.UserLogin,name='login'),
    path('signup/',views.UserSignup,name='signup'),
    path('logout/',views.UserLogout,name='logout'),
    path('about/',views.aboutus,name='about'),
    path('feedback/', views.user_feedback_view, name='userfeedback'),
]