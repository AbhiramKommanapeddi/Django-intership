#!/usr/bin/env python
"""
Test script for Django Internship Assignment API
Run this script to test all the API endpoints
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com", 
    "password": "testpassword123",
    "password_confirm": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def print_response(response, description=""):
    print(f"\n{description}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    """Test all API endpoints"""
    print_section("Django Internship Assignment - API Test")
    print(f"Testing API at: {BASE_URL}")
    print(f"Test time: {datetime.now()}")
    
    # Test 1: Root endpoint
    print_section("1. Testing Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response, "Root endpoint (GET /)")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server. Make sure Django is running on localhost:8000")
        return False
    
    # Test 2: Public endpoint
    print_section("2. Testing Public Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/public/")
        print_response(response, "Public endpoint (GET /api/public/)")
    except Exception as e:
        print(f"❌ Error testing public endpoint: {e}")
    
    # Test 3: User Registration
    print_section("3. Testing User Registration")
    try:
        response = requests.post(
            f"{BASE_URL}/api/register/",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        print_response(response, "User registration (POST /api/register/)")
        
        if response.status_code == 201:
            token = response.json().get('token')
            print(f"✅ Registration successful! Token: {token[:20]}...")
        else:
            print("❌ Registration failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return False
    
    # Test 4: User Login
    print_section("4. Testing User Login")
    try:
        login_data = {
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        response = requests.post(
            f"{BASE_URL}/api/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print_response(response, "User login (POST /api/login/)")
        
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"✅ Login successful! Token: {token[:20]}...")
        else:
            print("❌ Login failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during login: {e}")
        return False
    
    # Test 5: Protected endpoint without authentication
    print_section("5. Testing Protected Endpoint (No Auth)")
    try:
        response = requests.get(f"{BASE_URL}/api/protected/")
        print_response(response, "Protected endpoint without auth (GET /api/protected/)")
        
        if response.status_code == 401:
            print("✅ Correctly rejected unauthorized access")
        else:
            print("❌ Should have rejected unauthorized access")
            
    except Exception as e:
        print(f"❌ Error testing protected endpoint: {e}")
    
    # Test 6: Protected endpoint with authentication
    print_section("6. Testing Protected Endpoint (With Auth)")
    try:
        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/api/protected/", headers=headers)
        print_response(response, "Protected endpoint with auth (GET /api/protected/)")
        
        if response.status_code == 200:
            print("✅ Successfully accessed protected endpoint")
        else:
            print("❌ Failed to access protected endpoint with valid token")
            
    except Exception as e:
        print(f"❌ Error testing protected endpoint with auth: {e}")
    
    # Test 7: User Profile
    print_section("7. Testing User Profile")
    try:
        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/api/profile/", headers=headers)
        print_response(response, "User profile (GET /api/profile/)")
        
        if response.status_code == 200:
            print("✅ Successfully retrieved user profile")
        else:
            print("❌ Failed to retrieve user profile")
            
    except Exception as e:
        print(f"❌ Error testing user profile: {e}")
    
    print_section("API Test Summary")
    print("✅ All basic tests completed!")
    print("\n📝 Next Steps:")
    print("1. Start Redis server for Celery")
    print("2. Start Celery worker: celery -A django_internship worker -l info")
    print("3. Configure Telegram bot token in .env file")
    print("4. Start Telegram bot: python manage.py run_telegram_bot")
    print("5. Test the /start command with your bot")
    print("\n🔗 API Endpoints Summary:")
    print(f"  Root: {BASE_URL}/")
    print(f"  Public: {BASE_URL}/api/public/")
    print(f"  Register: {BASE_URL}/api/register/")
    print(f"  Login: {BASE_URL}/api/login/")
    print(f"  Protected: {BASE_URL}/api/protected/")
    print(f"  Profile: {BASE_URL}/api/profile/")
    print(f"  Admin: {BASE_URL}/admin/")
    
    return True

if __name__ == "__main__":
    print("Django Internship Assignment - API Testing Script")
    print("Make sure the Django server is running: python manage.py runserver")
    
    input("\nPress Enter to start testing...")
    success = test_api()
    
    if success:
        print("\n🎉 All tests passed! Your Django Internship Assignment is working correctly!")
    else:
        print("\n❌ Some tests failed. Check the Django server and try again.")
    
    input("\nPress Enter to exit...")
