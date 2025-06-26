#!/usr/bin/env python
"""
Simple script to create admin user and show login credentials
"""
import os
import sys
import django

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    """Create or update admin user"""
    
    print("🔧 Django Admin User Setup")
    print("=" * 30)
    
    # Admin credentials
    username = 'abhikadmin'
    password = 'admin123'
    email = 'admin@example.com'
    
    try:
        # Check if user exists
        if User.objects.filter(username=username).exists():
            print(f"📝 User '{username}' already exists, updating...")
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            print(f"✅ Updated user '{username}' to admin")
        else:
            print(f"👤 Creating new admin user '{username}'...")
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"✅ Created new admin user '{username}'")
        
        print("\n🔑 Django Admin Login Credentials:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   Admin URL: http://127.0.0.1:8000/admin/")
        
        print("\n📋 Instructions:")
        print("1. Go to: http://127.0.0.1:8000/admin/")
        print("2. Enter the username and password above")
        print("3. You'll have full admin access!")
        
        # Also show existing users
        print("\n👥 All users in database:")
        all_users = User.objects.all()
        for u in all_users:
            admin_status = "Admin" if u.is_superuser else "Regular"
            print(f"   • {u.username} ({admin_status})")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_admin()
