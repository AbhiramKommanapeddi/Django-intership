from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, ApiLog


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'telegram_username', 'telegram_chat_id', 'phone_number', 'bio', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ApiLogSerializer(serializers.ModelSerializer):
    """Serializer for ApiLog model."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ApiLog
        fields = ['id', 'endpoint', 'method', 'user', 'user_username', 'ip_address', 'timestamp', 'response_status', 'response_time']
        read_only_fields = ['id', 'timestamp']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # Create user profile
        UserProfile.objects.create(user=user)
        return user
