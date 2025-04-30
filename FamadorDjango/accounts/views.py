from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate,logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from blog.models import BlogPost
from datetime import datetime, timedelta
import json
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {
        'form': form
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:home')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('blog:home')

@login_required
def dashboard(request):
    user = request.user
    user_posts = BlogPost.objects.filter(author=user).order_by('-created_at')
    post_count = user_posts.count()
    
    # Generate chart data for last 7 days
    date_list = []
    post_data = []
    
    for i in range(6, -1, -1):
        date = datetime.now() - timedelta(days=i)
        count = BlogPost.objects.filter(
            author=user,
            created_at__date=date.date()
        ).count()
        date_list.append(date.strftime('%a'))
        post_data.append(count)
    
    return render(request, 'accounts/dashboard.html', {
        'user': user,
        'user_posts': user_posts,
        'post_count': post_count,
        'chart_labels': json.dumps(date_list),
        'chart_data': json.dumps(post_data),
    })

@login_required
def settings_view(request):
    if request.method == 'POST':
        # Handle profile update
        if 'username' in request.POST:
            user = request.user
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.bio = request.POST.get('bio')
            
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:settings')
        
        # Handle password change
        elif 'old_password' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('accounts:settings')
            else:
                messages.error(request, 'Please correct the error below.')
                return render(request, 'accounts/settings.html', {
                    'user': request.user,
                    'password_form': form
                })
    
    return render(request, 'accounts/settings.html', {
        'user': request.user,
        'password_form': PasswordChangeForm(request.user)
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/settings.html', {'form': form})