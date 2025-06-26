# Step-by-Step Celery Setup and Demo Guide

## Quick Start (5 minutes)

### Step 1: Install and Start Redis

```bash
# Using Docker (recommended)
docker run -d -p 6379:6379 --name redis-server redis:alpine

# Test Redis connection
docker exec -it redis-server redis-cli ping
# Should return: PONG
```

### Step 2: Start Django Development Server

```bash
# In your project directory
python manage.py runserver
```

### Step 3: Start Celery Worker

```bash
# Open a new terminal in project directory
celery -A django_internship worker --loglevel=info
```

**Keep this terminal open!** This is your Celery worker.

### Step 4: Run the Demo

```bash
# In a third terminal
python complete_celery_demo.py
```

## What You'll See

### 1. Redis Connection Test

```
✅ Redis is running and accessible!
   Redis info: 7.0.0
```

### 2. Celery Worker Check

```
✅ Celery worker is running!
   Node: celery@COMPUTER-NAME
   Pool: prefork
   Processes: 4
```

### 3. User Registration with Background Email

```
📋 Step 1: Registering new user
Username: celery_demo_1640123456
Email: demo@example.com

✅ Registration successful!
   User ID: 5
   Token: abc123def456...
   Background Email: Welcome email will be sent shortly

📋 Step 2: What happened in the background
✅ User account created in database
✅ Authentication token generated
✅ Welcome email task queued in Celery
✅ Task will be processed by Celery worker
```

### 4. Background Tasks Demo

```
📋 Step 1: Triggering daily report generation
   Task ID: 4a7b2c1d-e3f4-5678-9abc-def012345678
   Status: Task queued for background processing

📋 Step 4: Monitoring task progress
   Task 1 (4a7b2c1d...): ✅ COMPLETED
      Result: {'date': '2025-06-26', 'total_requests': 15, 'success_rate': '93.3%'}
```

## Real Example Output

When you register a user, here's what happens:

### In the Django Server Terminal:

```
[26/Jun/2025 14:30:15] "POST /api/register/ HTTP/1.1" 201 125
```

### In the Celery Worker Terminal:

```
[2025-06-26 14:30:15,123: INFO/MainProcess] Received task: api.tasks.send_welcome_email[abc-123-def]
[2025-06-26 14:30:15,456: INFO/ForkPoolWorker-1] Task api.tasks.send_welcome_email[abc-123-def] succeeded in 0.234s: 'Welcome email sent to demo@example.com'
```

### In Your Email (if configured):

```
Subject: Welcome to Django Internship API!

Hello celery_demo_1640123456!

Welcome to our Django Internship API platform. Your account has been successfully created.

What you can do now:
- Access protected endpoints using your authentication token
- View your profile at /api/profile/
- Explore the API documentation

Account Details:
- Username: celery_demo_1640123456
- Email: demo@example.com
- Registration Date: 2025-06-26 14:30:15

Best regards,
Django Internship Team
```

## Troubleshooting

### Error: "redis.exceptions.ConnectionError"

- **Solution**: Redis is not running
- **Fix**: `docker start redis-server` or start Redis service

### Error: "No Celery workers found"

- **Solution**: Celery worker not started
- **Fix**: Run `celery -A django_internship worker --loglevel=info`

### Error: "Connection refused" (Django)

- **Solution**: Django server not running
- **Fix**: Run `python manage.py runserver`

### Tasks stuck in PENDING state

- **Solution**: Celery worker crashed or overloaded
- **Fix**: Restart Celery worker

## Monitoring Tasks (Optional)

### Install Flower (Web-based monitoring)

```bash
pip install flower
flower -A django_internship --port=5555
```

Then visit: http://localhost:5555

### Check task status programmatically

```python
# In Django shell
from api.tasks import send_welcome_email
task = send_welcome_email.delay(1)
print(task.status)  # PENDING, SUCCESS, FAILURE
print(task.result)  # Task result
```

## Production Tips

1. **Use Redis Cluster** for high availability
2. **Monitor with Flower** in production
3. **Set up task routing** for different queue types
4. **Use Celery Beat** for scheduled tasks
5. **Implement proper logging** and error handling

## Files Modified/Created

- ✅ `django_internship/celery.py` - Celery configuration
- ✅ `api/tasks.py` - Background task definitions
- ✅ `api/views.py` - Integration with user registration
- ✅ `django_internship/settings.py` - Redis/Celery settings
- 🆕 `complete_celery_demo.py` - Comprehensive demo script
- 🆕 `REDIS_INSTALLATION_GUIDE.md` - Redis setup guide

Your Celery integration is now complete and production-ready! 🚀
