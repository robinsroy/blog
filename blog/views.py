from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm
import json

def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-created')
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    
    # Pagination
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by('-created')
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.active = True
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('blog:post_detail', slug=post.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user is the author or staff
    if not (request.user == post.author or request.user.is_staff):
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blog:post_detail', slug=slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user is the author or staff
    if not (request.user == post.author or request.user.is_staff):
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('blog:post_detail', slug=slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added.')
    return redirect('blog:post_detail', slug=post.slug)

@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        messages.error(request, 'You can only edit your own comments.')
        return redirect('blog:post_detail', slug=comment.post.slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            messages.success(request, 'Your comment has been updated.')
            return redirect('blog:post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'post': comment.post,
    }
    return render(request, 'blog/comment_form.html', context)

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('blog:post_detail', slug=comment.post.slug)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted.')
        return redirect('blog:post_detail', slug=comment.post.slug)

    context = {
        'comment': comment,
    }
    return render(request, 'blog/comment_confirm_delete.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-created')
    
    # Pagination
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'posts': page_obj,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/category_detail.html', context)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user, status='published').order_by('-created')
    comments = Comment.objects.filter(author=user, active=True).order_by('-created')
    
    context = {
        'profile_user': user,
        'posts': posts,
        'comments': comments,
    }
    return render(request, 'blog/user_profile.html', context)

@login_required
def like_post(request, post_id):
    """
    Handle liking a post with different reaction types
    """
    post = get_object_or_404(Post, id=post_id)
    
    # Check if this is an AJAX request with reaction type
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        reaction_type = data.get('reaction_type', 'like')
        
        # For now, we'll just toggle the like status regardless of reaction type
        # In a more advanced implementation, you would store the reaction type
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            action = 'removed'
        else:
            post.likes.add(request.user)
            action = 'added'
            
        return JsonResponse({
            'success': True,
            'like_count': post.like_count,
            'action': action,
            'reaction_type': reaction_type
        })
    
    # Handle non-AJAX requests for backward compatibility
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return redirect('blog:post_detail', slug=post.slug)

@login_required
def like_comment(request, comment_id):
    """
    Handle liking a comment with different reaction types
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if this is an AJAX request with reaction type
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        reaction_type = data.get('reaction_type', 'like')
        
        # For now, we'll just toggle the like status regardless of reaction type
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            action = 'removed'
        else:
            comment.likes.add(request.user)
            action = 'added'
            
        return JsonResponse({
            'success': True,
            'like_count': comment.like_count,
            'action': action,
            'reaction_type': reaction_type
        })
    
    # Handle non-AJAX requests for backward compatibility
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    
    post = comment.post
    return redirect('blog:post_detail', slug=post.slug)
