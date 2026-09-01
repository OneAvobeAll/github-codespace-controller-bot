# GitHub Codespace Controller Telegram Bot

A powerful Telegram bot to create, manage, and control GitHub Codespaces directly from Telegram.

## Features

- 🚀 Create and manage Codespaces for any public repository
- 🔐 Multiple GitHub API token management (add, swap, delete)
- 📦 Docker and non-Docker deployment options
- ⚙️ Custom build commands and start commands
- 🌍 Environment variables configuration
- 💳 Billing and usage limit monitoring
- ⏹️ Start/Stop Codespaces
- 📊 Codespace status monitoring
- 🔧 GitHub API configuration
- 💾 Persistent data storage with MongoDB

## Bot Commands

### Initial Setup
1. `/start` - Initialize the bot and create your first application
2. Create App - Give your app a name
3. Configure App Settings:
   - Set GitHub Repository (clone any public repo)
   - Set Environment Variables
   - Set Build Commands
   - Set Start Commands
   - Enable/Disable Docker Implementation
   - Start the application

### Codespace Management
- **Start Codespace** - Create and launch a new Codespace
- **Stop Codespace** - Gracefully stop a running Codespace
- **View Codespaces** - List all your active Codespaces
- **Codespace Status** - Check current Codespace status

### Configuration
- **Set GitHub API Token** - Add or update GitHub API tokens
- **Manage Tokens** - View, swap, or delete API tokens
- **View Billing** - Check GitHub billing and usage
- **Set Usage Limit** - Configure billing alerts
- **View Settings** - Check current app configuration

## Default Codespace Configuration
- **CPU**: 4-Core
- **RAM**: 16GB
- **Storage**: 32GB
- **Retention**: 30 days

## Installation

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Run: `python main.py`

## Configuration

Copy `.env.example` to `.env` and update:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GITHUB_API_TOKEN=your_github_api_token
MONGODB_URI=your_mongodb_connection_string
WEBHOOK_URL=your_webhook_url (optional for production)
```

## Architecture

- **bot/**: Telegram bot handlers and commands
- **github/**: GitHub API integration
- **codespace/**: Codespace management
- **database/**: MongoDB models and operations
- **config/**: Configuration management
- **utils/**: Utility functions

## Technologies

- Python 3.10+
- python-telegram-bot
- PyGithub
- Motor (Async MongoDB)
- aiohttp

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please open an issue on GitHub.
