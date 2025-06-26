from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile to store additional information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class ApiLog(models.Model):
    """Log API requests for monitoring."""
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    response_status = models.IntegerField()
    response_time = models.FloatField(help_text="Response time in seconds")

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.response_status}"

    class Meta:
        verbose_name = "API Log"
        verbose_name_plural = "API Logs"
        ordering = ['-timestamp']
