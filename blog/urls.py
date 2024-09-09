from django.urls import path
from . import views

urlpatterns = [
    path('viewblogs/', views.viewblogs, name='viewersblog'),  # For viewers
    path('blogs/', views.blogs, name='blogs'),  # For admin to see and edit all blogs
    path('createblog/', views.create_blog, name='create_blogs'),  # For admin to create blogs
    path('editblog/<int:blog_id>/', views.edit_blog, name='editblog'),  # For admin to edit blogs
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),  # Route for blog detail
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # New route for the admin dashboard
]
