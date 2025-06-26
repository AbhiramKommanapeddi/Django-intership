#!/usr/bin/env python
"""
Django Admin ChangeAddDeleteView Demo for API Logs
Demonstrates the admin interface functionality
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
from datetime import datetime, timedelta
import random

def demonstrate_admin_functionality():
    print("=== DJANGO ADMIN ChangeAddDeleteView DEMONSTRATION ===\n")
    
    print("🔧 Current API Log Statistics:")
    total_logs = ApiLog.objects.count()
    print(f"   Total logs in database: {total_logs}")
    
    if total_logs > 0:
        latest_log = ApiLog.objects.latest('timestamp')
        oldest_log = ApiLog.objects.earliest('timestamp')
        print(f"   Latest log: {latest_log.timestamp}")
        print(f"   Oldest log: {oldest_log.timestamp}")
        
        # Status distribution
        statuses = {}
        for log in ApiLog.objects.all():
            status = log.response_status
            statuses[status] = statuses.get(status, 0) + 1
        
        print("\n📊 Status Code Distribution:")
        for status, count in sorted(statuses.items()):
            status_name = {
                200: "OK", 201: "Created", 400: "Bad Request",
                401: "Unauthorized", 403: "Forbidden", 404: "Not Found",
                500: "Internal Server Error"
            }.get(status, "Unknown")
            percentage = (count / total_logs) * 100
            print(f"   {status} ({status_name}): {count} logs ({percentage:.1f}%)")
    
    print("\n🌐 Django Admin Interface Features:")
    print("   📍 URL: http://localhost:8000/admin/api/apilog/")
    print("   👤 Login: admin / admin123")
    print()
    
    print("📋 CHANGE VIEW Features:")
    print("   ✅ View individual log details")
    print("   ✅ Read-only access (cannot modify logs)")
    print("   ✅ Organized fieldsets for better readability")
    print("   ✅ Color-coded status indicators")
    print("   ✅ Formatted response times")
    print()
    
    print("➕ ADD VIEW Features:")
    print("   ❌ Add functionality disabled")
    print("   ℹ️  Logs are created automatically by the system")
    print("   🔒 Prevents manual log tampering")
    print()
    
    print("🗑️ DELETE VIEW Features:")
    print("   ⚠️  Only superusers can delete logs")
    print("   ✅ Bulk delete operations available")
    print("   🔐 Confirmation required for deletions")
    print("   📝 Maintains data integrity")
    print()
    
    print("📊 LIST VIEW Features:")
    print("   🔍 Filter by: method, status, date, user")
    print("   🔎 Search by: endpoint, username, IP address")
    print("   📈 Sort by: timestamp, response time, status")
    print("   📄 Pagination: 25 logs per page")
    print("   🎨 Color coding for different status types")
    print("   📅 Date hierarchy navigation")

def show_sample_log_entries():
    print("\n=== SAMPLE LOG ENTRIES IN ADMIN ===")
    
    logs = ApiLog.objects.all().order_by('-timestamp')[:5]
    
    if not logs:
        print("No logs found. Make some API requests first.")
        return
    
    print("Recent logs as they appear in Django Admin:\n")
    
    for i, log in enumerate(logs, 1):
        user_display = f"{log.user.username}" if log.user else "Anonymous"
        status_color = "🟢" if 200 <= log.response_status < 300 else "🔴" if log.response_status >= 400 else "🟡"
        response_time_ms = log.response_time * 1000
        
        print(f"#{i} {status_color} {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"    Endpoint: {log.endpoint}")
        print(f"    Method: {log.method}")
        print(f"    User: {user_display}")
        print(f"    IP: {log.ip_address}")
        print(f"    Status: {log.response_status}")
        print(f"    Time: {response_time_ms:.1f}ms")
        print("-" * 50)

def admin_permissions_demo():
    print("\n=== ADMIN PERMISSIONS DEMONSTRATION ===")
    
    print("🔐 Permission Levels:")
    print("   👑 Superuser (admin):")
    print("      ✅ View all logs")
    print("      ✅ Filter and search logs") 
    print("      ✅ Export logs to CSV")
    print("      ❌ Cannot add new logs")
    print("      ❌ Cannot modify existing logs")
    print("      ⚠️  Can delete logs (with confirmation)")
    print()
    
    print("   👤 Staff User:")
    print("      ✅ View all logs")
    print("      ✅ Filter and search logs")
    print("      ❌ Cannot add new logs")
    print("      ❌ Cannot modify existing logs")
    print("      ❌ Cannot delete logs")
    print()
    
    print("   🚫 Regular User:")
    print("      ❌ No admin access")
    print("      ℹ️  Can access logs via API endpoint if admin")

def main():
    print("🚀 DJANGO INTERNSHIP ASSIGNMENT")
    print("📊 API Logging & Django Admin ChangeAddDeleteView Demo")
    print("=" * 60)
    
    demonstrate_admin_functionality()
    show_sample_log_entries()
    admin_permissions_demo()
    
    print("\n🎯 KEY CONCEPTS DEMONSTRATED:")
    print("✅ Automatic API request logging")
    print("✅ Django Admin ChangeAddDeleteView functionality")
    print("✅ Read-only log management")
    print("✅ Comprehensive filtering and search")
    print("✅ Permission-based access control")
    print("✅ Production-ready logging system")
    
    print(f"\n📖 For detailed documentation, see: API_LOGGING_GUIDE.md")
    print(f"🌐 Access the admin interface at: http://localhost:8000/admin/api/apilog/")

if __name__ == "__main__":
    main()
