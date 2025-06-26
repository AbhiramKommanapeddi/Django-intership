from django.contrib import admin
from .models import TelegramUser, BotMessage


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username', 'full_name', 'django_user', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_bot', 'created_at']
    search_fields = ['username', 'first_name', 'last_name', 'telegram_id']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    
    # Temporarily enable adding for demo purposes
    def has_add_permission(self, request):
        """Allow adding TelegramUser through admin for demo"""
        return True
    
    def get_readonly_fields(self, request, obj=None):
        """Only make timestamp fields readonly"""
        return ['created_at', 'updated_at']
    
    # Add help text for manual creation
    fieldsets = (
        ('Telegram Information', {
            'fields': ('telegram_id', 'username', 'first_name', 'last_name', 'chat_id'),
            'description': 'Required: telegram_id and chat_id must be unique numbers (e.g., 123456789)'
        }),
        ('Settings', {
            'fields': ('is_bot', 'language_code', 'is_active')
        }),
        ('Django Integration', {
            'fields': ('django_user',),
            'description': 'Optional: Link with a Django user account'
        }),
    )


@admin.register(BotMessage)
class BotMessageAdmin(admin.ModelAdmin):
    list_display = ['telegram_user', 'message_type', 'command', 'timestamp', 'response_sent']
    list_filter = ['message_type', 'response_sent', 'timestamp']
    search_fields = ['telegram_user__username', 'command', 'message_text']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        """Disable adding BotMessage through admin - they are created by the bot"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Make bot messages readonly"""
        return False
