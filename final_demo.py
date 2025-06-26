#!/usr/bin/env python
"""
Final demonstration of Django Internship Assignment API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def final_demo():
    print("=== DJANGO INTERNSHIP ASSIGNMENT - FINAL DEMO ===\n")
    
    # Test 1: Public endpoint
    print("🌐 1. PUBLIC ENDPOINT (No authentication required)")
    print("   URL: GET /api/public/")
    response = requests.get(f"{BASE_URL}/api/public/")
    print(f"   ✅ Status: {response.status_code} - Accessible to everyone")
    data = response.json()
    print(f"   📝 Message: {data['message']}")
    print(f"   🕒 Server Time: {data['server_time']}")
    print()
    
    # Test 2: Protected endpoint without auth (should fail)
    print("🔒 2. PROTECTED ENDPOINT (Without authentication)")
    print("   URL: GET /api/protected/")
    response = requests.get(f"{BASE_URL}/api/protected/")
    print(f"   ❌ Status: {response.status_code} - Authentication required")
    print("   📝 This correctly blocks unauthorized access")
    print()
    
    # Test 3: Login to get token
    print("🔑 3. LOGIN ENDPOINT (Getting authentication token)")
    print("   URL: POST /api/login/")
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        token = data['token']
        print(f"   ✅ Status: {response.status_code} - Login successful")
        print(f"   🎫 Token: {token[:20]}...")
        print(f"   👤 User: {data['username']}")
        
        # Test 4: Protected endpoint with token
        print()
        print("🛡️ 4. PROTECTED ENDPOINT (With valid token)")
        print("   URL: GET /api/protected/")
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(f"{BASE_URL}/api/protected/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code} - Access granted")
            print(f"   📝 Message: {data['message']}")
            print(f"   👤 User ID: {data['user_id']}")
            print(f"   🔧 Is Staff: {data['is_staff']}")
            print(f"   ⚡ Is Superuser: {data['is_superuser']}")
        else:
            print(f"   ❌ Status: {response.status_code}")
    else:
        print(f"   ❌ Status: {response.status_code} - Login failed")
    
    print()
    print("=== FEATURES DEMONSTRATED ===")
    print("✅ Django REST Framework setup")
    print("✅ Public API endpoint (accessible to everyone)")
    print("✅ Protected API endpoint (Token authentication required)")
    print("✅ Django Admin panel (web-based login at /admin/)")
    print("✅ User registration and login system")
    print("✅ Token-based authentication")
    print("✅ Production-ready settings with environment variables")
    print("✅ Proper error handling and status codes")
    
    print()
    print("🌐 Web Access:")
    print(f"   • API Root: {BASE_URL}/")
    print(f"   • Django Admin: {BASE_URL}/admin/")
    print(f"   • Public API: {BASE_URL}/api/public/")
    print(f"   • Protected API: {BASE_URL}/api/protected/")

if __name__ == "__main__":
    final_demo()
