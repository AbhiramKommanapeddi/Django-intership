#!/usr/bin/env python
"""
Script to create a superuser for Django admin
"""
import os
import django
from django.core.management.base import BaseCommand

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Create a superuser if it doesn't exist"""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    if User.objects.filter(username=username).exists():
        print(f"❌ Superuser '{username}' already exists!")
        print("ℹ️  Try these alternatives:")
        print("   • Use 'djangoadmin' as username")
        print("   • Use 'superuser' as username") 
        print("   • Use your name as username")
        return False
    
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser created successfully!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"\n🔗 Login at: http://127.0.0.1:8000/admin/")
        return True
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Django Superuser Creation Script")
    print("="*40)
    create_superuser()
