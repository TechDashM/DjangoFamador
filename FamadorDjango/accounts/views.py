from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate,logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost
from datetime import datetime, timedelta
import json

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
    post_count = BlogPost.objects.filter(author=user).count()
    
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
        'post_count': post_count,
        'chart_labels': json.dumps(date_list),
        'chart_data': json.dumps(post_data),
    })