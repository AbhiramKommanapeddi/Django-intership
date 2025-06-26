from django.db import models
from django.contrib.auth.models import User


class TelegramUser(models.Model):
    """Model to store Telegram user information."""
    telegram_id = models.BigIntegerField(unique=True, help_text="Telegram user ID")
    username = models.CharField(max_length=100, blank=True, null=True, help_text="Telegram username")
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    chat_id = models.BigIntegerField(help_text="Telegram chat ID")
    is_bot = models.BooleanField(default=False)
    language_code = models.CharField(max_length=10, blank=True, null=True)
    
    # Link to Django user (optional)
    django_user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='telegram_profile'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"@{self.username}" if self.username else f"User {self.telegram_id}"
    
    @property
    def full_name(self):
        """Get full name from first and last name."""
        names = [self.first_name, self.last_name]
        return " ".join([name for name in names if name])
    
    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"


class BotMessage(models.Model):
    """Model to log bot messages."""
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=50, default='text')
    message_text = models.TextField(blank=True, null=True)
    command = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    response_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.telegram_user} - {self.command or self.message_type} at {self.timestamp}"
    
    class Meta:
        verbose_name = "Bot Message"
        verbose_name_plural = "Bot Messages"
        ordering = ['-timestamp']
