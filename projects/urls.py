from django.urls import path
from . import views


urlpatterns = [
path('projects/',views.projects,name='projects'),
path('addproject/',views.add_project,name='add-project')
]