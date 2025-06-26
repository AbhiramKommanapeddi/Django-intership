#!/usr/bin/env python3
"""
Simple test script to demonstrate the login process
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_login_flow():
    print("🚀 Testing Django Internship Assignment Login Flow")
    print("="*60)
    
    # Step 1: Test public endpoint
    print("\n1️⃣ Testing public endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/public/")
        if response.status_code == 200:
            print("✅ Public endpoint working!")
        else:
            print(f"❌ Public endpoint failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Make sure Django server is running: python manage.py runserver")
        return
    
    # Step 2: Register a test user
    print("\n2️⃣ Registering test user...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=register_data)
        print(f"Registration status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ User registered successfully!")
            reg_data = response.json()
            token = reg_data.get('token')
            print(f"Registration token: {token[:20]}...")
        elif response.status_code == 400:
            print("ℹ️ User might already exist, proceeding to login...")
        else:
            print(f"Registration response: {response.text}")
    except Exception as e:
        print(f"Registration error: {e}")
    
    # Step 3: Login user
    print("\n3️⃣ Testing login...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=login_data)
        print(f"Login status: {response.status_code}")
        print(f"Login response: {response.text}")
        
        if response.status_code == 200:
            login_result = response.json()
            token = login_result.get('token')
            print(f"\n🎉 LOGIN SUCCESS!")
            print(f"🔑 Your authentication token: {token}")
            print(f"👤 User ID: {login_result.get('user_id')}")
            print(f"👤 Username: {login_result.get('username')}")
            
            # Step 4: Test protected endpoint
            print("\n4️⃣ Testing protected endpoint with token...")
            headers = {"Authorization": f"Token {token}"}
            protected_response = requests.get(f"{BASE_URL}/api/protected/", headers=headers)
            
            if protected_response.status_code == 200:
                print("✅ Protected endpoint access successful!")
                protected_data = protected_response.json()
                print(f"Protected data: {json.dumps(protected_data, indent=2)}")
            else:
                print(f"❌ Protected endpoint failed: {protected_response.status_code}")
            
            print(f"\n📋 CURL Commands for you to use:")
            print(f"# Login command:")
            print(f'curl -X POST {BASE_URL}/api/login/ \\')
            print(f'  -H "Content-Type: application/json" \\')
            print(f'  -d \'{{"username":"testuser","password":"testpass123"}}\'')
            print(f"\n# Access protected endpoint:")
            print(f'curl -H "Authorization: Token {token}" {BASE_URL}/api/protected/')
            
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"Login error: {e}")

if __name__ == "__main__":
    test_login_flow()
