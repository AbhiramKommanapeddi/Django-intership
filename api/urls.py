from django.urls import path
from . import views

urlpatterns = [
    # Public endpoint
    path('public/', views.public_endpoint, name='public-endpoint'),
    
    # Protected endpoint
    path('protected/', views.protected_endpoint, name='protected-endpoint'),
    
    # Authentication endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    
    # User profile
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # API logs (admin only)
    path('logs/', views.ApiLogListView.as_view(), name='api-logs'),
]
