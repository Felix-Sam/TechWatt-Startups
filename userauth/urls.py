from django.urls import path 
from . import views 

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('login/',views.UserLogin,name='login'),
    path('signup/',views.UserSignup,name='signup'),
    path('logout/',views.UserLogout,name='logout'),
    path('about/',views.aboutus,name='about'),
    path('feedback/', views.user_feedback_view, name='userfeedback'),
    path('privacy/', views.privacy, name='privacy'),
    path('termsofservice/', views.termsofservice, name='termsofservice'),
    path('education/', views.education, name='education'),
    path('pythoncourse/', views.python_CourseOuline, name='pythoncourse'),
    path('machinelearningcourse/', views. machinelearning_CourseOuline, name='machinelearningcourse'),
    path('chatbotcourse/', views.chatbot_CourseOutline, name='chatbotcourse'),
    path('roboticscourse/', views.robotics_CourseOutline, name='roboticscourse'),
    path('computervision/', views.computervision_CourseOutline ,name='computervisioncourse'),
    path('generativeai/', views.generativeai_CourseOutline, name='generativeaicourse'),
]