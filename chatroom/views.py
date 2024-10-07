from django.shortcuts import render,redirect
from .models import ChatFormData,Message
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required(login_url = 'login')
def ChatroomForm(request):
    user = request.user

    # Check if the user has already registered
    if ChatFormData.objects.filter(user=user).exists():
        return redirect('chats') 

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')

        ChatFormData.objects.create(name=name, image=image, user=user)

        return redirect(reverse('chats'))  

    return render(request, 'chatroom/chatform.html')

@login_required(login_url = 'login')
def Chats(request):
    # Get all messages from the database ordered by creation date
    messages = Message.objects.all().order_by('date_created')

    if request.method == 'POST':
        user_data = ChatFormData.objects.get(user=request.user)
        message_content = request.POST.get('message')
        # uploaded_file = request.FILES.get('file')  # Retrieve the uploaded file from the form

        # Create a new message and save it to the database
        message = Message.objects.create(
            user_data=user_data,
            message=message_content,
            # file=uploaded_file  # CloudinaryField will handle the file upload
        )
        message.save()

    return render(request, 'chatroom/chats.html', {'messages': messages})