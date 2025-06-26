#!/usr/bin/env python
"""
Script to create sample Telegram users for admin demonstration
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
django.setup()

from telegram_bot.models import TelegramUser, BotMessage
from django.contrib.auth.models import User

def create_sample_data():
    """Create sample Telegram users and messages for admin demo"""
    
    print("🤖 Creating Sample Telegram Bot Data")
    print("=" * 40)
    
    # Sample Telegram users data
    telegram_users_data = [
        {
            'telegram_id': 123456789,
            'username': 'john_doe',
            'first_name': 'John',
            'last_name': 'Doe',
            'chat_id': 123456789,
            'language_code': 'en'
        },
        {
            'telegram_id': 987654321,
            'username': 'jane_smith',
            'first_name': 'Jane',
            'last_name': 'Smith', 
            'chat_id': 987654321,
            'language_code': 'en'
        },
        {
            'telegram_id': 555444333,
            'username': 'telegram_user',
            'first_name': 'Test',
            'last_name': 'User',
            'chat_id': 555444333,
            'language_code': 'en'
        }
    ]
    
    # Create Telegram users
    created_users = []
    for user_data in telegram_users_data:
        telegram_user, created = TelegramUser.objects.get_or_create(
            telegram_id=user_data['telegram_id'],
            defaults=user_data
        )
        
        if created:
            print(f"✅ Created Telegram user: @{telegram_user.username}")
            created_users.append(telegram_user)
        else:
            print(f"ℹ️  Telegram user @{telegram_user.username} already exists")
            created_users.append(telegram_user)
    
    # Create sample bot messages
    sample_messages = [
        {'command': '/start', 'message_type': 'start', 'message_text': '/start'},
        {'command': '/help', 'message_type': 'help', 'message_text': '/help'},
        {'command': '/status', 'message_type': 'status', 'message_text': '/status'},
        {'command': None, 'message_type': 'text', 'message_text': 'Hello bot!'},
        {'command': '/info', 'message_type': 'info', 'message_text': '/info'},
    ]
    
    print(f"\n📝 Creating sample bot messages...")
    for i, telegram_user in enumerate(created_users):
        if i < len(sample_messages):
            msg_data = sample_messages[i]
            message, created = BotMessage.objects.get_or_create(
                telegram_user=telegram_user,
                message_type=msg_data['message_type'],
                defaults={
                    'command': msg_data['command'],
                    'message_text': msg_data['message_text'],
                    'response_sent': True
                }
            )
            if created:
                print(f"✅ Created message: {msg_data['message_text']} from @{telegram_user.username}")
    
    print(f"\n🎯 Admin Demo Ready!")
    print(f"✅ Created {len(created_users)} Telegram users")
    print(f"✅ Created sample bot messages")
    print(f"\n🔗 View in admin:")
    print(f"   • Telegram Users: http://127.0.0.1:8000/admin/telegram_bot/telegramuser/")
    print(f"   • Bot Messages: http://127.0.0.1:8000/admin/telegram_bot/botmessage/")
    print(f"\n📝 Note: You can view and edit existing records, but adding new")
    print(f"   Telegram users should be done through the bot, not the admin.")

if __name__ == "__main__":
    create_sample_data()
