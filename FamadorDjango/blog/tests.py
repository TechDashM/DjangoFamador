from django.urls import path
from .views import home, post_detail, create_post  # All views should be available now

urlpatterns = [
    path('', home, name='home'),  # Handles root URL
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('create/', create_post, name='create_post'),
]