"""
URL configuration for django_internship project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static


def root_view(request):
    """Root endpoint with project information."""
    return JsonResponse({
        'message': 'Welcome to Django Internship Assignment API!',
        'project': 'Django REST Framework with Celery and Telegram Bot',
        'features': [
            'Django REST Framework',
            'Token Authentication',
            'Celery Background Tasks',
            'Telegram Bot Integration',
            'Production Settings',
            'Environment Variables',
            'Redis Integration',
            'Email Notifications'
        ],
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'docs': 'Check README.md for API documentation'
        },
        'version': '1.0'
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', root_view, name='root'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
