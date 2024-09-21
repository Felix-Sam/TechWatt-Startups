from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Project,ProjectPayment
from django.http import HttpResponse,JsonResponse
import requests
import logging
logger = logging.getLogger(__name__)
from django.http import FileResponse

# For displaying the payment sucess message
@login_required(login_url = 'login')
def paymentsucessful(request):
    return render(request, 'projects/paymentsucess.html')

# For displaying the payment not sucess message
@login_required(login_url = 'login')
def paymentunsucessful(request):
    return render(request, 'projects/paymentunsucess.html')


# For checking project status if is free or paid redirect user to get the proeject 
@login_required(login_url='login')
def projects(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = Project.objects.get(id=project_id)
        
        # Check if user has already paid for this project
        previous_payment = ProjectPayment.objects.filter(
            user=request.user,
            project=project,
            status='completed'
        ).exists()

        if previous_payment:
            # Redirect to the project download page if the user has already paid
            return redirect(reverse('download_project', args=[project.id]))

        if project.price == "0" or project.price.lower() == "free":
            return redirect(project.project_url)
        
        amount = project.price
        amount = int(amount)
        callback_url = request.build_absolute_uri('/projectpayment/callback/')

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "amount": amount*100,
            'email': request.user.email,
            # "currency": "USD",
            "callback_url": callback_url
        }

        try:
            response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)
            response_data = response.json()

            if response_data.get('status'):
                ProjectPayment.objects.create(
                    user=request.user,
                    reference=response_data['data']['reference'],
                    amount=amount, 
                    status='pending',
                    project=project
                )
                return redirect(response_data['data']['authorization_url'])
            else:
                logger.error(f"Paystack error: {response_data.get('message')}")
                return redirect(reverse('paymentunsucess'))
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return redirect(reverse('paymentunsucess'))
   
    project = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects': project})



# For downloading paid projects
@login_required(login_url='login')
def download_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        file_path = project.project_zip.path  # Access the file path of the ZIP file
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=project.project_zip.name)
        return response
    except Project.DoesNotExist:
        return HttpResponse("Project not found.", status=404)

# Callback function for making payments
@login_required(login_url='login')
def ProjectPayment_callback(request):
    reference = request.GET.get('reference')

    if not reference:
        return JsonResponse({"message": "Missing reference parameter."})

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
        response_data = response.json()

        if response_data.get('status') and response_data['data'].get('status') == 'success':
            payment = ProjectPayment.objects.filter(reference=reference).update(status='completed')
            project_payment = ProjectPayment.objects.get(reference=reference)
            project = project_payment.project
            return redirect(reverse('download_project', args=[project.id]))  # Redirect to download after successful payment
            
        else:
            ProjectPayment.objects.filter(reference=reference).update(status='failed')
            return redirect(reverse('paymentunsucess'))
        
    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return redirect(reverse('paymentunsucess'))






# addining a project for admin
@login_required(login_url='login')
def add_project(request):
    # Restrict access to the specific user
    if request.user.email != 'felixsam922@gmail.com':
        return redirect(reverse('homepage'))
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        project_url = request.POST.get('project_url')
        image = request.FILES.get('image')
        project_zip = request.FILES.get('project_zip')  # Handle the zip file upload

        # Create the new project, saving both image and zip
        Project.objects.create(
            title=title, 
            description=description, 
            price=price,
            project_url=project_url, 
            image=image,
            project_zip=project_zip  # Save the zip file
        )

        # Redirect to the admin dashboard after successful creation
        return redirect(reverse('admin_dashboard'))

    # Render the form for adding a project
    return render(request, 'projects/addproject.html')



# Delete project for admin
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




