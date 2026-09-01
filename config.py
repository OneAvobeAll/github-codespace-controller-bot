"""
Configuration settings for the bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')

# GitHub
GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN', '')

# MongoDB
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/codespace_bot')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'codespace_bot')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Codespace defaults
DEFAULT_CPU_CORES = 4
DEFAULT_RAM_GB = 16
DEFAULT_STORAGE_GB = 32
DEFAULT_RETENTION_DAYS = 30

# Supported machine types
MACHINE_TYPES = {
    'small': {'cpu': 2, 'ram': 8, 'storage': 32},
    'medium': {'cpu': 4, 'ram': 16, 'storage': 32},
    'large': {'cpu': 8, 'ram': 32, 'storage': 64},
    'xlarge': {'cpu': 16, 'ram': 64, 'storage': 128},
}
