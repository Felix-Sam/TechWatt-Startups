from django.shortcuts import render ,redirect, get_object_or_404
from .models import BlogImage,BlogPost
from django.http import HttpResponse
from .models import BlogPost, BlogImage
from django.http import Http404
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# CREATING BLOG
@login_required(login_url='login')
def create_blog(request):
    if request.user.email != 'felixsam922@gmail.com':
        return redirect(reverse('homepage'))

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        images = request.FILES.getlist('images')
        author = request.user
        
        # Create the blog post
        blog_post = BlogPost.objects.create(title=title, content=content, author=author)
        
        # Save each image
        for image in images:
            BlogImage.objects.create(blog_post=blog_post, image=image)
        
        return redirect(reverse('admin_dashboard'))  # Redirect after creation

    return render(request, 'blog/createblog.html')

# BLOGS FOR VIEWERS
@login_required(login_url = 'login')
def viewblogs(request):
    blogs = BlogPost.objects.all()  # Get all blog posts

    blogdata = {
        'blogs': blogs,  
    }

    return render(request, 'blog/viewblogs.html', context=blogdata)


# BLOGS FOR ADMIN
@login_required(login_url = 'login')
def blogs(request):
    # Fetch all blog posts
    blog_posts = BlogPost.objects.all()
    # Check if the user is authenticated and has the required email
    if request.user.is_authenticated and request.user.email == 'felixsam922@gmail.com':
        if request.method == 'POST':
            if 'delete' in request.POST:
                blog_id = request.POST.get('delete')
                blog = get_object_or_404(BlogPost, id=blog_id)
                blog.delete()
                return redirect(reverse('blogs'))
            
            elif 'edit' in request.POST:
                blog_id = request.POST.get('edit')
                return redirect(reverse('editblog', args=[blog_id]))
    
    # If user is not authorized, redirect to homepage
    if not request.user.is_authenticated or request.user.email != 'felixsam922@gmail.com':
        return redirect(reverse('homepage'))

    # Render the blog posts template
    return render(request, 'blog/blogs.html', {'blogs': blog_posts})


# EDIT BLOGS FOR ADMIN 
def edit_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    if request.user.is_authenticated and request.user.email == 'felixsam922@gmail.com':
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            images = request.FILES.getlist('images')
            
            # Update blog post
            blog.title = title
            blog.content = content
            blog.save()

            # Update images
            if images:
                BlogImage.objects.filter(blog_post=blog).delete()  # Remove existing images
                for image in images:
                    BlogImage.objects.create(blog_post=blog, image=image)
            
            return redirect(reverse('blogs'))
    # If user is not authorized, redirect to homepage
    if not request.user.is_authenticated or request.user.email != 'felixsam922@gmail.com':
        return redirect(reverse('homepage'))
    
    return render(request, 'blog/editblog.html', {'blog': blog})


# For readmore information about a given blog. For readers 
def blog_detail(request, blog_id):
    # Fetch the blog post by ID
    blog = get_object_or_404(BlogPost, id=blog_id)
    # Pass the blog post to the template
    return render(request, 'blog/readmore.html', {'blog': blog})



# Admin dashboard for the blog post
def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.email != 'felixsam922@gmail.com':
        return redirect(reverse('homepage'))

    # If the user is authenticated and authorized
    blogs = BlogPost.objects.all()  # Fetch all blogs for admin
    context = {
        'blogs': blogs
    }

    return render(request, 'blog/dashboard.html', context)