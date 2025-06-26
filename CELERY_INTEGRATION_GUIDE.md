# Celery Integration Guide - Django Internship Assignment

## Overview

This Django project includes comprehensive **Celery integration** with **Redis as the message broker** for handling background tasks asynchronously. This is essential for operations that shouldn't block the main request-response cycle.

## ✅ What is Implemented

### 1. **Celery Configuration**

- **Broker**: Redis (`redis://localhost:6379/0`)
- **Result Backend**: Redis (same as broker)
- **Serialization**: JSON for both tasks and results
- **Auto-discovery**: Automatically finds tasks in Django apps

### 2. **Background Tasks Implemented**

#### 📧 **Email Tasks**

1. **Welcome Email** (`send_welcome_email`)

   - Sends HTML + text welcome email after user registration
   - Includes user details and account information
   - Triggered automatically during user registration

2. **Password Reset Email** (`send_password_reset_email`)

   - Sends password reset instructions
   - Includes secure reset link

3. **Bulk Notifications** (`send_bulk_notifications`)

   - Send notifications to multiple users
   - Includes retry logic for failed sends
   - Tracks success/failure rates

4. **Admin Notifications** (`send_admin_notification`)
   - Sends alerts to all admin users
   - System notifications and alerts

#### 📊 **Analytics & Reporting Tasks**

5. **Daily Report Generation** (`generate_daily_report`)

   - Analyzes daily API usage
   - Calculates success rates, response times
   - Identifies top endpoints and users

6. **API Analytics Processing** (`process_api_analytics`)
   - Weekly analytics processing
   - Heavy computational tasks
   - User activity analysis

#### 🧹 **Maintenance Tasks**

7. **Log Cleanup** (`cleanup_old_logs`)

   - Removes API logs older than 30 days
   - Scheduled maintenance task
   - Database optimization

8. **Database Backup** (`backup_database`)
   - Creates JSON backups of important data
   - Scheduled backup operations

---

## 🔧 Setup Instructions

### 1. **Install Redis**

#### Windows:

```bash
# Download Redis for Windows or use WSL
# Or use Docker:
docker run -d -p 6379:6379 redis:alpine
```

#### macOS:

```bash
brew install redis
redis-server
```

#### Ubuntu/Linux:

```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

### 2. **Install Python Dependencies**

```bash
pip install celery redis django-celery-beat
```

### 3. **Environment Variables**

Add to your `.env` file:

```env
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 4. **Start Celery Worker**

```bash
# In your project directory
celery -A django_internship worker --loglevel=info
```

### 5. **Start Celery Beat (Optional - for scheduled tasks)**

```bash
celery -A django_internship beat --loglevel=info
```

### 6. **Monitor with Flower (Optional)**

```bash
pip install flower
celery -A django_internship flower
# Access at: http://localhost:5555
```

---

## 📧 Email Task Example

### Automatic Welcome Email After Registration

When a user registers via `/api/register/`, a welcome email is automatically sent in the background:

```python
# In api/views.py
@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        # 🚀 Send welcome email asynchronously
        send_welcome_email.delay(user.id)

        return Response({
            'message': 'User registered successfully!',
            'user_id': user.id,
            'username': user.username,
            'token': token.key,
            'email_sent': 'Welcome email will be sent shortly'
        }, status=status.HTTP_201_CREATED)
```

### Welcome Email Task Implementation

```python
# In api/tasks.py
@shared_task
def send_welcome_email(user_id):
    """Send welcome email to new user after registration."""
    try:
        user = User.objects.get(id=user_id)

        # HTML email content
        html_message = f"""
        <html>
        <body>
            <h2>Welcome to Django Internship API!</h2>
            <p>Hello <strong>{user.username}</strong>!</p>

            <h3>What you can do now:</h3>
            <ul>
                <li>Access protected endpoints using your token</li>
                <li>View your profile at <code>/api/profile/</code></li>
                <li>Explore the API documentation</li>
            </ul>

            <h3>Account Details:</h3>
            <ul>
                <li><strong>Username:</strong> {user.username}</li>
                <li><strong>Email:</strong> {user.email}</li>
                <li><strong>Registration:</strong> {user.date_joined}</li>
            </ul>
        </body>
        </html>
        """

        # Send email with both text and HTML versions
        email = EmailMultiAlternatives(
            subject='Welcome to Django Internship API!',
            body=text_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

        return f"Welcome email sent to {user.email}"

    except Exception as e:
        logger.error(f"Error sending welcome email: {str(e)}")
        raise
```

---

## 🔄 Task Workflows

### Sequential Tasks (Chains)

Execute tasks one after another:

```python
from celery import chain

# Generate report, then send notification
workflow = chain(
    generate_daily_report.s(),
    send_admin_notification.s("Daily Report", "Report generated!")
)
result = workflow.apply_async()
```

### Parallel Tasks (Groups)

Execute multiple tasks simultaneously:

```python
from celery import group

# Run multiple tasks in parallel
parallel_tasks = group(
    send_welcome_email.s(user_id),
    generate_daily_report.s(),
    process_api_analytics.s()
)
result = parallel_tasks.apply_async()
```

### Complex Workflows (Chords)

Combine groups with callbacks:

```python
from celery import chord

# Run parallel tasks, then execute callback
workflow = chord([
    process_api_analytics.s(),
    generate_daily_report.s()
])(send_admin_notification.s("Analytics Complete"))
```

---

## 📊 Real Examples & Demo

### 1. **User Registration Flow**

```bash
POST /api/register/
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123"
}

# Response:
{
    "message": "User registered successfully!",
    "user_id": 5,
    "username": "newuser",
    "token": "abc123...",
    "email_sent": "Welcome email will be sent shortly"
}

# Background: Welcome email task queued and executed
```

### 2. **Daily Analytics Report**

```python
# Task generates comprehensive daily report
{
    "date": "2025-06-26",
    "total_requests": 145,
    "successful_requests": 132,
    "failed_requests": 13,
    "success_rate": "91.0%",
    "unique_users": 8,
    "unique_ips": 12,
    "avg_response_time": "0.087s",
    "top_endpoints": {
        "/api/protected/": 45,
        "/api/public/": 38,
        "/api/login/": 25
    }
}
```

### 3. **Bulk Notification Result**

```python
# Send notification to all users
{
    "sent_count": 15,
    "failed_count": 2,
    "failed_emails": ["inactive@example.com", "bounced@example.com"]
}
```

---

## 🎛️ Monitoring & Management

### Celery Commands

```bash
# Check active tasks
celery -A django_internship inspect active

# Check registered tasks
celery -A django_internship inspect registered

# Get worker statistics
celery -A django_internship inspect stats

# Monitor events in real-time
celery -A django_internship events

# Purge all tasks from queue
celery -A django_internship purge

# Control workers
celery -A django_internship control shutdown
```

### Task Result Inspection

```python
from celery.result import AsyncResult

# Check task status
result = AsyncResult('task-id-here')
print(f"State: {result.state}")
print(f"Result: {result.result}")
print(f"Traceback: {result.traceback}")
```

### Web-based Monitoring with Flower

```bash
pip install flower
celery -A django_internship flower

# Access at: http://localhost:5555
# Features:
# - Real-time task monitoring
# - Worker statistics
# - Task history
# - Task details and results
# - Rate limiting controls
```

---

## 🚀 How to Test

### 1. **Start Required Services**

```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Django
python manage.py runserver

# Terminal 3: Start Celery Worker
celery -A django_internship worker --loglevel=info
```

### 2. **Run the Demo**

```bash
python celery_demo.py
```

### 3. **Test Registration Email**

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser123",
    "email": "test@example.com",
    "password": "securepass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 4. **Manual Task Execution**

```python
# In Django shell
python manage.py shell

from api.tasks import send_welcome_email, generate_daily_report
from django.contrib.auth.models import User

# Send welcome email
user = User.objects.first()
result = send_welcome_email.delay(user.id)
print(f"Task ID: {result.id}")
print(f"Result: {result.get()}")

# Generate report
report_result = generate_daily_report.delay()
print(f"Report: {report_result.get()}")
```

---

## 🎯 Benefits Demonstrated

### ✅ **Performance**

- Non-blocking operations
- Background processing
- Scalable task execution

### ✅ **Reliability**

- Task retry mechanisms
- Error handling and logging
- Result persistence

### ✅ **Scalability**

- Multiple worker processes
- Distributed task execution
- Load balancing

### ✅ **Monitoring**

- Task status tracking
- Performance metrics
- Real-time monitoring

### ✅ **Flexibility**

- Complex workflows
- Scheduled tasks
- Priority queues

---

## 📁 File Structure

```
django_internship/
├── django_internship/
│   ├── celery.py          # Celery configuration
│   ├── settings.py        # Celery settings
│   └── __init__.py        # Celery app initialization
├── api/
│   ├── tasks.py           # Background tasks
│   ├── views.py           # API endpoints (triggers tasks)
│   └── models.py          # Data models
├── celery_demo.py         # Comprehensive demo script
└── requirements.txt       # Dependencies (includes celery, redis)
```

This comprehensive Celery integration provides enterprise-level background task processing for the Django Internship Assignment project!
