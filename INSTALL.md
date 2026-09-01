# GitHub Codespace Controller Telegram Bot - Installation & Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MongoDB (local or cloud)
- GitHub Personal Access Token
- Telegram Bot Token

### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OneAvobeAll/github-codespace-controller-bot.git
   cd github-codespace-controller-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add:
   - `TELEGRAM_BOT_TOKEN`: Get from BotFather on Telegram
   - `GITHUB_API_TOKEN`: Create at https://github.com/settings/tokens
   - `MONGODB_URI`: Your MongoDB connection string

5. **Run the bot**
   ```bash
   python main.py
   ```

### Option 2: Docker Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OneAvobeAll/github-codespace-controller-bot.git
   cd github-codespace-controller-bot
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your tokens

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Check logs**
   ```bash
   docker-compose logs -f bot
   ```

### Option 3: Non-Docker Installation (Production)

#### Setup MongoDB
```bash
# Using MongoDB Atlas (Cloud)
# 1. Create account at https://www.mongodb.com/cloud/atlas
# 2. Create a cluster
# 3. Copy connection string
# 4. Add to .env as MONGODB_URI
```

#### Setup Systemd Service (Linux)

Create `/etc/systemd/system/codespace-bot.service`:
```ini
[Unit]
Description=GitHub Codespace Controller Bot
After=network.target

[Service]
Type=simple
User=codespace-bot
WorkingDirectory=/opt/codespace-bot
Environment="PATH=/opt/codespace-bot/venv/bin"
ExecStart=/opt/codespace-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable codespace-bot
sudo systemctl start codespace-bot
```

## 🔐 Getting Required Tokens

### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow the prompts
4. Copy the token and add to `.env`

### GitHub Personal Access Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Required scopes:
   - `repo` - Full repository access
   - `codespace` - Codespace access
   - `user` - User profile access
4. Copy the token and add to `.env`

### MongoDB Connection String

**MongoDB Atlas (Recommended for Cloud):**
```
mongodb+srv://username:password@cluster.mongodb.net/codespace_bot?retryWrites=true&w=majority
```

**Local MongoDB:**
```
mongodb://localhost:27017/codespace_bot
```

## 📊 Bot Features

### Application Management
- ✨ Create new applications
- 📝 Configure repository URLs
- 🌍 Set environment variables
- 🔨 Configure build commands
- ▶️ Set start commands
- 🐳 Choose Docker implementation

### Codespace Control
- ▶️ Start new Codespaces
- ⏹️ Stop running Codespaces
- 📊 Check Codespace status
- 🔗 Get Codespace web URLs

### GitHub API Management
- 🔐 Add multiple GitHub tokens
- 🔄 Switch between tokens
- 🗑️ Delete tokens
- 📊 View billing information
- ⚠️ Set usage alerts

## 🐳 Docker Compose Usage

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f bot
```

### Access MongoDB
```bash
docker exec -it codespace-bot-db mongosh -u root -p password
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| TELEGRAM_BOT_TOKEN | Telegram bot token | ✅ |
| GITHUB_API_TOKEN | GitHub personal access token | ✅ |
| MONGODB_URI | MongoDB connection string | ✅ |
| DATABASE_NAME | Database name | ❌ (default: codespace_bot) |
| LOG_LEVEL | Logging level | ❌ (default: INFO) |
| DEBUG | Debug mode | ❌ (default: False) |

### Codespace Machine Types
- **small**: 2-Core, 8GB RAM, 32GB Storage
- **medium**: 4-Core, 16GB RAM, 32GB Storage (Default)
- **large**: 8-Core, 32GB RAM, 64GB Storage
- **xlarge**: 16-Core, 64GB RAM, 128GB Storage

## 🆘 Troubleshooting

### Bot doesn't respond to /start
1. Check `TELEGRAM_BOT_TOKEN` is correct
2. Verify bot is running: `python main.py`
3. Check logs for errors

### MongoDB connection fails
1. Verify `MONGODB_URI` is correct
2. Check MongoDB service is running
3. Verify credentials if using authentication

### GitHub API errors
1. Verify `GITHUB_API_TOKEN` is valid
2. Check token has required scopes
3. Verify token hasn't expired

### Codespace creation fails
1. Check repository is public
2. Verify GitHub token permissions
3. Check GitHub account has Codespaces enabled

## 📚 API Documentation

### Bot Commands
- `/start` - Initialize bot and show main menu
- `/help` - Show help information
- `/myapps` - List user applications
- `/settings` - Open settings menu

### Inline Buttons
All features are accessible through inline buttons in Telegram

## 🚀 Deployment

### Deploy to Heroku (if available)
```bash
heroku create your-app-name
heroku addons:create mongolab
git push heroku main
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set GITHUB_API_TOKEN=your_token
```

### Deploy to Railway.app
1. Connect GitHub repository
2. Set environment variables
3. Deploy

### Deploy to DigitalOcean/VPS
```bash
# SSH into server
ssh root@your_ip

# Clone repo
git clone https://github.com/OneAvobeAll/github-codespace-controller-bot.git
cd github-codespace-controller-bot

# Install dependencies
pip install -r requirements.txt

# Setup systemd service (see above)
# Start bot
sudo systemctl start codespace-bot
```

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with details
3. Include error logs and environment info

## 🔄 Workflow Summary

1. **User sends /start**
2. **Bot shows main menu**
3. **User clicks "Create New App"**
4. **User enters app name**
5. **Bot shows configuration menu**
6. **User configures:**
   - GitHub repository URL
   - Environment variables
   - Build commands
   - Start commands
   - Docker implementation
7. **User clicks "Review & Start"**
8. **Bot forks repository**
9. **Bot creates Codespace with 4-Core, 16GB, 32GB**
10. **Bot runs build commands**
11. **Bot runs start commands**
12. **Bot sends Codespace URL to user**
13. **User can stop Codespace when done**

---

**Made with ❤️ by OneAvobeAll**
