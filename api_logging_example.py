#!/usr/bin/env python
"""
API Logging Example - Django Internship Assignment
Demonstrates comprehensive API logging with admin interface
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def make_api_requests():
    """Make various API requests to generate logs"""
    print("=== GENERATING API LOGS FOR DEMONSTRATION ===\n")
    
    requests_made = []
    
    # 1. Public endpoint (should succeed)
    print("1. Making request to PUBLIC endpoint...")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/api/public/")
    end_time = time.time()
    requests_made.append({
        'endpoint': '/api/public/',
        'method': 'GET',
        'status': response.status_code,
        'response_time': end_time - start_time,
        'user': 'Anonymous'
    })
    print(f"   ✅ Response: {response.status_code}")
    
    # 2. Protected endpoint without auth (should fail)
    print("2. Making request to PROTECTED endpoint without auth...")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/api/protected/")
    end_time = time.time()
    requests_made.append({
        'endpoint': '/api/protected/',
        'method': 'GET',
        'status': response.status_code,
        'response_time': end_time - start_time,
        'user': 'Anonymous'
    })
    print(f"   ❌ Response: {response.status_code} (Expected - no auth)")
    
    # 3. Login to get token
    print("3. Making LOGIN request...")
    login_data = {"username": "admin", "password": "admin123"}
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
    end_time = time.time()
    requests_made.append({
        'endpoint': '/api/login/',
        'method': 'POST',
        'status': response.status_code,
        'response_time': end_time - start_time,
        'user': 'Anonymous'
    })
    
    if response.status_code == 200:
        token = response.json()['token']
        print(f"   ✅ Response: {response.status_code} - Got token")
        
        # 4. Protected endpoint with auth (should succeed)
        print("4. Making request to PROTECTED endpoint with auth...")
        headers = {'Authorization': f'Token {token}'}
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/api/protected/", headers=headers)
        end_time = time.time()
        requests_made.append({
            'endpoint': '/api/protected/',
            'method': 'GET',
            'status': response.status_code,
            'response_time': end_time - start_time,
            'user': 'admin'
        })
        print(f"   ✅ Response: {response.status_code}")
        
        # 5. User profile endpoint
        print("5. Making request to USER PROFILE endpoint...")
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/api/profile/", headers=headers)
        end_time = time.time()
        requests_made.append({
            'endpoint': '/api/profile/',
            'method': 'GET',
            'status': response.status_code,
            'response_time': end_time - start_time,
            'user': 'admin'
        })
        print(f"   ✅ Response: {response.status_code}")
        
        # 6. API logs endpoint (admin only)
        print("6. Making request to API LOGS endpoint...")
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/api/logs/", headers=headers)
        end_time = time.time()
        requests_made.append({
            'endpoint': '/api/logs/',
            'method': 'GET',
            'status': response.status_code,
            'response_time': end_time - start_time,
            'user': 'admin'
        })
        print(f"   ✅ Response: {response.status_code}")
    else:
        print(f"   ❌ Response: {response.status_code} - Login failed")
    
    # 7. Invalid endpoint (should fail)
    print("7. Making request to INVALID endpoint...")
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/api/invalid/")
    end_time = time.time()
    requests_made.append({
        'endpoint': '/api/invalid/',
        'method': 'GET',
        'status': response.status_code,
        'response_time': end_time - start_time,
        'user': 'Anonymous'
    })
    print(f"   ❌ Response: {response.status_code} (Expected - invalid endpoint)")
    
    print(f"\n📊 Made {len(requests_made)} API requests")
    return requests_made

def show_log_format_example():
    """Show example of the API log format"""
    print("\n=== API LOG FORMAT EXAMPLE ===")
    print("Each API request is automatically logged with the following information:")
    print()
    
    example_log = {
        "endpoint": "/api/protected/",
        "method": "GET", 
        "user": "admin",
        "ip_address": "127.0.0.1",
        "response_status": 200,
        "response_time": 0.045,  # in seconds
        "timestamp": "2025-06-26 09:30:15.123456+00:00"
    }
    
    print("┌" + "─" * 70 + "┐")
    print("│" + " " * 25 + "API LOG ENTRY" + " " * 25 + "│")
    print("├" + "─" * 70 + "┤")
    for key, value in example_log.items():
        field_name = key.replace("_", " ").title()
        print(f"│ {field_name:<20}: {str(value):<45} │")
    print("└" + "─" * 70 + "┘")

def show_admin_interface_info():
    """Show information about the Django admin interface"""
    print("\n=== DJANGO ADMIN INTERFACE - API LOGS ===")
    print("🌐 Admin URL: http://localhost:8000/admin/")
    print("📋 Navigate to: Home › Api › Api logs")
    print()
    print("ADMIN FEATURES:")
    print("✅ View all API logs in a table format")
    print("✅ Filter by endpoint, method, user, status code")
    print("✅ Search by IP address, endpoint")
    print("✅ Sort by timestamp, response time")
    print("✅ Export logs to CSV")
    print("✅ Read-only view (logs cannot be modified)")
    print()
    print("ADMIN LOGIN CREDENTIALS:")
    print("👤 Username: admin")
    print("🔐 Password: admin123")

def main():
    print("🚀 DJANGO INTERNSHIP ASSIGNMENT - API LOGGING DEMO")
    print("=" * 60)
    
    # Show the log format
    show_log_format_example()
    
    # Make API requests to generate logs
    requests_made = make_api_requests()
    
    # Show summary
    print("\n=== REQUEST SUMMARY ===")
    for i, req in enumerate(requests_made, 1):
        status_emoji = "✅" if 200 <= req['status'] < 300 else "❌"
        print(f"{i}. {status_emoji} {req['method']} {req['endpoint']}")
        print(f"   Status: {req['status']} | Time: {req['response_time']:.3f}s | User: {req['user']}")
    
    # Show admin interface info
    show_admin_interface_info()
    
    print(f"\n🎯 CONCEPT DEMONSTRATED:")
    print("• Automatic API request logging")
    print("• Tracking endpoint, method, user, IP, status, timing")
    print("• Django admin interface for log management")
    print("• ChangeAddDeleteView functionality in admin")
    print("• Production-ready logging system")

if __name__ == "__main__":
    main()
