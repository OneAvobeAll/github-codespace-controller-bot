"""Logging configuration"""
import logging
import os
from config import LOG_LEVEL


def setup_logging():
    """
    Configure logging for the application
    """
    # Get log level from config
    log_level = getattr(logging, LOG_LEVEL, logging.INFO)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # File handler
            logging.FileHandler('logs/codespace_bot.log')
        ]
    )
    
    # Set specific loggers
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('motor').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)
