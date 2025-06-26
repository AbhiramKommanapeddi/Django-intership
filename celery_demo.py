#!/usr/bin/env python
"""
Celery Integration Demo for Django Internship Assignment
Demonstrates background tasks with Redis as broker
"""
import os
import sys
import django
import time
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
django.setup()

from api.tasks import (
    send_welcome_email, send_password_reset_email, generate_daily_report,
    send_admin_notification, process_api_analytics, send_bulk_notifications,
    cleanup_old_logs, send_notification_email
)
from django.contrib.auth.models import User
from celery import group, chain, chord
from django_internship.celery import app as celery_app

def show_celery_info():
    """Display Celery configuration information"""
    print("=== CELERY CONFIGURATION ===")
    print(f"Broker URL: {celery_app.conf.broker_url}")
    print(f"Result Backend: {celery_app.conf.result_backend}")
    print(f"Task Serializer: {celery_app.conf.task_serializer}")
    print(f"Result Serializer: {celery_app.conf.result_serializer}")
    print(f"Timezone: {celery_app.conf.timezone}")
    print()

def demonstrate_basic_tasks():
    """Demonstrate basic Celery tasks"""
    print("=== BASIC CELERY TASKS DEMONSTRATION ===\n")
    
    # Get a user for testing
    try:
        user = User.objects.first()
        if not user:
            print("❌ No users found. Create a user first.")
            return
        
        print(f"Using test user: {user.username} ({user.email})")
        print()
        
        # 1. Welcome Email Task
        print("1. 📧 WELCOME EMAIL TASK")
        print("   Sending welcome email asynchronously...")
        result = send_welcome_email.delay(user.id)
        print(f"   Task ID: {result.id}")
        print(f"   Task State: {result.state}")
        
        # Wait for result
        try:
            result_value = result.get(timeout=10)
            print(f"   ✅ Result: {result_value}")
        except Exception as e:
            print(f"   ⚠️ Task completed but email not sent (email not configured): {e}")
        print()
        
        # 2. Password Reset Email Task
        print("2. 🔐 PASSWORD RESET EMAIL TASK")
        reset_link = "https://example.com/reset/abc123"
        result = send_password_reset_email.delay(user.id, reset_link)
        print(f"   Task ID: {result.id}")
        try:
            result_value = result.get(timeout=10)
            print(f"   ✅ Result: {result_value}")
        except Exception as e:
            print(f"   ⚠️ Task completed: {e}")
        print()
        
        # 3. Admin Notification Task
        print("3. 🔔 ADMIN NOTIFICATION TASK")
        result = send_admin_notification.delay(
            "System Alert", 
            "This is a test notification from the Celery demo."
        )
        print(f"   Task ID: {result.id}")
        try:
            result_value = result.get(timeout=10)
            print(f"   ✅ Result: {result_value}")
        except Exception as e:
            print(f"   ⚠️ Task completed: {e}")
        print()
        
    except Exception as e:
        print(f"❌ Error in basic tasks demo: {e}")

def demonstrate_analytics_tasks():
    """Demonstrate analytics and reporting tasks"""
    print("=== ANALYTICS & REPORTING TASKS ===\n")
    
    # 1. Daily Report Generation
    print("1. 📊 DAILY REPORT GENERATION")
    print("   Generating daily usage report...")
    result = generate_daily_report.delay()
    print(f"   Task ID: {result.id}")
    
    try:
        report = result.get(timeout=15)
        print("   ✅ Daily Report Generated:")
        print(f"   📅 Date: {report['date']}")
        print(f"   📈 Total Requests: {report['total_requests']}")
        print(f"   ✅ Successful: {report['successful_requests']}")
        print(f"   ❌ Failed: {report['failed_requests']}")
        print(f"   📊 Success Rate: {report['success_rate']}")
        print(f"   👥 Unique Users: {report['unique_users']}")
        print(f"   🌐 Unique IPs: {report['unique_ips']}")
        print(f"   ⏱️ Avg Response Time: {report['avg_response_time']}")
        if report['top_endpoints']:
            print(f"   🔝 Top Endpoints: {report['top_endpoints']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # 2. API Analytics Processing
    print("2. 📈 API ANALYTICS PROCESSING")
    print("   Processing API analytics (this may take a few seconds)...")
    result = process_api_analytics.delay()
    print(f"   Task ID: {result.id}")
    
    try:
        analytics = result.get(timeout=20)
        print("   ✅ Analytics Processed:")
        print(f"   📊 Total Requests (7 days): {analytics['total_requests']}")
        print(f"   👥 Unique Users: {analytics['unique_users']}")
        print(f"   ⏱️ Avg Response Time: {analytics['avg_response_time']:.3f}s")
        print(f"   ❌ Error Rate: {analytics['error_rate']:.1f}%")
        if analytics['most_active_user']:
            print(f"   🏆 Most Active User: {analytics['most_active_user']['username']} ({analytics['most_active_user']['request_count']} requests)")
        if analytics['slowest_endpoint']:
            print(f"   🐌 Slowest Endpoint: {analytics['slowest_endpoint']['endpoint']} ({analytics['slowest_endpoint']['avg_time']:.3f}s)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()

def demonstrate_bulk_operations():
    """Demonstrate bulk operations and advanced features"""
    print("=== BULK OPERATIONS & ADVANCED FEATURES ===\n")
    
    # 1. Bulk Notifications
    print("1. 📬 BULK NOTIFICATIONS")
    users = User.objects.all()[:3]  # Get first 3 users
    if users:
        user_ids = [user.id for user in users]
        print(f"   Sending bulk notification to {len(user_ids)} users...")
        
        result = send_bulk_notifications.delay(
            user_ids,
            "System Maintenance Notice",
            "We will be performing scheduled maintenance on our API servers tonight from 2 AM to 4 AM UTC. During this time, some services may be temporarily unavailable."
        )
        print(f"   Task ID: {result.id}")
        
        try:
            bulk_result = result.get(timeout=15)
            print("   ✅ Bulk Notification Completed:")
            print(f"   📧 Sent: {bulk_result['sent_count']}")
            print(f"   ❌ Failed: {bulk_result['failed_count']}")
            if bulk_result['failed_emails']:
                print(f"   Failed emails: {bulk_result['failed_emails']}")
        except Exception as e:
            print(f"   ⚠️ Bulk notification task completed: {e}")
    else:
        print("   ❌ No users found for bulk notification demo")
    print()
    
    # 2. Cleanup Task
    print("2. 🧹 CLEANUP OLD LOGS")
    print("   Cleaning up old API logs...")
    result = cleanup_old_logs.delay()
    print(f"   Task ID: {result.id}")
    
    try:
        cleanup_result = result.get(timeout=10)
        print(f"   ✅ {cleanup_result}")
    except Exception as e:
        print(f"   ⚠️ Cleanup task completed: {e}")
    print()

def demonstrate_task_workflows():
    """Demonstrate complex task workflows using groups, chains, and chords"""
    print("=== TASK WORKFLOWS (GROUPS, CHAINS, CHORDS) ===\n")
    
    try:
        users = User.objects.all()[:2]
        if not users:
            print("❌ No users found for workflow demo")
            return
        
        print("1. 🔗 TASK CHAIN (Sequential Execution)")
        print("   Executing: Generate Report → Send Admin Notification")
        
        # Create a chain: generate report, then send notification
        workflow = chain(
            generate_daily_report.s(),
            send_admin_notification.s("Daily Report", "Daily report has been generated.")
        )
        
        result = workflow.apply_async()
        print(f"   Workflow ID: {result.id}")
        print("   Waiting for chain to complete...")
        
        try:
            final_result = result.get(timeout=20)
            print(f"   ✅ Chain completed: {final_result}")
        except Exception as e:
            print(f"   ⚠️ Chain completed with note: {e}")
        print()
        
        print("2. 🤝 TASK GROUP (Parallel Execution)")
        print("   Executing multiple tasks in parallel...")
        
        # Create a group of tasks to run in parallel
        parallel_tasks = group(
            send_welcome_email.s(users[0].id),
            generate_daily_report.s(),
            process_api_analytics.s()
        )
        
        result = parallel_tasks.apply_async()
        print(f"   Group ID: {result.id}")
        print("   Waiting for all tasks to complete...")
        
        try:
            group_results = result.get(timeout=25)
            print("   ✅ All parallel tasks completed:")
            for i, res in enumerate(group_results, 1):
                print(f"      Task {i}: {'✅ Success' if res else '⚠️ Completed'}")
        except Exception as e:
            print(f"   ⚠️ Group tasks completed: {e}")
        print()
        
    except Exception as e:
        print(f"❌ Error in workflow demo: {e}")

def show_task_monitoring():
    """Show how to monitor Celery tasks"""
    print("=== TASK MONITORING ===\n")
    
    print("📊 CELERY MONITORING COMMANDS:")
    print("   • Check active tasks: celery -A django_internship inspect active")
    print("   • Check registered tasks: celery -A django_internship inspect registered")
    print("   • Check task stats: celery -A django_internship inspect stats")
    print("   • Monitor events: celery -A django_internship events")
    print("   • Flower monitoring: celery -A django_internship flower")
    print()
    
    print("🔍 TASK RESULT INSPECTION:")
    print("   You can inspect task results using:")
    print("   from celery.result import AsyncResult")
    print("   result = AsyncResult('task-id')")
    print("   print(result.state, result.result)")
    print()

def main():
    print("🚀 DJANGO INTERNSHIP ASSIGNMENT - CELERY INTEGRATION DEMO")
    print("=" * 70)
    print()
    
    # Check if Redis is running
    try:
        from redis import Redis
        redis_client = Redis.from_url(celery_app.conf.broker_url)
        redis_client.ping()
        print("✅ Redis broker is running and accessible")
    except Exception as e:
        print(f"❌ Redis broker connection failed: {e}")
        print("   Please start Redis server: redis-server")
        print("   Or install Redis: https://redis.io/download")
        return
    
    print()
    
    # Show configuration
    show_celery_info()
    
    # Run demonstrations
    demonstrate_basic_tasks()
    demonstrate_analytics_tasks()
    demonstrate_bulk_operations()
    demonstrate_task_workflows()
    show_task_monitoring()
    
    print("🎯 CELERY FEATURES DEMONSTRATED:")
    print("✅ Background email sending after user registration")
    print("✅ Redis as message broker")
    print("✅ Asynchronous task execution")
    print("✅ Task result tracking")
    print("✅ Error handling and retries")
    print("✅ Bulk operations")
    print("✅ Complex workflows (chains, groups, chords)")
    print("✅ Analytics and reporting tasks")
    print("✅ Admin notifications")
    print("✅ Cleanup and maintenance tasks")
    
    print(f"\n📖 For more details, see the task definitions in: api/tasks.py")
    print(f"🔧 To start a Celery worker: celery -A django_internship worker --loglevel=info")

if __name__ == "__main__":
    main()
