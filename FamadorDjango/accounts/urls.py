from django.urls import path
from .views import register_view, login_view, logout_view, dashboard

app_name = 'accounts'  # This is crucial

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),  # This defines the login URL
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]