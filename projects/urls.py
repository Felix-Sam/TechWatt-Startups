from django.urls import path
from . import views


urlpatterns = [
path('projects/',views.projects,name='projects'),
path('addproject/',views.add_project,name='add-project'),
path('modifyproject/',views.modifyproject,name='modify-project'),
path('editproject/<int:project_id>/', views.edit_project, name='editproject'),  # For admin to edit blogs
]