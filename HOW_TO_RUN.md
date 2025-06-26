# 🚀 How to Run Django Internship Assignment

## Quick Start (Recommended)

### 1. Automated Setup

```bash
# Run the automated setup script
python setup.py
```

This will handle virtual environment, dependencies, database setup, and give you options to create superuser and start the server.

---

## Manual Setup (Step by Step)

### Prerequisites

- Python 3.8+ installed
- Git (for cloning)
- Redis server (optional, for Celery)

### Step 1: Project Setup

```bash
# Navigate to project directory
cd "c:\Users\abhik\Downloads\Django intership"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
source venv/Scripts/activate
# On Linux/Mac: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings (optional for basic testing)
# The project works with default SQLite database
```

### Step 3: Database Setup

```bash
# Run database migrations
python manage.py migrate

# Create admin user (optional but recommended)
python manage.py createsuperuser
```

### Step 4: Start the Server

```bash
# Start Django development server
python manage.py runserver
```

**✅ Your server is now running at: http://127.0.0.1:8000/**

---

## 🎯 Testing the API

### Quick API Test

```bash
# Run automated test script
python test_api.py

# Or test manually:
# Test public endpoint
curl http://127.0.0.1:8000/api/public/

# Test root endpoint
curl http://127.0.0.1:8000/
```

### Register and Login Flow

```bash
# 1. Register a new user
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password_confirm":"testpass123"}'

# 2. Login to get token
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# 3. Use token for protected endpoint
curl -H "Authorization: Token YOUR_TOKEN_HERE" http://127.0.0.1:8000/api/protected/
```

---

## 🔧 Optional Services

### Start Celery Worker (Background Tasks)

```bash
# Open new terminal, activate venv, then:
celery -A django_internship worker --loglevel=info
```

### Start Telegram Bot

```bash
# 1. Get bot token from @BotFather on Telegram
# 2. Add token to .env file: TELEGRAM_BOT_TOKEN=your-token
# 3. Start bot in new terminal:
python manage.py run_telegram_bot
```

### Start Redis (for Celery)

```bash
# Windows (if Redis installed):
redis-server

# Linux/Mac:
sudo systemctl start redis
# or
redis-server
```

---

## 📱 VS Code Integration

### Using VS Code Tasks

1. Open project in VS Code
2. Press `Ctrl+Shift+P`
3. Type "Tasks: Run Task"
4. Choose from available tasks:
   - **Django Internship - Run Server**
   - **Django Internship - Run Celery Worker**
   - **Django Internship - Run Telegram Bot**
   - **Django Internship - Test API**
   - **Django Internship - Create Superuser**

---

## 🌐 Available Endpoints

| Endpoint          | Method  | Auth    | Description            |
| ----------------- | ------- | ------- | ---------------------- |
| `/`               | GET     | No      | Root information       |
| `/api/public/`    | GET     | No      | **Public endpoint**    |
| `/api/register/`  | POST    | No      | User registration      |
| `/api/login/`     | POST    | No      | User login             |
| `/api/protected/` | GET     | Token   | **Protected endpoint** |
| `/api/profile/`   | GET/PUT | Token   | User profile           |
| `/api/logs/`      | GET     | Admin   | API logs               |
| `/admin/`         | ALL     | Session | Django admin           |

---

## 🔍 Troubleshooting

### Common Issues

**1. Module not found errors:**

```bash
# Make sure virtual environment is activated
source venv/Scripts/activate
pip install -r requirements.txt
```

**2. Database errors:**

```bash
# Reset database
python manage.py migrate
```

**3. Port already in use:**

```bash
# Use different port
python manage.py runserver 8001
```

**4. Permission errors (Windows):**

```bash
# Run as administrator or use:
python -m venv venv
```

### Check Status

```bash
# Check if server is running
curl http://127.0.0.1:8000/api/public/

# Check Django configuration
python manage.py check

# View logs
tail -f django.log  # If exists
```

---

## 📋 Development Workflow

### Daily Development

```bash
# 1. Activate environment
source venv/Scripts/activate

# 2. Start Django server
python manage.py runserver

# 3. In separate terminals (optional):
celery -A django_internship worker -l info    # Background tasks
python manage.py run_telegram_bot             # Telegram bot
```

### Making Changes

```bash
# After model changes
python manage.py makemigrations
python manage.py migrate

# Test changes
python test_api.py
```

---

## 🎯 Assignment Demonstration

### Required Features Demo:

1. **Django Setup**: ✅ Production settings with environment variables
2. **Public Endpoint**: http://127.0.0.1:8000/api/public/
3. **Protected Endpoint**: http://127.0.0.1:8000/api/protected/ (requires token)
4. **Celery**: Background email task after registration
5. **Telegram Bot**: /start command stores username in database

### Quick Demo Commands:

```bash
# Test public endpoint
curl http://127.0.0.1:8000/api/public/

# Register and get token
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"demo123","password_confirm":"demo123"}'

# Login to get token
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'

# Access protected endpoint
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/protected/
```

---

## 🚀 Production Deployment

For production deployment, see `DEPLOYMENT.md` for complete guide including:

- Environment variables setup
- Database configuration (PostgreSQL)
- Web server setup (Nginx + Gunicorn)
- SSL/HTTPS configuration
- Process management (systemd)

---

**🎉 Your Django Internship Assignment is ready to run and demonstrate all required features!**
