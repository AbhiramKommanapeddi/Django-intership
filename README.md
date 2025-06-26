# Django Internship Assignment

A comprehensive Django REST Framework project demonstrating backend development skills with authentication, Celery, Telegram bot integration, and production-ready settings.

## 🚀 Features

- **Django REST Framework**: Complete API with public and protected endpoints
- **Authentication**: Token-based authentication and session authentication
- **Celery Integration**: Background tasks with Redis broker
- **Telegram Bot**: Interactive bot that stores user information
- **Production Settings**: Environment variables, security settings, logging
- **Database**: PostgreSQL support with SQLite fallback
- **Email**: Asynchronous email notifications via Celery
- **Admin Interface**: Django admin with custom configurations
- **API Logging**: Request/response logging and monitoring

## 📋 Requirements

- Python 3.8+
- Redis server
- PostgreSQL (optional, SQLite fallback included)

## 🛠️ Installation & Setup

### 1. Clone and Setup Virtual Environment

```bash
# Clone the repository
git clone <your-repository-url>
cd django-internship

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

**Required Environment Variables:**

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-very-long-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL - optional)
DB_NAME=django_internship
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Start Redis Server

```bash
# On Windows (with Redis installed):
redis-server

# On Linux/Mac:
sudo systemctl start redis
# or
redis-server
```

## 🚀 Running the Application

### 1. Start Django Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

### 2. Start Celery Worker

Open a new terminal and run:

```bash
# Activate virtual environment first
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/Mac

# Start Celery worker
celery -A django_internship worker --loglevel=info
```

### 3. Start Telegram Bot (Optional)

Open another terminal and run:

```bash
# Activate virtual environment first
source venv/Scripts/activate  # Windows

# Start Telegram bot
python manage.py run_telegram_bot
```

## 📡 API Documentation

### Public Endpoints

#### GET `/api/public/`

- **Description**: Public endpoint accessible to everyone
- **Authentication**: None required
- **Response**: Server information and available endpoints

```bash
curl http://localhost:8000/api/public/
```

#### POST `/api/register/`

- **Description**: Register a new user account
- **Authentication**: None required
- **Body**:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "Test",
  "last_name": "User"
}
```

#### POST `/api/login/`

- **Description**: Login and get authentication token
- **Authentication**: None required
- **Body**:

```json
{
  "username": "testuser",
  "password": "securepassword123"
}
```

### Protected Endpoints

#### GET `/api/protected/`

- **Description**: Protected endpoint for authenticated users only
- **Authentication**: Token required
- **Headers**: `Authorization: Token your-token-here`

```bash
curl -H "Authorization: Token your-token-here" http://localhost:8000/api/protected/
```

#### GET `/api/profile/`

- **Description**: Get user profile information
- **Authentication**: Token required
- **Method**: GET (retrieve) / PUT (update)

#### GET `/api/logs/` (Admin Only)

- **Description**: View API request logs
- **Authentication**: Token required + Admin user
- **Method**: GET

## 🤖 Telegram Bot

### Setup Telegram Bot

1. **Create Bot with BotFather**:

   - Send `/newbot` to [@BotFather](https://t.me/BotFather)
   - Follow instructions to create your bot
   - Copy the bot token to your `.env` file

2. **Bot Commands**:

   - `/start` - Register with the bot and store Telegram username
   - `/help` - Get help information
   - `/status` - Check registration status
   - `/info` - Get API information

3. **Features**:
   - Stores Telegram username in Django database
   - Links Telegram users with Django users
   - Provides API information and help

## ⚙️ Celery Tasks

### Background Tasks

1. **Welcome Email**: Sent automatically after user registration
2. **Log Cleanup**: Periodically clean old API logs
3. **Notification Emails**: Generic notification system

### Running Celery

```bash
# Worker (processes tasks)
celery -A django_internship worker --loglevel=info

# Beat (scheduler - optional)
celery -A django_internship beat --loglevel=info

# Monitor (optional)
celery -A django_internship flower
```

## 🔒 Authentication

### Token Authentication

1. **Register** or **Login** to get your token
2. **Include token** in all protected requests:

```bash
# Header format
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# Example request
curl -H "Authorization: Token your-token-here" http://localhost:8000/api/protected/
```

## 🗄️ Database Models

### API App Models

- **UserProfile**: Extended user information including Telegram data
- **ApiLog**: Request/response logging for monitoring

### Telegram Bot Models

- **TelegramUser**: Telegram user information and Django user linking
- **BotMessage**: Bot interaction history

## 📊 Admin Interface

Access the Django admin at `http://localhost:8000/admin/`

**Features**:

- User management
- API logs monitoring
- Telegram users management
- Bot message history

## 🔧 Production Deployment

### Environment Variables

Ensure all environment variables are properly set:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Static Files

```bash
python manage.py collectstatic
```

### Database

Configure PostgreSQL for production:

```env
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=secure_password
DB_HOST=db_host
DB_PORT=5432
```

### Security

The project includes production-ready security settings:

- HTTPS enforcement
- XSS protection
- Content type sniffing protection
- CSRF protection
- CORS configuration

## 🧪 Testing

### Test the API

```bash
# Test public endpoint
curl http://localhost:8000/api/public/

# Register user
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password_confirm":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Access protected endpoint
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/protected/
```

## 📁 Project Structure

```
django_internship/
├── django_internship/          # Main project settings
│   ├── __init__.py
│   ├── settings.py            # Production-ready settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py
│   └── celery.py              # Celery configuration
├── api/                       # API application
│   ├── models.py              # User profiles, API logs
│   ├── views.py               # API endpoints
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # API URLs
│   ├── admin.py               # Admin configuration
│   └── tasks.py               # Celery tasks
├── telegram_bot/              # Telegram bot application
│   ├── models.py              # Telegram user models
│   ├── bot.py                 # Bot implementation
│   ├── admin.py               # Admin configuration
│   └── management/commands/
│       └── run_telegram_bot.py
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🎯 Assignment Requirements ✅

- ✅ **Django Project Setup**: Production-ready settings with environment variables
- ✅ **API Development**: Public and protected endpoints with Token authentication
- ✅ **Django Login**: Web-based authentication system
- ✅ **Celery Integration**: Background tasks with Redis broker
- ✅ **Telegram Bot**: Interactive bot storing usernames in database
- ✅ **Code Management**: Clean code, proper commits, comprehensive documentation

## 🚀 Quick Start Commands

```bash
# 1. Setup project
git clone <repo-url> && cd django-internship
python -m venv venv && source venv/Scripts/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Setup database
python manage.py migrate
python manage.py createsuperuser

# 4. Start services (in separate terminals)
python manage.py runserver                    # Django server
celery -A django_internship worker -l info    # Celery worker
python manage.py run_telegram_bot             # Telegram bot
```

## 📞 Contact & Support

This project was created as part of the Django Internship Assignment, demonstrating:

- Clean, production-ready code
- Proper Django project structure
- REST API development
- Background task processing
- Real-time bot integration
- Comprehensive documentation

For questions or support, please check the code comments and documentation throughout the project.
