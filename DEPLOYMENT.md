# Deployment Guide - Django Internship Assignment

This guide provides instructions for deploying the Django Internship Assignment to production environments.

## 🚀 Production Deployment Checklist

### 1. Environment Configuration

**Required Environment Variables for Production:**

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here-minimum-50-characters
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# Database (PostgreSQL recommended)
DB_NAME=django_internship_prod
DB_USER=django_user
DB_PASSWORD=very-secure-database-password
DB_HOST=your-db-host
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://your-redis-host:6379/0

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-production-telegram-bot-token

# Email Configuration
EMAIL_HOST=smtp.youremailprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-app-password
```

### 2. Server Requirements

- **Python**: 3.8+
- **Database**: PostgreSQL 12+ (recommended)
- **Cache/Broker**: Redis 6+
- **Web Server**: Nginx (recommended)
- **WSGI Server**: Gunicorn (included)

### 3. Database Setup (PostgreSQL)

```sql
-- Create database and user
CREATE DATABASE django_internship_prod;
CREATE USER django_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE django_internship_prod TO django_user;
ALTER USER django_user CREATEDB;
```

### 4. Server Setup

```bash
# 1. Clone repository
git clone your-repository-url
cd django-internship

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your production settings

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput
```

### 5. Nginx Configuration

Create `/etc/nginx/sites-available/django-internship`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/django-internship /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Systemd Services

**Django Service** (`/etc/systemd/system/django-internship.service`):

```ini
[Unit]
Description=Django Internship Gunicorn daemon
After=network.target

[Service]
User=your-user
Group=your-group
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    django_internship.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

**Celery Worker Service** (`/etc/systemd/system/celery-internship.service`):

```ini
[Unit]
Description=Celery Service for Django Internship
After=network.target

[Service]
Type=forking
User=your-user
Group=your-group
EnvironmentFile=/path/to/your/project/.env
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/venv/bin/celery -A django_internship worker --loglevel=info --detach
Restart=always

[Install]
WantedBy=multi-user.target
```

**Telegram Bot Service** (`/etc/systemd/system/telegram-bot-internship.service`):

```ini
[Unit]
Description=Telegram Bot for Django Internship
After=network.target

[Service]
User=your-user
Group=your-group
EnvironmentFile=/path/to/your/project/.env
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/venv/bin/python manage.py run_telegram_bot
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start services:

```bash
sudo systemctl enable django-internship
sudo systemctl enable celery-internship
sudo systemctl enable telegram-bot-internship

sudo systemctl start django-internship
sudo systemctl start celery-internship
sudo systemctl start telegram-bot-internship
```

### 7. SSL/HTTPS Setup (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is set up automatically
```

### 8. Monitoring & Logging

**Log locations:**

- Django: `/path/to/project/django.log`
- Nginx: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- Systemd services: `sudo journalctl -u service-name`

**Monitoring commands:**

```bash
# Check service status
sudo systemctl status django-internship
sudo systemctl status celery-internship
sudo systemctl status telegram-bot-internship

# View logs
sudo journalctl -u django-internship -f
tail -f /path/to/project/django.log

# Check API health
curl https://yourdomain.com/api/public/
```

### 9. Backup Strategy

**Database backup script** (`backup.sh`):

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="django_internship_prod"

# Create backup
pg_dump $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "db_backup_*.sql" -mtime +7 -delete
```

Add to crontab:

```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

### 10. Security Considerations

1. **Firewall**: Only open necessary ports (80, 443, SSH)
2. **SSH**: Use key-based authentication, disable password auth
3. **Database**: Restrict access to application server only
4. **Redis**: Bind to localhost, use password authentication
5. **Regular updates**: Keep OS and dependencies updated
6. **Monitoring**: Set up log monitoring and alerts

### 11. Performance Optimization

1. **Database indexing**: Add indexes for frequently queried fields
2. **Redis caching**: Implement Redis for session storage and caching
3. **Static files**: Use CDN for static file delivery
4. **Gunicorn workers**: Adjust worker count based on server specs
5. **Database connection pooling**: Use pgbouncer for PostgreSQL

### 12. Deployment Script

Create `deploy.sh` for automated deployments:

```bash
#!/bin/bash
echo "Deploying Django Internship Assignment..."

# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart django-internship
sudo systemctl restart celery-internship

echo "Deployment completed!"
```

### 13. Health Check Endpoints

The API includes health check endpoints:

- `GET /api/public/` - Basic API health check
- `GET /` - Root endpoint with system information

Monitor these endpoints for uptime monitoring.

### 14. Scaling Considerations

For high-traffic scenarios:

1. **Load balancing**: Use multiple Gunicorn instances
2. **Database read replicas**: For read-heavy workloads
3. **Celery scaling**: Multiple worker instances
4. **Redis clustering**: For high availability
5. **CDN**: For static file delivery

## 🔍 Troubleshooting

**Common issues and solutions:**

1. **500 Internal Server Error**

   - Check Django logs: `tail -f django.log`
   - Verify environment variables are set correctly
   - Check database connectivity

2. **Static files not loading**

   - Run `python manage.py collectstatic`
   - Check Nginx static file configuration
   - Verify file permissions

3. **Celery tasks not running**

   - Check Redis connectivity
   - Verify Celery worker is running
   - Check Celery logs: `sudo journalctl -u celery-internship`

4. **Telegram bot not responding**
   - Verify bot token is correct
   - Check bot service status
   - Test webhook URL accessibility

This deployment guide ensures your Django Internship Assignment runs securely and efficiently in production!
