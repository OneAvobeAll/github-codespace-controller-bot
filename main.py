"""
Main entry point for the GitHub Codespace Controller Telegram Bot
"""
import logging
import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from bot.handlers import start_handler, codespace_handler, github_handler, settings_handler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main():
    """Start the bot"""
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

    # Create application
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_handler.start_command))
    application.add_handler(CommandHandler("help", start_handler.help_command))
    application.add_handler(CommandHandler("myapps", start_handler.list_apps))
    application.add_handler(CommandHandler("settings", settings_handler.settings_command))
    
    # Add callback query handlers
    application.add_handler(CallbackQueryHandler(start_handler.handle_create_app, pattern="^create_app$"))
    application.add_handler(CallbackQueryHandler(start_handler.handle_main_menu, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(github_handler.set_github_repo, pattern="^set_repo_"))
    application.add_handler(CallbackQueryHandler(github_handler.set_env_vars, pattern="^set_env_"))
    application.add_handler(CallbackQueryHandler(github_handler.set_build_cmd, pattern="^set_build_"))
    application.add_handler(CallbackQueryHandler(github_handler.set_start_cmd, pattern="^set_start_"))
    application.add_handler(CallbackQueryHandler(github_handler.set_docker, pattern="^set_docker_"))
    application.add_handler(CallbackQueryHandler(codespace_handler.start_codespace, pattern="^start_codespace_"))
    application.add_handler(CallbackQueryHandler(codespace_handler.stop_codespace, pattern="^stop_codespace_"))
    application.add_handler(CallbackQueryHandler(codespace_handler.check_status, pattern="^check_status_"))
    application.add_handler(CallbackQueryHandler(settings_handler.manage_tokens, pattern="^manage_tokens"))
    application.add_handler(CallbackQueryHandler(settings_handler.view_billing, pattern="^view_billing"))
    
    # Add message handlers for text input
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start_handler.handle_user_input))

    logger.info("🤖 GitHub Codespace Controller Bot started successfully!")
    
    # Start the bot
    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
