#!/usr/bin/env python
"""
Quick setup script for Django Internship Assignment
This script helps set up the project quickly for development and testing
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and print the result."""
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"{'='*50}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success!")
            if result.stdout:
                print(f"Output: {result.stdout}")
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    return True

def setup_project():
    """Set up the Django project for development."""
    print("🚀 Django Internship Assignment - Quick Setup")
    print("This script will set up your Django project for development\n")
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        return False
    
    # Step 1: Create virtual environment (if not exists)
    if not Path("venv").exists():
        print("📦 Creating virtual environment...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Step 2: Install dependencies
    print("\n📦 Installing dependencies...")
    activate_cmd = "venv\\Scripts\\activate" if os.name == 'nt' else "source venv/bin/activate"
    pip_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    
    if not run_command(pip_cmd, "Installing Python packages"):
        return False
    
    # Step 3: Setup environment file
    if not Path(".env").exists():
        print("\n⚙️ Setting up environment file...")
        import shutil
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from .env.example")
        print("📝 You can edit .env to configure your settings")
    else:
        print("✅ .env file already exists")
    
    # Step 4: Run migrations
    print("\n🗄️ Setting up database...")
    migrate_cmd = f"{activate_cmd} && python manage.py migrate"
    if not run_command(migrate_cmd, "Running database migrations"):
        return False
    
    # Step 5: Collect static files
    print("\n📂 Collecting static files...")
    static_cmd = f"{activate_cmd} && python manage.py collectstatic --noinput"
    run_command(static_cmd, "Collecting static files")
    
    # Setup summary
    print(f"\n{'='*60}")
    print("  🎉 SETUP COMPLETE!")
    print(f"{'='*60}")
    
    print("\n✅ Your Django Internship Assignment is ready!")
    print("\n📋 Next Steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Start the Django server: python manage.py runserver")
    print("3. Test the API: python test_api.py")
    print("4. Optional: Configure Telegram bot token in .env")
    print("5. Optional: Start Redis and Celery worker")
    
    print("\n🔗 Important URLs:")
    print("  • API Root: http://localhost:8000/")
    print("  • Public API: http://localhost:8000/api/public/")
    print("  • Admin Panel: http://localhost:8000/admin/")
    
    print("\n📚 Documentation:")
    print("  • Check README.md for detailed instructions")
    print("  • API endpoints documented in README.md")
    print("  • Use VS Code tasks for easy development")
    
    # Ask if user wants to create superuser
    create_superuser = input("\n❓ Would you like to create a superuser now? (y/n): ").lower().strip()
    if create_superuser == 'y':
        superuser_cmd = f"{activate_cmd} && python manage.py createsuperuser"
        run_command(superuser_cmd, "Creating superuser")
    
    # Ask if user wants to start the server
    start_server = input("\n❓ Would you like to start the Django server now? (y/n): ").lower().strip()
    if start_server == 'y':
        print("\n🚀 Starting Django development server...")
        print("📝 Open another terminal to run additional services (Celery, Telegram bot)")
        print("🛑 Press Ctrl+C to stop the server")
        
        server_cmd = f"{activate_cmd} && python manage.py runserver"
        os.system(server_cmd)
    
    return True

if __name__ == "__main__":
    print("Django Internship Assignment - Quick Setup Script")
    print("This will set up your development environment\n")
    
    try:
        success = setup_project()
        if success:
            print("\n🎯 Setup completed successfully!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
    except KeyboardInterrupt:
        print("\n\n🛑 Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    input("\nPress Enter to exit...")
