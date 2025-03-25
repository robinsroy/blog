from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post, Comment
from .forms import UserRegistrationForm, UserManagementForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import JsonResponse

class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('admin:index')
        return reverse_lazy('blog:post_list')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('blog:post_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_auth/register.html', {'form': form})

@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created')
    user_comments = Comment.objects.filter(author=request.user).order_by('-created')
    
    context = {
        'user': request.user,
        'user_posts': user_posts,
        'user_comments': user_comments,
    }
    return render(request, 'user_auth/profile.html', context)

@login_required
def custom_admin(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('blog:post_list')
    
    # Get statistics
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    total_users = User.objects.count()
    
    # Get recent activity
    recent_posts = Post.objects.order_by('-created')[:5]
    recent_comments = Comment.objects.order_by('-created')[:5]
    
    context = {
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_users': total_users,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
    }
    return render(request, 'user_auth/custom_admin.html', context)

@login_required
def user_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create users.')
        return redirect('blog:post_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('user_auth:custom_admin')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'user_auth/user_form.html', {'form': form, 'title': 'Create User'})

@login_required
def user_edit(request, user_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit users.')
        return redirect('blog:post_list')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserManagementForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated successfully.')
            return redirect('user_auth:custom_admin')
    else:
        form = UserManagementForm(instance=user)
    
    return render(request, 'user_auth/user_form.html', {'form': form, 'title': 'Edit User'})

@login_required
def user_delete(request, user_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete users.')
        return redirect('blog:post_list')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully.')
        return redirect('user_auth:custom_admin')
    
    return render(request, 'user_auth/user_confirm_delete.html', {'user': user})

@login_required
def user_detail(request, user_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to view user details.')
        return redirect('blog:post_list')
    
    user = get_object_or_404(User, id=user_id)
    user_posts = Post.objects.filter(author=user).order_by('-created')
    user_comments = Comment.objects.filter(author=user).order_by('-created')
    
    context = {
        'user': user,
        'user_posts': user_posts,
        'user_comments': user_comments,
    }
    
    return render(request, 'user_auth/user_detail.html', context)
