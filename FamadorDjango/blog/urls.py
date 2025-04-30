from django.urls import path
from . import views

app_name = 'blog'  # This is crucial for namespacing

urlpatterns = [
    path('', views.home, name='home'),  # This defines the 'home' URL
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
]