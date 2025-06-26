from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import logging
import time
import json
import requests

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(user_id):
    """
    Send welcome email to new user after registration.
    This is a background task that runs asynchronously.
    """
    try:
        user = User.objects.get(id=user_id)
        
        subject = 'Welcome to Django Internship API!'
        
        # Create both plain text and HTML versions
        text_message = f"""
        Hello {user.username}!
        
        Welcome to our Django Internship API platform. Your account has been successfully created.
        
        Here's what you can do now:
        - Access protected endpoints using your authentication token
        - View your profile at /api/profile/
        - Explore the API documentation
        
        Account Details:
        - Username: {user.username}
        - Email: {user.email}
        - Registration Date: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}
        
        Best regards,
        Django Internship Team
        """
        
        html_message = f"""
        <html>
        <body>
            <h2>Welcome to Django Internship API!</h2>
            <p>Hello <strong>{user.username}</strong>!</p>
            
            <p>Welcome to our Django Internship API platform. Your account has been successfully created.</p>
            
            <h3>What you can do now:</h3>
            <ul>
                <li>Access protected endpoints using your authentication token</li>
                <li>View your profile at <code>/api/profile/</code></li>
                <li>Explore the API documentation</li>
            </ul>
            
            <h3>Account Details:</h3>
            <ul>
                <li><strong>Username:</strong> {user.username}</li>
                <li><strong>Email:</strong> {user.email}</li>
                <li><strong>Registration Date:</strong> {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            
            <p>Best regards,<br>Django Internship Team</p>
        </body>
        </html>
        """
        
        # Send email with both text and HTML versions
        if settings.EMAIL_HOST_USER:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            logger.info(f"Welcome email sent to {user.email}")
        else:
            logger.info(f"Email not configured, but welcome email task completed for user {user.username}")
        
        return f"Welcome email sent to {user.email}"
        
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist")
        return f"User with ID {user_id} not found"
    except Exception as e:
        logger.error(f"Error sending welcome email: {str(e)}")
        raise


@shared_task
def cleanup_old_logs():
    """
    Clean up old API logs (older than 30 days).
    This task can be scheduled to run periodically.
    """
    from datetime import timedelta
    from django.utils import timezone
    from .models import ApiLog
    
    try:
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted_count = ApiLog.objects.filter(timestamp__lt=cutoff_date).delete()[0]
        logger.info(f"Cleaned up {deleted_count} old API logs")
        return f"Cleaned up {deleted_count} old API logs"
    except Exception as e:
        logger.error(f"Error cleaning up logs: {str(e)}")
        raise


@shared_task
def send_notification_email(user_id, subject, message):
    """
    Generic task to send notification emails.
    """
    try:
        user = User.objects.get(id=user_id)
        
        if settings.EMAIL_HOST_USER and user.email:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Notification email sent to {user.email}")
            return f"Notification email sent to {user.email}"
        else:
            logger.info(f"Email not configured or user email missing")
            return "Email not sent - configuration missing"
            
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist")
        return f"User with ID {user_id} not found"
    except Exception as e:
        logger.error(f"Error sending notification email: {str(e)}")
        raise


@shared_task
def send_password_reset_email(user_id, reset_link):
    """
    Send password reset email to user.
    """
    try:
        user = User.objects.get(id=user_id)
        
        subject = 'Password Reset - Django Internship API'
        message = f"""
        Hello {user.username},
        
        You requested a password reset for your Django Internship API account.
        
        Click the link below to reset your password:
        {reset_link}
        
        If you didn't request this reset, please ignore this email.
        
        Best regards,
        Django Internship Team
        """
        
        if settings.EMAIL_HOST_USER and user.email:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Password reset email sent to {user.email}")
            return f"Password reset email sent to {user.email}"
        else:
            logger.info(f"Password reset email task completed (email not configured)")
            return "Password reset email task completed"
            
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist")
        return f"User with ID {user_id} not found"
    except Exception as e:
        logger.error(f"Error sending password reset email: {str(e)}")
        raise


@shared_task
def generate_daily_report():
    """
    Generate daily usage report.
    This task can be scheduled to run daily.
    """
    try:
        from .models import ApiLog
        
        # Get today's data
        today = timezone.now().date()
        today_start = timezone.datetime.combine(today, timezone.datetime.min.time())
        today_end = timezone.datetime.combine(today, timezone.datetime.max.time())
        
        # Make timezone aware
        today_start = timezone.make_aware(today_start)
        today_end = timezone.make_aware(today_end)
        
        logs = ApiLog.objects.filter(timestamp__range=[today_start, today_end])
        
        # Generate report data
        total_requests = logs.count()
        successful_requests = logs.filter(response_status__lt=400).count()
        failed_requests = logs.filter(response_status__gte=400).count()
        unique_users = logs.filter(user__isnull=False).values('user').distinct().count()
        unique_ips = logs.values('ip_address').distinct().count()
        
        # Most accessed endpoints
        endpoint_stats = {}
        for log in logs:
            endpoint = log.endpoint
            endpoint_stats[endpoint] = endpoint_stats.get(endpoint, 0) + 1
        
        # Average response time
        avg_response_time = logs.aggregate(
            avg_time=timezone.models.Avg('response_time')
        )['avg_time'] or 0
        
        report = {
            'date': today.isoformat(),
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'success_rate': f"{(successful_requests/total_requests*100):.1f}%" if total_requests > 0 else "0%",
            'unique_users': unique_users,
            'unique_ips': unique_ips,
            'avg_response_time': f"{avg_response_time:.3f}s",
            'top_endpoints': dict(sorted(endpoint_stats.items(), key=lambda x: x[1], reverse=True)[:5])
        }
        
        logger.info(f"Daily report generated: {report}")
        return report
        
    except Exception as e:
        logger.error(f"Error generating daily report: {str(e)}")
        raise


@shared_task
def send_admin_notification(subject, message):
    """
    Send notification email to all admin users.
    """
    try:
        admin_users = User.objects.filter(is_staff=True, email__isnull=False)
        
        if not admin_users.exists():
            return "No admin users found"
        
        admin_emails = [user.email for user in admin_users if user.email]
        
        if settings.EMAIL_HOST_USER and admin_emails:
            send_mail(
                subject=f"[Django Internship API] {subject}",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=admin_emails,
                fail_silently=False,
            )
            logger.info(f"Admin notification sent to {len(admin_emails)} admins")
            return f"Admin notification sent to {len(admin_emails)} admins"
        else:
            logger.info("Admin notification task completed (email not configured)")
            return "Admin notification task completed"
            
    except Exception as e:
        logger.error(f"Error sending admin notification: {str(e)}")
        raise


@shared_task
def process_api_analytics():
    """
    Process API analytics and update statistics.
    This task can be scheduled to run periodically.
    """
    try:
        from .models import ApiLog
        
        # Simulate heavy analytics processing
        time.sleep(2)  # Simulate processing time
        
        # Get last 7 days of data
        week_ago = timezone.now() - timedelta(days=7)
        logs = ApiLog.objects.filter(timestamp__gte=week_ago)
        
        analytics = {
            'total_requests': logs.count(),
            'unique_users': logs.filter(user__isnull=False).values('user').distinct().count(),
            'avg_response_time': logs.aggregate(avg_time=timezone.models.Avg('response_time'))['avg_time'] or 0,
            'error_rate': logs.filter(response_status__gte=400).count() / logs.count() * 100 if logs.count() > 0 else 0,
            'most_active_user': None,
            'slowest_endpoint': None
        }
        
        # Find most active user
        if logs.filter(user__isnull=False).exists():
            user_activity = {}
            for log in logs.filter(user__isnull=False):
                user_id = log.user.id
                user_activity[user_id] = user_activity.get(user_id, 0) + 1
            
            most_active_user_id = max(user_activity, key=user_activity.get)
            most_active_user = User.objects.get(id=most_active_user_id)
            analytics['most_active_user'] = {
                'username': most_active_user.username,
                'request_count': user_activity[most_active_user_id]
            }
        
        # Find slowest endpoint
        endpoint_times = {}
        for log in logs:
            endpoint = log.endpoint
            if endpoint not in endpoint_times:
                endpoint_times[endpoint] = []
            endpoint_times[endpoint].append(log.response_time)
        
        if endpoint_times:
            avg_times = {endpoint: sum(times)/len(times) for endpoint, times in endpoint_times.items()}
            slowest_endpoint = max(avg_times, key=avg_times.get)
            analytics['slowest_endpoint'] = {
                'endpoint': slowest_endpoint,
                'avg_time': avg_times[slowest_endpoint]
            }
        
        logger.info(f"Analytics processed: {analytics}")
        return analytics
        
    except Exception as e:
        logger.error(f"Error processing analytics: {str(e)}")
        raise


@shared_task(bind=True, max_retries=3)
def send_bulk_notifications(self, user_ids, subject, message):
    """
    Send bulk notifications to multiple users.
    Includes retry logic for failed sends.
    """
    try:
        users = User.objects.filter(id__in=user_ids, email__isnull=False)
        
        sent_count = 0
        failed_emails = []
        
        for user in users:
            try:
                if user.email and settings.EMAIL_HOST_USER:
                    send_mail(
                        subject=subject,
                        message=f"Hello {user.username},\n\n{message}",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    sent_count += 1
                    logger.info(f"Bulk notification sent to {user.email}")
                else:
                    failed_emails.append(user.email or f"user_{user.id}")
                    
            except Exception as e:
                logger.error(f"Failed to send email to {user.email}: {str(e)}")
                failed_emails.append(user.email or f"user_{user.id}")
        
        result = {
            'sent_count': sent_count,
            'failed_count': len(failed_emails),
            'failed_emails': failed_emails
        }
        
        if failed_emails and self.request.retries < self.max_retries:
            logger.warning(f"Retrying bulk notification for {len(failed_emails)} failed emails")
            raise self.retry(countdown=60, exc=Exception(f"Failed to send to {len(failed_emails)} emails"))
        
        logger.info(f"Bulk notification completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in bulk notification task: {str(e)}")
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=60)
        raise
