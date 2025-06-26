from django.contrib import admin
from .models import UserProfile, ApiLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'telegram_username', 'phone_number', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'telegram_username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ApiLog)
class ApiLogAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for API logs with comprehensive filtering and display options.
    Demonstrates ChangeAddDeleteView functionality for API logging.
    """
    list_display = [
        'timestamp', 'endpoint', 'method', 'user_display', 'ip_address', 
        'response_status', 'status_color', 'response_time_display'
    ]
    list_filter = [
        'method', 'response_status', 'timestamp', 
        ('user', admin.RelatedOnlyFieldListFilter),
        ('timestamp', admin.DateFieldListFilter)
    ]
    search_fields = ['endpoint', 'user__username', 'ip_address', 'method']
    readonly_fields = [
        'endpoint', 'method', 'user', 'ip_address', 
        'timestamp', 'response_status', 'response_time'
    ]
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'
    list_per_page = 25
    
    # Disable add/change permissions (logs should be read-only)
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete logs
    
    def user_display(self, obj):
        """Display user with proper formatting"""
        if obj.user:
            return f"{obj.user.username} ({obj.user.get_full_name() or 'No name'})"
        return "Anonymous"
    user_display.short_description = "User"
    user_display.admin_order_field = "user__username"
    
    def status_color(self, obj):
        """Color-coded status display"""
        color = {
            200: 'green',
            201: 'green', 
            400: 'orange',
            401: 'red',
            403: 'red',
            404: 'orange',
            500: 'red'
        }.get(obj.response_status, 'black')
        
        status_text = {
            200: 'OK',
            201: 'Created',
            400: 'Bad Request',
            401: 'Unauthorized', 
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Server Error'
        }.get(obj.response_status, 'Unknown')
        
        return f'<span style="color: {color}; font-weight: bold;">{obj.response_status} {status_text}</span>'
    
    status_color.short_description = "Status"
    status_color.allow_tags = True
    status_color.admin_order_field = "response_status"
    
    def response_time_display(self, obj):
        """Format response time with color coding"""
        time_ms = obj.response_time * 1000  # Convert to milliseconds
        
        # Color code based on performance
        if time_ms < 100:
            color = 'green'
        elif time_ms < 500:
            color = 'orange'
        else:
            color = 'red'
        
        return f'<span style="color: {color};">{time_ms:.1f}ms</span>'
    
    response_time_display.short_description = "Response Time"
    response_time_display.allow_tags = True
    response_time_display.admin_order_field = "response_time"
    
    fieldsets = (
        ('Request Information', {
            'fields': ('endpoint', 'method', 'user', 'ip_address', 'timestamp')
        }),
        ('Response Information', {
            'fields': ('response_status', 'response_time')
        })
    )
