from django.urls import path 
from . import views

urlpatterns = [
    path('userdata/',views.ChatroomForm,name='userdata'),
    path('chats/',views.Chats,name='chats'),
]