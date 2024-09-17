from django.shortcuts import render,redirect,get_object_or_404
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



# BLOGS FOR ADMIN
@login_required(login_url = 'login')
def modifyproject(request):
    # Fetch all blog posts
    project = Project.objects.all()
    # Check if the user is authenticated and has the required email
    if request.user.is_authenticated and request.user.email == 'felixsam922@gmail.com':
        if request.method == 'POST':
            if 'delete' in request.POST:
                project_id = request.POST.get('delete')
                project = get_object_or_404(Project, id=project_id)
                project.delete()
                return redirect(reverse('admin_dashboard'))
            
            elif 'edit' in request.POST:
                project_id = request.POST.get('edit')
                return redirect(reverse('editproject', args=[project_id]))
    
    # If user is not authorized, redirect to homepage
    if not request.user.is_authenticated or request.user.email != 'felixsam922@gmail.com':
        return redirect(reverse('homepage'))

    # Render the blog posts template
    return render(request, 'projects/modifyproject.html', {'projects': project})


# EDIT Project FOR ADMIN 
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.user.is_authenticated and request.user.email == 'felixsam922@gmail.com':
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            project_url = request.POST.get('project_url')
            image = request.FILES.get('image')
            
            # Update project details
            project.title = title
            project.description = description
            project.price = price
            project.project_url = project_url
            
            # Update image if a new one is uploaded
            if image:
                project.image = image
            
            project.save()  # Save the changes
            
            return redirect(reverse('admin_dashboard'))
    
    # If user is not authorized, redirect to homepage
    if not request.user.is_authenticated or request.user.email != 'felixsam922@gmail.com':
        return redirect(reverse('homepage'))
    
    return render(request, 'projects/editproject.html', {'project': project})