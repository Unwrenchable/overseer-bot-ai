# 🔐 Security Setup Guide

This guide explains how to secure your Overseer Bot AI deployment with proper authentication.

## ⚠️ CRITICAL: About .env.example

**The `.env.example` file is a TEMPLATE that is committed to Git.**
- It contains NO actual secrets, only placeholders and instructions
- NEVER put actual passwords, API keys, or private keys in .env.example
- Always create your own `.env` file from this template for actual secrets

## Overview

The Overseer Bot now includes two layers of security:

1. **HTTP Basic Authentication** - Protects the monitoring dashboard and API endpoints
2. **Webhook API Key Authentication** - Secures webhook endpoints for external integrations

## Quick Setup (3 Steps)

### 1. Copy Environment File

**Important:** The `.env.example` is a template. Create your own `.env` file:

```bash
cp .env.example .env
```

The `.env` file is in `.gitignore` and will NOT be committed to Git.

### 2. Generate Strong Credentials

```bash
# Generate a strong admin password
export ADMIN_PASSWORD=$(openssl rand -base64 32)
echo "ADMIN_PASSWORD=$ADMIN_PASSWORD"

# Generate a webhook API key
export WEBHOOK_API_KEY=$(openssl rand -hex 32)
echo "WEBHOOK_API_KEY=$WEBHOOK_API_KEY"
```

### 3. Edit Your .env File (Not .env.example!)

```bash
nano .env  # or use your preferred editor
```

Add your generated values to **your .env file**:

```env
# Admin authentication
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=<paste generated password>

# Webhook API key
WEBHOOK_API_KEY=<paste generated key>
```

**⚠️ Remember:** 
- Edit `.env` (your local copy) - NOT `.env.example` (the template)
- `.env` is in `.gitignore` and safe from accidental commits
- `.env.example` should remain with placeholder values only

## What's Protected?

### Protected with HTTP Basic Auth

These require username/password authentication:

- ✅ Main dashboard: `http://your-server:5000/`
- ✅ Status API: `http://your-server:5000/api/status`
- ✅ Prices API: `http://your-server:5000/api/prices`
- ✅ Jobs API: `http://your-server:5000/api/jobs`
- ✅ Activities API: `http://your-server:5000/api/activities`

### Protected with API Key

These require `Authorization: Bearer <key>` or `X-API-Key: <key>` header (only when `WEBHOOK_API_KEY` is set):

- ✅ Game event webhook: `POST http://your-server:5000/overseer-event`

## Accessing the Dashboard

### Using a Web Browser

When you visit `http://your-server:5000/`, your browser will prompt for credentials:

- **Username**: Your `ADMIN_USERNAME`
- **Password**: Your `ADMIN_PASSWORD`

The browser will remember these credentials for the session.

### Using cURL

```bash
# Access dashboard
curl -u admin:your_password http://your-server:5000/

# Access API endpoints
curl -u admin:your_password http://your-server:5000/api/status
```

### Using Python

```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    'http://your-server:5000/api/status',
    auth=HTTPBasicAuth('admin', 'your_password')
)
print(response.json())
```

## Webhook Integration

### Securing the Game Event Webhook

The bot receives game events at `POST /overseer-event`. If `WEBHOOK_API_KEY` is set in your environment, all webhook requests must include the key:

```bash
# Header formats accepted by the bot:
X-API-Key: your_webhook_api_key
# or
Authorization: Bearer your_webhook_api_key
```

Example:

```bash
curl -X POST https://your-bot.onrender.com/overseer-event \
  -H "Authorization: Bearer your_webhook_api_key" \
  -H "Content-Type: application/json" \
  -d '{"event_type":"perk","player_address":"0x123...","perk_name":"Bloody Mess"}'
```

If `WEBHOOK_API_KEY` is empty, the endpoint accepts all requests (fine for local dev, **not recommended in production**).

### Test Webhook

```bash
curl -X POST http://your-server:5000/overseer-event \
  -H "Authorization: Bearer your_webhook_api_key" \
  -H "Content-Type: application/json" \
  -d '{"event_type":"test","message":"Test event"}'
```

## Deployment Platforms

### ⚠️ Important: Never Commit Secrets!

**For ALL cloud deployments:**
- Use your platform's environment variables feature
- DO NOT put actual secrets in .env files or deployment configs
- DO NOT commit .env or config files with actual keys to Git

### Render.com

**⚠️ Note:** The `render.yaml` file uses `sync: false` for sensitive variables. This means:
- Variables are NOT auto-populated from the file
- You MUST set them manually in Render's dashboard
- This prevents accidental exposure of secrets in Git

**Setup:**
1. Go to your service's **Environment** tab in Render dashboard
2. Add environment variables manually:
   ```
   ADMIN_USERNAME=your_username
   ADMIN_PASSWORD=your_strong_password
   WEBHOOK_API_KEY=your_webhook_key
   ```
3. Click **Save Changes**
4. Your service will automatically restart

**Generate secure values first:**
```bash
openssl rand -base64 32  # For ADMIN_PASSWORD
openssl rand -hex 32     # For WEBHOOK_API_KEY
```

### Heroku

```bash
heroku config:set ADMIN_USERNAME=your_username
heroku config:set ADMIN_PASSWORD=your_strong_password
heroku config:set WEBHOOK_API_KEY=your_webhook_key
```

### Docker

#### Using docker run

```bash
docker run -d \
  -e ADMIN_USERNAME=your_username \
  -e ADMIN_PASSWORD=your_strong_password \
  -e WEBHOOK_API_KEY=your_webhook_key \
  -p 5000:5000 \
  overseer-bot-ai
```

#### Using docker-compose

```yaml
version: '3'
services:
  overseer-bot:
    image: overseer-bot-ai
    env_file:
      - .env
    ports:
      - "5000:5000"
```

### AWS/Cloud

- **AWS**: Use AWS Secrets Manager or Parameter Store
- **Azure**: Use Azure Key Vault
- **GCP**: Use Secret Manager

## Security Best Practices

### ✅ DO

- ✅ Use strong, unique passwords (20+ characters)
- ✅ Generate random API keys using `openssl rand -hex 32`
- ✅ Keep `.env` file secure and never commit it
- ✅ Use HTTPS in production (reverse proxy like nginx)
- ✅ Rotate credentials regularly (every 90 days)
- ✅ Use different credentials for dev/staging/production
- ✅ Limit access to monitoring dashboard to trusted IPs (firewall)
- ✅ Keep webhook API key secret and only share with authorized services

### ❌ DON'T

- ❌ Use default credentials (`admin` / `vault77secure`) in production
- ❌ Commit `.env` file to Git
- ❌ Share credentials in plain text (email, Slack, etc.)
- ❌ Use the same password across environments
- ❌ Expose the monitoring port (5000) directly to the internet without HTTPS

## Webhook API Key (Optional)

The `WEBHOOK_API_KEY` is optional. If not set (empty string), the game event webhook will work without authentication:

```env
WEBHOOK_API_KEY=
```

This can be useful for local development or trusted internal networks. **We strongly recommend setting an API key in production**.

## Troubleshooting

### Problem: "401 Unauthorized" when accessing dashboard

**Solution**: Check your credentials
```bash
# Verify environment variables are set
echo $ADMIN_USERNAME
echo $ADMIN_PASSWORD
```

### Problem: Webhooks failing with 401

**Solution**: Verify API key
1. Check `WEBHOOK_API_KEY` in your `.env` or platform environment
2. Ensure the sending service sends the key in the `Authorization: Bearer <key>` header
3. Test with curl to isolate the issue

### Problem: Browser keeps asking for password

**Solution**: Clear browser cache and cookies for the site

### Problem: Can't remember admin password

**Solution**: 
1. Generate a new password: `openssl rand -base64 32`
2. Update `.env` file with new password
3. Restart the bot

## Testing Your Setup

Run the test suite:

```bash
# Set test credentials
export ADMIN_USERNAME=testadmin
export ADMIN_PASSWORD=testpass123
export WEBHOOK_API_KEY=test_key_123

# Run the bot
python overseer_bot.py
```

In another terminal:

```bash
# Test dashboard access
curl -u testadmin:testpass123 http://localhost:5000/

# Test API
curl -u testadmin:testpass123 http://localhost:5000/api/status

# Test webhook
curl -X POST http://localhost:5000/token-scalper-alert \
  -H "Authorization: Bearer test_key_123" \
  -H "Content-Type: application/json" \
  -d '{"type":"test"}'
```

## Need Help?

- Check the logs: `tail -f overseer_ai.log`
- Review environment variables: `printenv | grep -E 'ADMIN|WEBHOOK'`
- Verify Flask is running: `curl http://localhost:5000/` (should ask for auth)

## 🔒 Remember

**Security is not optional!** Always:
1. Use strong, unique credentials
2. Enable HTTPS in production
3. Keep credentials secret
4. Rotate regularly
5. Monitor access logs

---

**Last updated**: 2026-02-10
