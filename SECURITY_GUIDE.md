# 🔐 Security Setup Guide

This guide explains how to secure your Overseer Bot AI deployment with proper authentication.

## Overview

The Overseer Bot now includes two layers of security:

1. **HTTP Basic Authentication** - Protects the monitoring dashboard and API endpoints
2. **Webhook API Key Authentication** - Secures webhook endpoints for external integrations

## Quick Setup (3 Steps)

### 1. Copy Environment File

```bash
cp .env.example .env
```

### 2. Generate Strong Credentials

```bash
# Generate a strong admin password
export ADMIN_PASSWORD=$(openssl rand -base64 32)
echo "ADMIN_PASSWORD=$ADMIN_PASSWORD"

# Generate a webhook API key
export WEBHOOK_API_KEY=$(openssl rand -hex 32)
echo "WEBHOOK_API_KEY=$WEBHOOK_API_KEY"
```

### 3. Edit .env File

```bash
nano .env  # or use your preferred editor
```

Add your generated values:

```env
# Admin authentication
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=<paste generated password>

# Webhook API key
WEBHOOK_API_KEY=<paste generated key>
```

## What's Protected?

### Protected with HTTP Basic Auth

These require username/password authentication:

- ✅ Main dashboard: `http://your-server:5000/`
- ✅ Status API: `http://your-server:5000/api/status`
- ✅ Prices API: `http://your-server:5000/api/prices`
- ✅ Jobs API: `http://your-server:5000/api/jobs`
- ✅ Activities API: `http://your-server:5000/api/activities`

### Protected with API Key

These require `Authorization` header with API key:

- ✅ Webhook: `POST http://your-server:5000/overseer-event`
- ✅ Token-scalper alerts: `POST http://your-server:5000/token-scalper-alert`

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

## Webhook Integration with Token-scalper

### Configure Token-scalper

Edit Token-scalper's `config.json`:

```json
{
  "social_media": {
    "enabled": true,
    "overseer_bot_enabled": true,
    "overseer_webhook_url": "http://your-overseer-bot:5000/token-scalper-alert",
    "overseer_api_key": "your_webhook_api_key_here"
  }
}
```

**Important**: Use the same `WEBHOOK_API_KEY` value from your Overseer Bot's `.env` file.

### Test Webhook

```bash
# Test with API key
curl -X POST http://your-server:5000/token-scalper-alert \
  -H "Authorization: Bearer your_webhook_api_key" \
  -H "Content-Type: application/json" \
  -d '{"type":"test","message":"Test alert"}'
```

## Deployment Platforms

### Render.com

1. Go to your service's **Environment** tab
2. Add environment variables:
   ```
   ADMIN_USERNAME=your_username
   ADMIN_PASSWORD=your_strong_password
   WEBHOOK_API_KEY=your_webhook_key
   ```
3. Click **Save Changes**
4. Your service will automatically restart

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

## Backward Compatibility

### Webhook API Key (Optional)

The `WEBHOOK_API_KEY` is optional. If not set (empty string), webhooks will work without authentication:

```env
WEBHOOK_API_KEY=
```

This maintains backward compatibility with existing Token-scalper integrations. However, **we strongly recommend setting an API key in production**.

## Troubleshooting

### Problem: "401 Unauthorized" when accessing dashboard

**Solution**: Check your credentials
```bash
# Verify environment variables are set
echo $ADMIN_USERNAME
echo $ADMIN_PASSWORD
```

### Problem: Token-scalper webhooks failing with 401

**Solution**: Verify API keys match
1. Check Overseer Bot's `WEBHOOK_API_KEY` in `.env`
2. Check Token-scalper's `overseer_api_key` in `config.json`
3. They must be identical

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
