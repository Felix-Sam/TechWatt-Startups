from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Project



@login_required(login_url = 'login')
def projects(request):
    project = Project.objects.all()
    
    return render(request,'projects/projects.html',{'projects':project})

@login_required(login_url = 'login')
def add_project(request):
    if request.user.email != 'felixsam922@gmail.com':
        return redirect(reverse('homepage'))
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        project_url = request.POST.get('project_url')
        image = request.FILES.get('image')

        # Create the new project
        Project.objects.create(title=title, description=description, price=price,project_url = project_url, image=image)
        
        # Redirect to the admin dashboard after successful creation
        return redirect(reverse('admin_dashboard'))

    # Render the form for adding a project
    return render(request, 'projects/addproject.html')