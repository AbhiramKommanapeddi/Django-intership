#!/usr/bin/env python
"""
API Log Demo Script
Demonstrates the API logging functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
django.setup()

from api.models import ApiLog
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

def show_api_logs():
    print("=== API LOGGING DEMONSTRATION ===\n")
    
    # Get recent logs
    logs = ApiLog.objects.all().order_by('-timestamp')[:10]
    
    if not logs:
        print("No API logs found. Make some API requests first.")
        return
    
    print(f"📊 Showing {len(logs)} most recent API logs:\n")
    print("=" * 100)
    
    for i, log in enumerate(logs, 1):
        print(f"LOG #{i}")
        print(f"Endpoint: {log.endpoint}")
        print(f"Method: {log.method}")
        print(f"User: {log.user.username if log.user else 'Anonymous'}")
        print(f"IP Address: {log.ip_address}")
        print(f"Response Status: {log.response_status}")
        print(f"Response Time: {log.response_time:.3f} seconds")
        print(f"Timestamp: {log.timestamp}")
        print("-" * 100)
    
    # Show statistics
    print("\n📈 API LOG STATISTICS:")
    total_logs = ApiLog.objects.count()
    print(f"Total API requests logged: {total_logs}")
    
    # Status code distribution
    status_codes = {}
    for log in ApiLog.objects.all():
        status = log.response_status
        status_codes[status] = status_codes.get(status, 0) + 1
    
    print("\nResponse Status Distribution:")
    for status, count in sorted(status_codes.items()):
        status_name = {
            200: "OK",
            201: "Created", 
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error"
        }.get(status, "Unknown")
        print(f"  {status} ({status_name}): {count} requests")
    
    # Most accessed endpoints
    endpoints = {}
    for log in ApiLog.objects.all():
        endpoint = log.endpoint
        endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
    
    print("\nMost Accessed Endpoints:")
    for endpoint, count in sorted(endpoints.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {endpoint}: {count} requests")
    
    # Average response time
    total_time = sum(log.response_time for log in ApiLog.objects.all())
    avg_time = total_time / total_logs if total_logs > 0 else 0
    print(f"\nAverage Response Time: {avg_time:.3f} seconds")

def create_sample_logs():
    """Create some sample API logs for demonstration"""
    print("\n🔧 Creating sample API logs for demonstration...\n")
    
    # Get or create a user
    user, created = User.objects.get_or_create(
        username='demo_user',
        defaults={
            'email': 'demo@example.com',
            'first_name': 'Demo',
            'last_name': 'User'
        }
    )
    
    sample_logs = [
        {
            'endpoint': '/api/public/',
            'method': 'GET',
            'user': None,  # Anonymous
            'ip_address': '192.168.1.100',
            'response_status': 200,
            'response_time': 0.045
        },
        {
            'endpoint': '/api/protected/',
            'method': 'GET',
            'user': user,
            'ip_address': '192.168.1.100',
            'response_status': 200,
            'response_time': 0.123
        },
        {
            'endpoint': '/api/login/',
            'method': 'POST',
            'user': None,
            'ip_address': '192.168.1.101',
            'response_status': 200,
            'response_time': 0.234
        },
        {
            'endpoint': '/api/protected/',
            'method': 'GET',
            'user': None,
            'ip_address': '192.168.1.102',
            'response_status': 401,
            'response_time': 0.012
        },
        {
            'endpoint': '/api/register/',
            'method': 'POST',
            'user': None,
            'ip_address': '192.168.1.103',
            'response_status': 400,
            'response_time': 0.156
        }
    ]
    
    for log_data in sample_logs:
        ApiLog.objects.create(**log_data)
        print(f"✅ Created log: {log_data['method']} {log_data['endpoint']} - {log_data['response_status']}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--create-samples':
        create_sample_logs()
    
    show_api_logs()
