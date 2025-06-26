#!/usr/bin/env python
"""
Complete Celery Integration Demo for Django Internship Project

This script demonstrates:
1. User registration with automatic welcome email
2. Background task execution
3. Task chaining and grouping
4. Real-time task monitoring
5. Error handling and retries
"""
import requests
import json
import time
import sys
import os

# Add Django project to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:8000"

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_step(step_num, description):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 40)

def test_redis_connection():
    """Test if Redis is running"""
    print_header("TESTING REDIS CONNECTION")
    
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        result = r.ping()
        if result:
            print("✅ Redis is running and accessible!")
            print(f"   Redis info: {r.info('server')['redis_version']}")
            return True
        else:
            print("❌ Redis ping failed")
            return False
    except Exception as e:
        print(f"❌ Redis connection failed: {str(e)}")
        print("\n💡 To fix this:")
        print("   1. Install Redis (see REDIS_INSTALLATION_GUIDE.md)")
        print("   2. Start Redis server")
        print("   3. Run this script again")
        return False

def test_celery_worker():
    """Test if Celery worker is running"""
    print_header("TESTING CELERY WORKER")
    
    try:
        # Try to import Celery and check worker status
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
        import django
        django.setup()
        
        from django_internship.celery import app
        
        # Check active nodes
        inspect = app.control.inspect()
        stats = inspect.stats()
        
        if stats:
            print("✅ Celery worker is running!")
            for node, stat in stats.items():
                print(f"   Node: {node}")
                print(f"   Pool: {stat.get('pool', {}).get('implementation', 'N/A')}")
                print(f"   Processes: {stat.get('pool', {}).get('processes', 'N/A')}")
            return True
        else:
            print("❌ No Celery workers found")
            print("\n💡 To fix this:")
            print("   1. Open a new terminal")
            print("   2. Navigate to project directory")
            print("   3. Run: celery -A django_internship worker --loglevel=info")
            print("   4. Keep that terminal open and run this script again")
            return False
            
    except Exception as e:
        print(f"❌ Celery check failed: {str(e)}")
        return False

def demo_user_registration_with_email():
    """Demo user registration that triggers welcome email"""
    print_header("DEMO: USER REGISTRATION WITH WELCOME EMAIL")
    
    # Create unique test user
    timestamp = int(time.time())
    test_user = {
        "username": f"celery_demo_{timestamp}",
        "email": "demo@example.com",
        "password": "demo123password",
        "password_confirm": "demo123password",
        "first_name": "Celery",
        "last_name": "Demo"
    }
    
    print_step(1, "Registering new user")
    print(f"Username: {test_user['username']}")
    print(f"Email: {test_user['email']}")
    
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=test_user)
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Token: {data.get('token', 'N/A')[:20]}...")
            print(f"   Background Email: {data.get('email_sent')}")
            
            print_step(2, "What happened in the background")
            print("✅ User account created in database")
            print("✅ Authentication token generated")
            print("✅ Welcome email task queued in Celery")
            print("✅ Task will be processed by Celery worker")
            
            return data.get('user_id'), data.get('token')
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None, None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server")
        print("💡 Make sure Django is running: python manage.py runserver")
        return None, None
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return None, None

def demo_background_tasks():
    """Demo various background tasks"""
    print_header("DEMO: BACKGROUND TASKS")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
        import django
        django.setup()
        
        from api.tasks import (
            generate_daily_report,
            process_api_analytics,
            cleanup_old_logs,
            send_admin_notification
        )
        
        print_step(1, "Triggering daily report generation")
        task1 = generate_daily_report.delay()
        print(f"   Task ID: {task1.id}")
        print("   Status: Task queued for background processing")
        
        print_step(2, "Triggering API analytics processing")
        task2 = process_api_analytics.delay()
        print(f"   Task ID: {task2.id}")
        print("   Status: Heavy analytics task queued")
        
        print_step(3, "Triggering admin notification")
        task3 = send_admin_notification.delay(
            "Demo Notification", 
            "This is a demo notification from Celery integration test."
        )
        print(f"   Task ID: {task3.id}")
        print("   Status: Admin notification queued")
        
        print_step(4, "Monitoring task progress")
        tasks = [task1, task2, task3]
        
        for i, task in enumerate(tasks, 1):
            print(f"   Task {i} ({task.id[:8]}...): ", end="")
            
            # Wait a bit for task to process
            timeout = 10
            start_time = time.time()
            
            while task.status == 'PENDING' and (time.time() - start_time) < timeout:
                time.sleep(0.5)
            
            if task.status == 'SUCCESS':
                print("✅ COMPLETED")
                if task.result:
                    print(f"      Result: {str(task.result)[:100]}...")
            elif task.status == 'FAILURE':
                print("❌ FAILED")
                print(f"      Error: {task.result}")
            else:
                print(f"⏳ {task.status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Background tasks demo failed: {str(e)}")
        return False

def demo_task_chaining():
    """Demo task chaining and grouping"""
    print_header("DEMO: ADVANCED CELERY FEATURES")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
        import django
        django.setup()
        
        from celery import chain, group, chord
        from api.tasks import generate_daily_report, process_api_analytics
        
        print_step(1, "Creating task chain")
        print("   Chain: Daily Report → Analytics Processing")
        
        # Create a chain of tasks
        task_chain = chain(
            generate_daily_report.s(),
            process_api_analytics.s()
        )
        
        result = task_chain.apply_async()
        print(f"   Chain ID: {result.id}")
        
        print_step(2, "Creating task group")
        print("   Group: Multiple analytics tasks in parallel")
        
        # Create a group of parallel tasks
        task_group = group(
            generate_daily_report.s(),
            process_api_analytics.s(),
            generate_daily_report.s()
        )
        
        group_result = task_group.apply_async()
        print(f"   Group ID: {group_result.id}")
        print(f"   Parallel tasks: {len(group_result.children)}")
        
        print_step(3, "Monitoring advanced task execution")
        print("   Waiting for tasks to complete...")
        
        # Monitor chain
        timeout = 15
        start_time = time.time()
        while not result.ready() and (time.time() - start_time) < timeout:
            time.sleep(1)
            print("   Chain progress: ⏳ Processing...")
        
        if result.ready():
            if result.successful():
                print("   Chain result: ✅ COMPLETED")
            else:
                print("   Chain result: ❌ FAILED")
        else:
            print("   Chain result: ⏳ TIMEOUT")
        
        # Monitor group
        start_time = time.time()
        while not group_result.ready() and (time.time() - start_time) < timeout:
            time.sleep(1)
            completed = sum(1 for child in group_result.children if child.ready())
            print(f"   Group progress: {completed}/{len(group_result.children)} tasks completed")
        
        if group_result.ready():
            print("   Group result: ✅ ALL COMPLETED")
        else:
            print("   Group result: ⏳ TIMEOUT")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced features demo failed: {str(e)}")
        return False

def demo_task_monitoring():
    """Demo task monitoring and status checking"""
    print_header("DEMO: TASK MONITORING")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
        import django
        django.setup()
        
        from django_internship.celery import app
        from api.tasks import generate_daily_report
        
        print_step(1, "Getting Celery worker statistics")
        
        inspect = app.control.inspect()
        
        # Active tasks
        active = inspect.active()
        if active:
            print("📊 Active tasks:")
            for worker, tasks in active.items():
                print(f"   Worker {worker}: {len(tasks)} active tasks")
        else:
            print("📊 No active tasks currently")
        
        # Scheduled tasks
        scheduled = inspect.scheduled()
        if scheduled:
            print("📅 Scheduled tasks:")
            for worker, tasks in scheduled.items():
                print(f"   Worker {worker}: {len(tasks)} scheduled tasks")
        else:
            print("📅 No scheduled tasks")
        
        # Reserved tasks
        reserved = inspect.reserved()
        if reserved:
            print("📋 Reserved tasks:")
            for worker, tasks in reserved.items():
                print(f"   Worker {worker}: {len(tasks)} reserved tasks")
        else:
            print("📋 No reserved tasks")
        
        print_step(2, "Creating and monitoring a test task")
        
        task = generate_daily_report.delay()
        print(f"   Task created: {task.id}")
        
        # Monitor task states
        states = []
        for _ in range(10):
            state = task.status
            if state not in states:
                states.append(state)
                print(f"   Task state: {state}")
            
            if state in ['SUCCESS', 'FAILURE', 'REVOKED']:
                break
            time.sleep(0.5)
        
        if task.ready():
            if task.successful():
                print(f"   Final result: ✅ {str(task.result)[:100]}...")
            else:
                print(f"   Final result: ❌ {task.result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Task monitoring demo failed: {str(e)}")
        return False

def print_summary():
    """Print summary and next steps"""
    print_header("CELERY INTEGRATION SUMMARY")
    
    print("🎯 What you've learned:")
    print("   ✅ Celery setup with Redis broker")
    print("   ✅ Background task execution")
    print("   ✅ Automatic email sending after registration")
    print("   ✅ Task chaining and grouping")
    print("   ✅ Real-time task monitoring")
    print("   ✅ Error handling and retries")
    
    print("\n📁 Key files in your project:")
    print("   • django_internship/celery.py - Celery configuration")
    print("   • api/tasks.py - Background task definitions")
    print("   • api/views.py - Integration with registration")
    print("   • django_internship/settings.py - Redis/Celery settings")
    
    print("\n🚀 Production considerations:")
    print("   • Use Redis Cluster for high availability")
    print("   • Monitor tasks with Flower: pip install flower")
    print("   • Set up task routing for different queues")
    print("   • Implement proper error handling and logging")
    print("   • Use Celery Beat for scheduled tasks")
    
    print("\n📖 Learn more:")
    print("   • Celery documentation: https://docs.celeryproject.org/")
    print("   • Django-Celery integration: https://docs.celeryproject.org/en/stable/django/")
    print("   • Redis documentation: https://redis.io/documentation")

def main():
    """Main demo function"""
    print_header("CELERY INTEGRATION COMPLETE DEMO")
    print("This demo will test your complete Celery setup with Redis broker")
    print("and demonstrate background task execution.")
    
    # Check prerequisites
    if not test_redis_connection():
        return
    
    if not test_celery_worker():
        return
    
    print("\n🎉 All prerequisites met! Starting comprehensive demo...")
    
    # Demo user registration
    user_id, token = demo_user_registration_with_email()
    
    if user_id:
        # Demo background tasks
        demo_background_tasks()
        
        # Demo advanced features
        demo_task_chaining()
        
        # Demo monitoring
        demo_task_monitoring()
        
        # Print summary
        print_summary()
        
        print(f"\n✅ Demo completed successfully!")
        print(f"   Test user created: ID {user_id}")
        print(f"   Check your Django admin for API logs and user data")
    else:
        print("\n❌ Demo could not complete due to registration failure")

if __name__ == "__main__":
    main()
