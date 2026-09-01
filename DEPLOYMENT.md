# GitHub Codespace Controller Bot - Deployment Guide

## 🚀 Deployment Options

This guide covers multiple deployment options for the GitHub Codespace Controller Bot.

---

## 1. 🐳 Docker (Recommended)

### Local Docker Deployment

```bash
# Clone repository
git clone https://github.com/OneAvobeAll/github-codespace-controller-bot.git
cd github-codespace-controller-bot

# Copy environment file
cp .env.example .env
# Edit .env with your tokens

# Build and run
docker build -t codespace-bot .
docker run -d --name codespace-bot --env-file .env codespace-bot

# View logs
docker logs -f codespace-bot
```

### Docker Compose (with MongoDB)

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f bot

# Rebuild and restart
docker-compose up -d --build
```

---

## 2. Cloud Deployment

### Railway.app

1. Go to https://railway.app and sign up
2. Click "Create New" - "GitHub Repo"
3. Select this repository
4. Set environment variables in dashboard
5. Deploy automatically

### Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/your-project/codespace-bot
gcloud run deploy codespace-bot --image gcr.io/your-project/codespace-bot
```

### AWS Lambda

Use Serverless Framework for deployment

---

## 3. VPS/Server Deployment

### Ubuntu Server Setup

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3.11 python3-pip git

cd /opt
sudo git clone https://github.com/OneAvobeAll/github-codespace-controller-bot.git
cd github-codespace-controller-bot

sudo python3 -m venv venv
sudo source venv/bin/activate
sudo pip install -r requirements.txt

sudo cp .env.example .env
sudo nano .env  # Edit with your tokens
```

### Setup Systemd Service

Create `/etc/systemd/system/codespace-bot.service`:

```ini
[Unit]
Description=GitHub Codespace Controller Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/github-codespace-controller-bot
Environment="PATH=/opt/github-codespace-controller-bot/venv/bin"
ExecStart=/opt/github-codespace-controller-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable codespace-bot
sudo systemctl start codespace-bot
sudo systemctl status codespace-bot
```

---

## 4. Kubernetes

### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codespace-bot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: codespace-bot
  template:
    metadata:
      labels:
        app: codespace-bot
    spec:
      containers:
      - name: bot
        image: codespace-bot:latest
        env:
        - name: TELEGRAM_BOT_TOKEN
          valueFrom:
            secretKeyRef:
              name: codespace-secrets
              key: telegram-token
        - name: GITHUB_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: codespace-secrets
              key: github-token
        - name: MONGODB_URI
          valueFrom:
            secretKeyRef:
              name: codespace-secrets
              key: mongodb-uri
```

Deploy:
```bash
kubectl create secret generic codespace-secrets \
  --from-literal=telegram-token=your_token
  
kubectl apply -f deployment.yaml
```

---

## Security Checklist

- Use environment variables for secrets
- Enable HTTPS/TLS
- Set up firewall rules
- Regular MongoDB backups
- Keep dependencies updated
- Monitor logs
- Use strong passwords
- Rotate API tokens regularly

---

## Production Checklist

- Configure all environment variables
- Set up MongoDB authentication
- Enable HTTPS
- Configure logging and monitoring
- Set up automated backups
- Test error handling
- Plan scaling strategy

