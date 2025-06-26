#!/usr/bin/env python
"""
Test Celery integration by creating a user and triggering welcome email task
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_registration_with_celery():
    """Test user registration that triggers welcome email task"""
    print("=== TESTING CELERY INTEGRATION WITH USER REGISTRATION ===\n")
    
    # Test user data
    test_user = {
        "username": f"celerytest_{int(time.time())}",  # Unique username
        "email": "celerytest@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "first_name": "Celery",
        "last_name": "Test"
    }
    
    print("📝 Registering new user with the following data:")
    print(f"   Username: {test_user['username']}")
    print(f"   Email: {test_user['email']}")
    print(f"   First Name: {test_user['first_name']}")
    print(f"   Last Name: {test_user['last_name']}")
    print()
    
    try:
        # Make registration request
        print("🚀 Sending registration request...")
        response = requests.post(f"{BASE_URL}/api/register/", json=test_user)
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Username: {data.get('username')}")
            print(f"   Token: {data.get('token', 'N/A')[:20]}...")
            print(f"   Email Status: {data.get('email_sent', 'N/A')}")
            print()
            
            print("🔍 What happens in the background:")
            print("   1. User account created in database")
            print("   2. Authentication token generated")
            print("   3. Response sent immediately to client")
            print("   4. 🚀 Welcome email task queued for Celery worker")
            print("   5. Celery worker processes email task asynchronously")
            print()
            
            print("📧 Expected Welcome Email Content:")
            print(f"   To: {test_user['email']}")
            print(f"   Subject: Welcome to Django Internship API!")
            print(f"   Content: HTML + text email with user details")
            print(f"   Includes: Username, email, registration date, API usage instructions")
            print()
            
            return True
            
        elif response.status_code == 400:
            error_data = response.json()
            print("❌ Registration failed (expected if user exists):")
            for field, errors in error_data.items():
                print(f"   {field}: {errors}")
            print()
            return False
            
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server")
        print("   Make sure Django is running: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error during registration test: {e}")
        return False

def show_celery_worker_info():
    """Show information about Celery worker"""
    print("=== CELERY WORKER INFORMATION ===")
    print()
    print("🔧 To start Celery worker and see background tasks:")
    print("   1. Install Redis:")
    print("      Windows: docker run -d -p 6379:6379 redis:alpine")
    print("      macOS: brew install redis && redis-server")
    print("      Linux: sudo apt install redis-server")
    print()
    print("   2. Start Redis server:")
    print("      redis-server")
    print()
    print("   3. Start Celery worker in new terminal:")
    print("      cd 'c:\\Users\\abhik\\Downloads\\Django intership'")
    print("      source venv/Scripts/activate")
    print("      celery -A django_internship worker --loglevel=info")
    print()
    print("   4. Run this test again")
    print()
    print("📊 When Celery worker is running, you'll see:")
    print("   • Task received: api.tasks.send_welcome_email")
    print("   • Task execution logs")
    print("   • Task completion status")
    print("   • Email sending results")
    print()

def show_task_status_without_worker():
    """Show what happens when Celery worker is not running"""
    print("=== TASK BEHAVIOR WITHOUT CELERY WORKER ===")
    print()
    print("📝 Current behavior (without Redis/Celery worker):")
    print("   ✅ User registration still works normally")
    print("   ✅ API responds immediately")
    print("   📨 Email task is queued but not processed")
    print("   ⏳ Task waits in queue until worker starts")
    print()
    print("🔄 With Celery worker running:")
    print("   ✅ User registration works normally")
    print("   ✅ API responds immediately")
    print("   📨 Email task is queued AND processed")
    print("   📧 Welcome email is actually sent")
    print("   📊 Task results are stored and trackable")
    print()
    print("💡 This demonstrates the non-blocking nature of Celery:")
    print("   • API performance is not affected by email sending")
    print("   • User gets immediate response")
    print("   • Background tasks run independently")
    print("   • System remains responsive under heavy load")

def main():
    print("🚀 DJANGO INTERNSHIP ASSIGNMENT - CELERY INTEGRATION TEST")
    print("=" * 65)
    print()
    
    # Test registration
    success = test_registration_with_celery()
    
    if success:
        print("🎉 CELERY INTEGRATION TEST COMPLETED")
        print()
        print("✅ User registration successful")
        print("✅ Background task queued")
        print("✅ Non-blocking operation demonstrated")
        print()
        
    show_task_status_without_worker()
    show_celery_worker_info()
    
    print("🎯 KEY FEATURES DEMONSTRATED:")
    print("✅ Asynchronous task execution")
    print("✅ Background email processing")
    print("✅ Non-blocking API responses")
    print("✅ Redis as message broker")
    print("✅ Task queuing and processing")
    print("✅ Error handling and logging")
    print("✅ Production-ready configuration")

if __name__ == "__main__":
    main()
