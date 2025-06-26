"""
Telegram Bot implementation for Django Internship project.
"""
import logging
import asyncio
from typing import Optional
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from django.conf import settings
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import TelegramUser, BotMessage

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class DjangoBotHandler:
    """Handler class for Telegram bot with Django integration."""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.application = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        logger.info(f"Start command from user: {user.username} (ID: {user.id})")
        
        try:
            # Save or update telegram user in database
            telegram_user = await self.save_telegram_user(user, chat_id)
            
            # Log the message
            await self.log_message(telegram_user, 'start', '/start')
            
            # Send welcome message
            welcome_message = f"""
🎉 *Welcome to Django Internship Bot!*

Hello {telegram_user.full_name or user.first_name or 'there'}!

Your Telegram information has been saved:
• Username: @{user.username or 'Not set'}
• User ID: `{user.id}`
• Chat ID: `{chat_id}`

This bot is part of the Django Internship Assignment project.

Available commands:
/start - Show this welcome message
/help - Get help information
/status - Check your registration status
/info - Get API information

For more features, check out our API endpoints!
            """
            
            await update.message.reply_text(
                welcome_message,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text(
                "Sorry, there was an error processing your request. Please try again later."
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command."""
        user = update.effective_user
        
        try:
            telegram_user = await self.get_telegram_user(user.id)
            if telegram_user:
                await self.log_message(telegram_user, 'help', '/help')
            
            help_message = """
🤖 *Django Internship Bot Help*

This bot is connected to a Django REST API with the following features:

*Available Commands:*
/start - Initialize your account and get welcome message
/help - Show this help message
/status - Check your registration status
/info - Get API endpoint information

*API Features:*
• Public endpoints (no authentication required)
• Protected endpoints (token authentication required)
• User registration and login
• Celery background tasks
• Email notifications

*How to use the API:*
1. Register at: `/api/register/`
2. Login at: `/api/login/`
3. Use your token to access protected endpoints

Visit the API documentation for more details!
            """
            
            await update.message.reply_text(
                help_message,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in help command: {e}")
            await update.message.reply_text("Error processing help command.")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /status command."""
        user = update.effective_user
        
        try:
            telegram_user = await self.get_telegram_user(user.id)
            
            if telegram_user:
                await self.log_message(telegram_user, 'status', '/status')
                
                status_message = f"""
📊 *Your Status*

✅ Telegram account registered
• Username: @{telegram_user.username or 'Not set'}
• Full name: {telegram_user.full_name or 'Not set'}
• Registration date: {telegram_user.created_at.strftime('%Y-%m-%d %H:%M')}
• Status: {'Active' if telegram_user.is_active else 'Inactive'}

{f'🔗 Linked Django user: {telegram_user.django_user.username}' if telegram_user.django_user else '❌ No Django account linked'}

To link with Django account, register at the API endpoints.
                """
            else:
                status_message = """
❌ *Not Registered*

You haven't started the bot yet. Please use /start to register your Telegram account.
                """
            
            await update.message.reply_text(
                status_message,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await update.message.reply_text("Error checking status.")
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /info command."""
        user = update.effective_user
        
        try:
            telegram_user = await self.get_telegram_user(user.id)
            if telegram_user:
                await self.log_message(telegram_user, 'info', '/info')
            
            info_message = """
🔗 *API Information*

*Public Endpoints:*
• `GET /api/public/` - Public information
• `POST /api/register/` - User registration
• `POST /api/login/` - User login

*Protected Endpoints:*
• `GET /api/protected/` - Protected data
• `GET /api/profile/` - User profile
• `PUT /api/profile/` - Update profile
• `GET /api/logs/` - API logs (admin only)

*Authentication:*
Use Token authentication in header:
`Authorization: Token your-token-here`

*Features:*
✅ Django REST Framework
✅ Token Authentication
✅ Celery Background Tasks
✅ Email Notifications
✅ Telegram Bot Integration
✅ Production Settings
✅ Redis Integration

This project demonstrates all the requirements for the Django Internship Assignment!
            """
            
            await update.message.reply_text(
                info_message,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in info command: {e}")
            await update.message.reply_text("Error getting API info.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular text messages."""
        user = update.effective_user
        message_text = update.message.text
        
        try:
            telegram_user = await self.get_telegram_user(user.id)
            
            if telegram_user:
                await self.log_message(telegram_user, 'text', message_text)
                
                response = f"""
Thanks for your message! 💬

I received: "{message_text}"

I'm a bot for the Django Internship Assignment. Use these commands:
/start - Get started
/help - Get help
/status - Check your status
/info - API information

Or interact with the API directly at the endpoints!
                """
            else:
                response = """
Hello! Please use /start first to register with the bot.
                """
            
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text("Sorry, I couldn't process your message.")
    
    @sync_to_async
    def save_telegram_user(self, user, chat_id) -> TelegramUser:
        """Save or update telegram user in database."""
        telegram_user, created = TelegramUser.objects.get_or_create(
            telegram_id=user.id,
            defaults={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'chat_id': chat_id,
                'is_bot': user.is_bot,
                'language_code': user.language_code,
            }
        )
        
        if not created:
            # Update existing user
            telegram_user.username = user.username
            telegram_user.first_name = user.first_name
            telegram_user.last_name = user.last_name
            telegram_user.chat_id = chat_id
            telegram_user.language_code = user.language_code
            telegram_user.save()
        
        return telegram_user
    
    @sync_to_async
    def get_telegram_user(self, telegram_id) -> Optional[TelegramUser]:
        """Get telegram user from database."""
        try:
            return TelegramUser.objects.get(telegram_id=telegram_id)
        except TelegramUser.DoesNotExist:
            return None
    
    @sync_to_async
    def log_message(self, telegram_user: TelegramUser, message_type: str, content: str):
        """Log bot message to database."""
        BotMessage.objects.create(
            telegram_user=telegram_user,
            message_type=message_type,
            message_text=content,
            command=content if content.startswith('/') else None,
            response_sent=True
        )
    
    def setup_handlers(self):
        """Setup bot command and message handlers."""
        if not self.application:
            self.application = Application.builder().token(self.bot_token).build()
        
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        
        # Message handler for text messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("Bot handlers setup complete")
    
    async def start_bot(self):
        """Start the bot."""
        if not self.bot_token:
            logger.error("TELEGRAM_BOT_TOKEN not configured")
            return
        
        try:
            self.setup_handlers()
            logger.info("Starting Telegram bot...")
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            logger.info("Bot started successfully!")
            
            # Keep the bot running
            await self.application.updater.idle()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
        finally:
            await self.application.stop()
    
    def run_bot(self):
        """Run the bot (synchronous wrapper)."""
        asyncio.run(self.start_bot())


# Global bot instance
bot_handler = DjangoBotHandler()


def start_telegram_bot():
    """Function to start the telegram bot."""
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram bot token not configured. Bot will not start.")
        return
    
    logger.info("Initializing Telegram bot...")
    bot_handler.run_bot()
