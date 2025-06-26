from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import time

from .models import UserProfile, ApiLog
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    ApiLogSerializer, 
    UserRegistrationSerializer
)
from .tasks import send_welcome_email


class ApiLogMixin:
    """Mixin to log API requests."""
    
    def log_request(self, request, response):
        """Log the API request."""
        try:
            # Calculate response time (this is approximate)
            response_time = getattr(request, '_start_time', 0)
            if response_time:
                response_time = time.time() - response_time
            else:
                response_time = 0
            
            ApiLog.objects.create(
                endpoint=request.path,
                method=request.method,
                user=request.user if request.user.is_authenticated else None,
                ip_address=self.get_client_ip(request),
                response_status=response.status_code,
                response_time=response_time
            )
        except Exception as e:
            # Don't let logging errors break the API
            print(f"Logging error: {e}")
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to add logging."""
        request._start_time = time.time()
        response = super().dispatch(request, *args, **kwargs)
        self.log_request(request, response)
        return response


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_endpoint(request):
    """
    Public endpoint accessible to everyone.
    Returns current server time and basic API information.
    """
    data = {
        'message': 'Welcome to Django Internship API!',
        'server_time': timezone.now().isoformat(),
        'api_version': '1.0',
        'endpoints': {
            'public': '/api/public/',
            'protected': '/api/protected/',
            'register': '/api/register/',
            'login': '/api/login/',
            'profile': '/api/profile/',
            'logs': '/api/logs/'
        },
        'authentication': 'Token Authentication required for protected endpoints'
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def protected_endpoint(request):
    """
    Protected endpoint accessible only to authenticated users.
    Returns user information and protected data.
    """
    data = {
        'message': f'Hello {request.user.username}! This is a protected endpoint.',
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'access_time': timezone.now().isoformat(),
        'user_permissions': list(request.user.get_all_permissions()),
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """
    Register a new user and send welcome email.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        # Send welcome email asynchronously
        send_welcome_email.delay(user.id)
        
        return Response({
            'message': 'User registered successfully!',
            'user_id': user.id,
            'username': user.username,
            'token': token.key,
            'email_sent': 'Welcome email will be sent shortly'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    """
    Authenticate user and return token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(ApiLogMixin, generics.RetrieveUpdateAPIView):
    """
    Get or update user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ApiLogListView(ApiLogMixin, generics.ListAPIView):
    """
    List API logs (admin only).
    """
    serializer_class = ApiLogSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_queryset(self):
        return ApiLog.objects.all()[:100]  # Limit to last 100 logs
