from django.urls import path
from . import views


urlpatterns = [
path('projects/',views.projects,name='projects'),
path('addproject/',views.add_project,name='add-project'),
path('modifyproject/',views.modifyproject,name='modify-project'),
path('editproject/<int:project_id>/', views.edit_project, name='editproject'),  # For admin to edit projects
path('projectpayment/callback/', views.ProjectPayment_callback, name='ProjectPayment_callback'),


path('paymentsucess/',views.paymentsucessful,name='paymentsucess'),
path('paymentunsucess/',views.paymentunsucessful,name='paymentunsucess'),

path('download_project/<int:project_id>/', views.download_project, name='download_project'),

]