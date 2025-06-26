"""
Django management command to run the Telegram bot.
Usage: python manage.py run_telegram_bot
"""
from django.core.management.base import BaseCommand
from telegram_bot.bot import start_telegram_bot


class Command(BaseCommand):
    help = 'Run the Telegram bot'
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting Telegram bot...')
        )
        try:
            start_telegram_bot()
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('Bot stopped by user')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Bot error: {e}')
            )
