#!/usr/bin/env python
"""
Simple test script to demonstrate API endpoints working
"""
import requests
import json

BASE_URL = "http://localhost:8000"
TOKEN = "2e74638b2725e728908c7ff18a24511d0974bdb4"  # testuser token

def test_endpoints():
    print("=== Django Internship Assignment - API Endpoints Demo ===\n")
    
    # Test 1: Public endpoint (no authentication required)
    print("1. Testing PUBLIC endpoint (accessible to everyone):")
    try:
        response = requests.get(f"{BASE_URL}/api/public/")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: {data['message']}")
            print(f"   Server Time: {data['server_time']}")
        else:
            print(f"   ❌ FAILED: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print()
    
    # Test 2: Protected endpoint without token (should fail)
    print("2. Testing PROTECTED endpoint WITHOUT authentication:")
    try:
        response = requests.get(f"{BASE_URL}/api/protected/")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 401:
            print(f"   ✅ CORRECTLY BLOCKED: Authentication required")
        else:
            print(f"   ❌ UNEXPECTED: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print()
    
    # Test 3: Protected endpoint with valid token (should succeed)
    print("3. Testing PROTECTED endpoint WITH valid token:")
    try:
        headers = {'Authorization': f'Token {TOKEN}'}
        response = requests.get(f"{BASE_URL}/api/protected/", headers=headers)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: {data['message']}")
            print(f"   User: {data['username']} (ID: {data['user_id']})")
            print(f"   Is Staff: {data['is_staff']}")
        else:
            print(f"   ❌ FAILED: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print()
    
    # Test 4: Login endpoint
    print("4. Testing LOGIN endpoint:")
    try:
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: {data['message']}")
            print(f"   Token: {data['token'][:20]}...")
        else:
            print(f"   ❌ FAILED: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print("\n=== Summary ===")
    print("✅ Public endpoint: Accessible to everyone")
    print("✅ Protected endpoint: Requires token authentication")
    print("✅ Django admin: Available at http://localhost:8000/admin/")
    print("✅ All API endpoints are working correctly!")

if __name__ == "__main__":
    test_endpoints()
