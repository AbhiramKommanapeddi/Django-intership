#!/usr/bin/env python
"""
Celery Integration Example - User Registration with Background Email

This example demonstrates:
1. How user registration triggers background email tasks
2. What happens when Redis/Celery is available vs not available
3. The complete flow from registration to email delivery
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_user_registration_celery():
    """Test user registration that triggers Celery email task"""
    print("=== CELERY INTEGRATION EXAMPLE ===")
    print("Testing user registration with background email task\n")
    
    # Create test user data
    timestamp = int(time.time())
    user_data = {
        "username": f"testuser_{timestamp}",
        "email": "testuser@example.com", 
        "password": "securepassword123",
        "password_confirm": "securepassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    print("🔥 Registering new user:")
    print(f"   Username: {user_data['username']}")
    print(f"   Email: {user_data['email']}")
    print(f"   Name: {user_data['first_name']} {user_data['last_name']}")
    
    try:
        # Make registration request
        print("\n📡 Sending registration request to Django API...")
        response = requests.post(f"{BASE_URL}/api/register/", json=user_data)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            # Registration successful
            data = response.json()
            print("\n✅ SUCCESS! User registration completed")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Username: {data.get('username')}")
            print(f"   Auth Token: {data.get('token', 'N/A')[:25]}...")
            print(f"   Email Status: {data.get('email_sent')}")
            
            print("\n🎯 What happens behind the scenes:")
            print("   1. ✅ User account created in database")
            print("   2. ✅ Authentication token generated") 
            print("   3. ✅ Welcome email task queued in Celery")
            print("   4. ⏳ Task waits for Celery worker to process")
            
            print("\n📧 Email Task Details:")
            print("   Task: send_welcome_email")
            print("   Arguments: user_id =", data.get('user_id'))
            print("   Queue: celery (default)")
            print("   Broker: Redis (redis://localhost:6379/0)")
            
            print("\n💡 To see the email task execute:")
            print("   1. Start Redis: docker run -d -p 6379:6379 --name redis redis:alpine")
            print("   2. Start Celery worker: celery -A django_internship worker --loglevel=info")
            print("   3. The welcome email task will process automatically")
            
            return True
            
        elif response.status_code == 400:
            # Validation errors
            errors = response.json()
            print(f"\n❌ Registration failed - Validation errors:")
            for field, error_list in errors.items():
                if isinstance(error_list, list):
                    for error in error_list:
                        print(f"   {field}: {error}")
                else:
                    print(f"   {field}: {error_list}")
            return False
            
        else:
            print(f"\n❌ Registration failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to Django server")
        print("💡 Make sure Django is running:")
        print("   python manage.py runserver")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def explain_celery_integration():
    """Explain how Celery integration works"""
    print("\n" + "="*60)
    print("  HOW CELERY INTEGRATION WORKS")
    print("="*60)
    
    print("\n📋 The Complete Flow:")
    print("   1. User submits registration form")
    print("   2. Django API validates data")
    print("   3. User account created in database") 
    print("   4. Authentication token generated")
    print("   5. Background task queued: send_welcome_email.delay(user_id)")
    print("   6. Django returns immediate response (fast!)")
    print("   7. Celery worker picks up task from Redis queue")
    print("   8. Email sent in background (slow operation)")
    
    print("\n🏗️ Key Components:")
    print("   • Redis: Message broker (task queue)")
    print("   • Celery Worker: Background task processor") 
    print("   • Django: Web application (fast responses)")
    print("   • Email Service: SMTP for sending emails")
    
    print("\n⚡ Benefits of This Architecture:")
    print("   ✅ Fast API responses (no waiting for email)")
    print("   ✅ Reliable email delivery (retry on failure)")
    print("   ✅ Scalable (multiple workers)")
    print("   ✅ Fault tolerant (tasks survive crashes)")
    print("   ✅ Monitoring and debugging tools")
    
    print("\n📁 Code Files:")
    print("   • api/views.py - Registration endpoint with Celery integration")
    print("   • api/tasks.py - Background task definitions")
    print("   • django_internship/celery.py - Celery configuration")
    print("   • django_internship/settings.py - Redis/Celery settings")

def show_email_template():
    """Show what the welcome email looks like"""
    print("\n" + "="*60)
    print("  WELCOME EMAIL TEMPLATE")
    print("="*60)
    
    print("\n📧 Email Preview (HTML version):")
    print("-" * 40)
    
    email_html = """
    <html>
    <body>
        <h2>Welcome to Django Internship API!</h2>
        <p>Hello <strong>testuser_123456</strong>!</p>
        
        <p>Welcome to our Django Internship API platform. Your account has been successfully created.</p>
        
        <h3>What you can do now:</h3>
        <ul>
            <li>Access protected endpoints using your authentication token</li>
            <li>View your profile at <code>/api/profile/</code></li>
            <li>Explore the API documentation</li>
        </ul>
        
        <h3>Account Details:</h3>
        <ul>
            <li><strong>Username:</strong> testuser_123456</li>
            <li><strong>Email:</strong> testuser@example.com</li>
            <li><strong>Registration Date:</strong> 2025-06-26 14:30:15</li>
        </ul>
        
        <p>Best regards,<br>Django Internship Team</p>
    </body>
    </html>
    """
    
    print(email_html)
    
    print("\n📧 Email Preview (Text version):")
    print("-" * 40)
    
    email_text = """
    Hello testuser_123456!
    
    Welcome to our Django Internship API platform. Your account has been successfully created.
    
    Here's what you can do now:
    - Access protected endpoints using your authentication token
    - View your profile at /api/profile/
    - Explore the API documentation
    
    Account Details:
    - Username: testuser_123456
    - Email: testuser@example.com
    - Registration Date: 2025-06-26 14:30:15
    
    Best regards,
    Django Internship Team
    """
    
    print(email_text)

def main():
    """Main function"""
    # Test registration
    success = test_user_registration_celery()
    
    # Explain how it works
    explain_celery_integration()
    
    # Show email template
    show_email_template()
    
    print("\n" + "="*60)
    print("  NEXT STEPS")
    print("="*60)
    
    if success:
        print("\n✅ Registration test completed successfully!")
        print("\n🚀 To see background email processing:")
        print("   1. Install Redis (see REDIS_INSTALLATION_GUIDE.md)")
        print("   2. Start Redis server")
        print("   3. Start Celery worker: celery -A django_internship worker --loglevel=info")
        print("   4. Register another user and watch the Celery logs")
        
        print("\n📊 Advanced features to try:")
        print("   • Run: python complete_celery_demo.py (full demo)")
        print("   • Check Django admin for API logs")
        print("   • Try other background tasks (analytics, reports)")
        print("   • Set up Flower monitoring: pip install flower")
    else:
        print("\n❌ Registration test failed")
        print("💡 Make sure Django server is running: python manage.py runserver")
    
    print("\n📚 Documentation:")
    print("   • CELERY_INTEGRATION_GUIDE.md - Complete setup guide")
    print("   • CELERY_QUICK_START.md - 5-minute quick start")
    print("   • REDIS_INSTALLATION_GUIDE.md - Redis setup")

if __name__ == "__main__":
    main()
