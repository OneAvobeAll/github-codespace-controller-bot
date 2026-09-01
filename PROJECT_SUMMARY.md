# GitHub Codespace Controller Telegram Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MongoDB](https://img.shields.io/badge/MongoDB-green.svg)](https://www.mongodb.com/)

🚀 **A powerful Telegram bot to create, manage, and control GitHub Codespaces directly from Telegram.**

## 🎯 Features

### 🔧 Application Management
- ✅ Create and manage applications with custom configurations
- ✅ Clone any public GitHub repository
- ✅ Configure custom build and start commands
- ✅ Set environment variables for applications
- ✅ Support both Docker and non-Docker deployments
- ✅ Store and manage application settings

### ☁️ Codespace Control
- ✅ **Start Codespaces** - Automatically forks repo and launches Codespace
  - 4-Core CPU (customizable: 2, 4, 8, or 16-core)
  - 16GB RAM (customizable: 8, 16, 32, or 64GB)
  - 32GB Storage (customizable: 32, 64, or 128GB)
- ✅ **Stop Codespaces** - Gracefully shutdown running Codespaces
- ✅ **Monitor Status** - Check real-time Codespace status
- ✅ **Get URLs** - Direct access links to Codespace web environments

### 🔐 GitHub API Token Management
- ✅ Add multiple GitHub API tokens
- ✅ Switch between active tokens
- ✅ Delete unused tokens
- ✅ Token validation and security
- ✅ Support for Personal Access Tokens and OAuth tokens

### 💳 Billing & Usage Monitoring
- ✅ View GitHub billing information
- ✅ Track Codespace usage and costs
- ✅ Set monthly usage limits
- ✅ Receive billing alerts
- ✅ Usage statistics per application

### 🛠️ Technical Features
- ✅ **MongoDB Integration** - Persistent data storage
- ✅ **Async Operations** - Non-blocking bot operations
- ✅ **Error Handling** - Comprehensive error management
- ✅ **Logging** - Detailed activity logs
- ✅ **Docker Support** - Easy deployment with Docker Compose
- ✅ **Scalable Architecture** - Ready for production deployment

## 📋 Bot Commands

### Primary Commands
```
/start          - Initialize bot and show main menu
/myapps         - List all your applications
/settings       - Open settings and configuration
/help           - Display help information
```

### Interactive Buttons

**Main Menu:**
- ✨ Create New App
- 📱 My Applications
- ⚙️ Settings
- ❓ Help

**Application Configuration:**
- 🔗 Set Repository
- 🌍 Set Environment Variables
- 🔨 Set Build Command
- ▶️ Set Start Command
- 🐳 Docker Implementation
- ✅ Review & Start

**Codespace Management:**
- ▶️ Start Codespace
- ⏹️ Stop Codespace
- 📊 Check Status
- 🌐 Open in Browser

**Settings:**
- 🔑 Manage GitHub Tokens
- 💳 View Billing
- ⏰ Usage Limits
- 🔔 Notifications

## 🏗️ Architecture

```
github-codespace-controller-bot/
├── bot/
│   └── handlers/
│       ├── start_handler.py       # /start command and menu
│       ├── github_handler.py      # GitHub configuration
│       ├── codespace_handler.py   # Codespace operations
│       └── settings_handler.py    # Settings management
├── database/
│   ├── models.py                  # Data models
│   └── db.py                      # MongoDB operations
├── github_api/
│   └── github_manager.py          # GitHub API integration
├── utils/
│   ├── helpers.py                 # Utility functions
│   └── logger.py                  # Logging setup
├── main.py                        # Bot entry point
├── config.py                      # Configuration
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker container
├── docker-compose.yml             # Docker Compose config
├── INSTALL.md                     # Installation guide
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MongoDB (local or cloud)
- GitHub Personal Access Token
- Telegram Bot Token

### Installation (Docker - Recommended)

1. **Clone repository**
   ```bash
   git clone https://github.com/OneAvobeAll/github-codespace-controller-bot.git
   cd github-codespace-controller-bot
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your tokens
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

### Installation (Local)

1. **Clone repository**
   ```bash
   git clone https://github.com/OneAvobeAll/github-codespace-controller-bot.git
   cd github-codespace-controller-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your tokens
   ```

5. **Run bot**
   ```bash
   python main.py
   ```

## 🔑 Getting Required Tokens

### Telegram Bot Token
1. Open Telegram → Search `@BotFather`
2. Send `/newbot` and follow prompts
3. Copy token to `.env` as `TELEGRAM_BOT_TOKEN`

### GitHub Personal Access Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Required scopes:
   - `repo` - Repository access
   - `codespace` - Codespace management
   - `user` - User profile
4. Copy token to `.env` as `GITHUB_API_TOKEN`

### MongoDB Connection String

**Cloud (MongoDB Atlas):**
```
mongodb+srv://username:password@cluster.mongodb.net/codespace_bot?retryWrites=true&w=majority
```

**Local MongoDB:**
```
mongodb://localhost:27017/codespace_bot
```

Add to `.env` as `MONGODB_URI`

## 📊 Workflow Example

```
1. User: /start
2. Bot: Shows main menu
3. User: Clicks "Create New App"
4. User: Enters app name (e.g., "My Node App")
5. User: Configures:
   - Repository: https://github.com/user/repo
   - Environment: NODE_ENV=production
   - Build: npm install && npm run build
   - Start: npm start
   - Docker: No
6. User: Clicks "Start"
7. Bot: Forks repository to user's GitHub
8. Bot: Creates 4-core 16GB Codespace
9. Bot: Runs build commands
10. Bot: Runs start commands
11. Bot: Sends Codespace URL
12. User: Opens Codespace in browser
13. User: Works on code
14. User: Clicks "Stop" when done
15. Bot: Stops Codespace gracefully
```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| TELEGRAM_BOT_TOKEN | ✅ | - | Telegram bot token from BotFather |
| GITHUB_API_TOKEN | ✅ | - | GitHub personal access token |
| MONGODB_URI | ✅ | - | MongoDB connection string |
| DATABASE_NAME | ❌ | codespace_bot | MongoDB database name |
| LOG_LEVEL | ❌ | INFO | Logging level (DEBUG/INFO/WARNING/ERROR) |
| DEBUG | ❌ | False | Debug mode (True/False) |

### Codespace Machine Types

| Type | CPU | RAM | Storage | Cost/Hour |
|------|-----|-----|---------|----------|
| small | 2-Core | 8GB | 32GB | $0.42 |
| medium | 4-Core | 16GB | 32GB | $1.08 |
| large | 8-Core | 32GB | 64GB | $2.16 |
| xlarge | 16-Core | 64GB | 128GB | $4.32 |

## 🐳 Docker Compose Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f bot

# Access MongoDB
docker exec -it codespace-bot-db mongosh -u root -p password

# Rebuild containers
docker-compose up -d --build

# Remove all data
docker-compose down -v
```

## 🔍 Monitoring

### View Bot Logs
```bash
# Local
tail -f logs/codespace_bot.log

# Docker
docker-compose logs -f bot
```

### Check MongoDB
```bash
# Connect to MongoDB
mongosh "mongodb+srv://username:password@cluster.mongodb.net"

# List databases
show dbs

# Use database
use codespace_bot

# View collections
show collections
```

## 📈 Scaling

### For Multiple Instances
1. Use MongoDB Atlas for centralized database
2. Deploy bot on different servers
3. Each bot instance uses same database
4. Users can access their apps from any bot instance

### Performance Tips
- Use MongoDB Atlas for better performance
- Cache frequently accessed data
- Limit API calls with rate limiting
- Use async operations for long tasks

## 🐛 Troubleshooting

### Bot doesn't respond
```
1. Check TELEGRAM_BOT_TOKEN is correct
2. Verify bot is running: docker-compose ps
3. Check logs: docker-compose logs bot
4. Restart bot: docker-compose restart bot
```

### MongoDB connection fails
```
1. Verify MONGODB_URI is correct
2. Check MongoDB service: docker-compose logs mongodb
3. Test connection: mongosh "$MONGODB_URI"
4. Restart MongoDB: docker-compose restart mongodb
```

### GitHub API errors
```
1. Verify GITHUB_API_TOKEN is valid
2. Check token scopes at https://github.com/settings/tokens
3. Verify token hasn't expired
4. Test GitHub API: curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user
```

### Codespace creation fails
```
1. Verify repository is public
2. Check GitHub token has 'codespace' scope
3. Verify GitHub account has Codespaces enabled
4. Check GitHub API rate limits: curl -H "Authorization: Bearer $TOKEN" https://api.github.com/rate_limit
```

## 📚 Documentation

- [Installation Guide](INSTALL.md)
- [Configuration](config.py)
- [API Models](database/models.py)
- [GitHub Integration](github_api/github_manager.py)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [Motor](https://github.com/mongodb-labs/motor) (Async MongoDB driver)
- [MongoDB](https://www.mongodb.com/)

## 📧 Support

For issues, questions, or suggestions:

1. Check [existing issues](https://github.com/OneAvobeAll/github-codespace-controller-bot/issues)
2. Create a [new issue](https://github.com/OneAvobeAll/github-codespace-controller-bot/issues/new)
3. Include:
   - Clear description of the problem
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Relevant logs and environment info

## 🎉 Roadmap

- [ ] Web dashboard for app management
- [ ] Scheduled Codespace creation
- [ ] Custom Dockerfile support
- [ ] Multiple repository support per app
- [ ] Advanced billing analytics
- [ ] Team collaboration features
- [ ] Slack bot integration
- [ ] Discord bot integration

## 📊 Statistics

- 📦 **Dependencies**: 10+ (lightweight)
- 📝 **Lines of Code**: 2000+
- 🔧 **Handlers**: 4 (modular architecture)
- 💾 **Collections**: 4 (MongoDB)
- 🌍 **Supported Regions**: All (GitHub Codespaces)

---

**Made with ❤️ by [OneAvobeAll](https://github.com/OneAvobeAll)**

⭐ Star this repo if you find it useful!
