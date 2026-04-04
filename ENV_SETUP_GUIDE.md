# 🔧 Environment Setup Guide

Complete guide for configuring environment variables in Overseer Bot UI.

---

## 📋 Table of Contents

1. [Understanding .env Files](#understanding-env-files)
2. [Setup Methods](#setup-methods)
3. [Interactive Setup Script](#interactive-setup-script)
4. [Manual Setup by Platform](#manual-setup-by-platform)
5. [Configuration Reference](#configuration-reference)
6. [Security Best Practices](#security-best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Cloud Deployment](#cloud-deployment)

---

## Understanding .env Files

### What is .env?

The `.env` file stores environment variables (configuration settings) for your Overseer Bot instance. It contains sensitive information like API keys and passwords.

### Important Facts

**❌ NO Auto-Management:**
- Overseer Bot does **NOT** auto-create `.env` files
- Overseer Bot does **NOT** auto-update `.env` files
- Configuration is **MANUAL ONLY**

**How it works:**
1. You create `.env` from `.env.example` template
2. You manually edit `.env` with your values
3. Bot reads `.env` at startup using `os.getenv()`
4. Changes require editing `.env` and restarting the bot

**Security:**
- `.env` is in `.gitignore` (never committed to Git)
- `.env.example` is a template (committed, contains no secrets)
- Your actual `.env` should NEVER be shared or committed

---

## Setup Methods

### Quick Comparison

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **setup_env.py** | Beginners, first-time setup | Interactive, validates input, generates secure credentials | Requires Python |
| **Manual** | Advanced users, quick updates | Fast, full control | Requires knowledge of all variables |
| **Cloud Dashboard** | Production deployments | Most secure, managed by platform | Platform-specific |

---

## Interactive Setup Script

### Overview

`setup_env.py` is an interactive Python script that guides you through creating your `.env` file with step-by-step prompts.

### Features

✅ Guided prompts for all configuration options
✅ Automatic secure password/key generation
✅ Input validation
✅ Backup of existing .env files
✅ Load and update existing configurations
✅ Cross-platform (Windows, Mac, Linux)
✅ Secure file permissions (Unix-like systems)

### Usage

#### Basic Usage

```bash
# Navigate to repository directory
cd overseer-bot-ui

# Run the setup script
python setup_env.py
```

#### With Existing .env

If you already have a `.env` file:
```bash
python setup_env.py
# Script will offer to update existing values
# and create a backup of your current file
```

#### Get Help

```bash
python setup_env.py --help
```

### Step-by-Step Walkthrough

1. **Twitter API Credentials**
   - Prompts for all 5 Twitter API keys
   - Get from: https://developer.twitter.com/

2. **Admin Authentication**
   - Set dashboard username
   - Option to auto-generate secure password
   - Displays generated password (save it!)

3. **Webhook Configuration (Optional)**
   - For Token-scalper integration
   - Auto-generates secure API key
   - Can skip if not needed

4. **Server Configuration**
   - Web server port (default: 5000)

5. **Wallet Configuration (Optional)**
   - Solana wallet setup
   - Ethereum/BSC wallet setup
   - Can skip if wallet features not needed

6. **External APIs (Optional)**
   - Overseer-bot-ai integration
   - Token-scalper API integration
   - Polling configuration

7. **AI Features (Optional)**
   - Hugging Face token
   - Can skip if not using AI features

### Example Session

```
==================================================================
  🤖 Overseer Bot UI - Environment Setup
==================================================================

This script will help you create or update your .env configuration file.
You can skip optional sections by answering 'no' to prompts.

⚠️  IMPORTANT: Your .env file contains sensitive credentials.
⚠️  Never commit it to version control or share it publicly.

==================================================================
  Twitter API Credentials
==================================================================
ℹ️  Get these from: https://developer.twitter.com/
ℹ️  You need a Twitter Developer account with API access

Consumer Key (API Key): AbCdEfGh123456789
Consumer Secret (API Secret): 1234567890AbCdEfGhIjKlMnOp
Access Token: 1234567890-AbCdEfGhIjKlMnOp
Access Token Secret: AbCdEfGhIjKlMnOpQrStUvWxYz
Bearer Token: AAAAAAAAAAAAAAAAAAAAAAA...

==================================================================
  Admin Authentication
==================================================================
ℹ️  These credentials protect your monitoring dashboard

Admin username [admin]: admin
Generate a secure password? [Y/n]: y
✅ Generated password: xK9mP2vR8qN4jL6tY3wZ5cH7bF
⚠️  SAVE THIS PASSWORD! You won't see it again in the file.
Press Enter after you've saved the password...

==================================================================
  Webhook Configuration (Optional)
==================================================================
ℹ️  Used for Token-scalper integration and external webhooks

Do you want to configure webhook authentication? [y/N]: n

...

==================================================================
  ✅ Setup Complete!
==================================================================

Next steps:
1. Review your .env file: cat .env (Unix) or type .env (Windows)
2. Install dependencies: pip install -r requirements.txt
3. Run the bot: python overseer_bot.py
4. Access dashboard: http://localhost:5000

⚠️  Remember to keep your .env file secure!
ℹ️  For cloud deployment, set these as environment variables in your platform
```

---

## Manual Setup by Platform

### Linux / macOS

```bash
# Copy template
cp .env.example .env

# Edit with your preferred editor
nano .env
# or
vim .env
# or
code .env  # VS Code

# Set secure permissions
chmod 600 .env

# Verify not tracked by git
git status
```

### Windows (Command Prompt)

```cmd
REM Copy template
copy .env.example .env

REM Edit with Notepad
notepad .env

REM Verify not tracked by git
git status
```

**Security:** Right-click `.env` → Properties → Security → Restrict access to your user only

### Windows (PowerShell)

```powershell
# Copy template
Copy-Item .env.example .env

# Edit with Notepad
notepad .env

# Or VS Code
code .env

# Verify not tracked by git
git status
```

### Verify Setup

After manual setup:

```bash
# Check file exists
ls -la .env     # Linux/Mac
dir .env        # Windows

# Verify it's in .gitignore
git status      # Should NOT show .env

# Test configuration (dry run)
python overseer_bot.py --help  # Should not error on imports
```

---

## Configuration Reference

### Required Variables

These are **mandatory** for the bot to function:

```env
# Twitter API (all 5 required)
CONSUMER_KEY=your_key
CONSUMER_SECRET=your_secret
ACCESS_TOKEN=your_token
ACCESS_SECRET=your_access_secret
BEARER_TOKEN=your_bearer

# Admin credentials (both required)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure_password_here
```

### Optional Variables

#### Wallet Features

```env
ENABLE_WALLET_UI=true  # or false
SOLANA_PRIVATE_KEY=base58_encoded_key
SOLANA_RPC_ENDPOINT=https://api.mainnet-beta.solana.com
ETH_PRIVATE_KEY=hex_key_without_0x
ETH_RPC_ENDPOINT=https://eth.public-rpc.com
BSC_RPC_ENDPOINT=https://bsc-dataseed1.binance.org
```

#### External API Integration

```env
OVERSEER_BOT_AI_URL=https://your-api.onrender.com
OVERSEER_BOT_AI_API_KEY=optional_api_key
TOKEN_SCALPER_URL=https://your-scalper.onrender.com
TOKEN_SCALPER_API_KEY=optional_api_key
POLL_INTERVAL=15  # seconds
REQUEST_TIMEOUT=5  # seconds
```

#### Other Features

```env
WEBHOOK_API_KEY=secure_hex_key  # For incoming webhooks
HUGGING_FACE_TOKEN=hf_token     # For AI responses
PORT=5000                        # Web server port
```

### Default Values

If not specified, these defaults are used:

| Variable | Default Value |
|----------|---------------|
| ADMIN_USERNAME | admin |
| ADMIN_PASSWORD | vault77secure (⚠️ CHANGE THIS!) |
| ENABLE_WALLET_UI | true |
| PORT | 5000 |
| POLL_INTERVAL | 15 |
| REQUEST_TIMEOUT | 5 |
| SOLANA_RPC_ENDPOINT | https://api.mainnet-beta.solana.com |
| ETH_RPC_ENDPOINT | https://eth.public-rpc.com |
| BSC_RPC_ENDPOINT | https://bsc-dataseed1.binance.org |

---

## Security Best Practices

### File Permissions

**Unix/Linux/macOS:**
```bash
# Restrict to owner only
chmod 600 .env

# Verify
ls -la .env
# Should show: -rw------- (owner read/write only)
```

**Windows:**
1. Right-click `.env` → Properties
2. Security tab → Advanced
3. Disable inheritance
4. Remove all users except your account
5. Grant your account "Read" and "Write" only

### Credential Generation

**Strong Passwords:**
```bash
# Linux/macOS/Git Bash
openssl rand -base64 32

# PowerShell
$bytes = New-Object Byte[] 32
[Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
[Convert]::ToBase64String($bytes)

# Python
python -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode()[:32])"

# Or use setup script
python setup_env.py
```

**API Keys:**
```bash
# Linux/macOS/Git Bash
openssl rand -hex 32

# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Security Checklist

- [ ] `.env` file created from template
- [ ] All default passwords changed
- [ ] Strong passwords used (20+ characters)
- [ ] File permissions set to 600 (Unix) or restricted (Windows)
- [ ] `.env` confirmed in `.gitignore`
- [ ] No secrets in `.env.example`
- [ ] Backup of `.env` stored securely (encrypted)
- [ ] Access to `.env` limited to necessary users only

### What NOT to Do

❌ Never commit `.env` to version control
❌ Never share `.env` in chat, email, or screenshots
❌ Never put actual secrets in `.env.example`
❌ Never use default passwords in production
❌ Never store `.env` in cloud storage unencrypted
❌ Never reuse passwords across services

---

## Troubleshooting

### Common Issues

#### Issue: Bot can't find .env file

**Symptoms:**
- Bot uses default values
- Missing configuration warnings

**Solution:**
```bash
# Check if .env exists in correct directory
ls -la .env

# Ensure you're in repository root
pwd
# Should show: /path/to/overseer-bot-ui

# If .env is missing, create it
cp .env.example .env
# or
python setup_env.py
```

#### Issue: Permission denied reading .env

**Symptoms:**
- "Permission denied" errors on startup

**Solution:**
```bash
# Unix/Linux/macOS - Fix permissions
chmod 600 .env

# Windows - Check file properties
# Right-click .env → Properties → Security
```

#### Issue: Invalid credentials

**Symptoms:**
- Twitter API authentication errors
- "Invalid credentials" in logs

**Solution:**
```bash
# Verify credentials in .env
cat .env | grep -E "CONSUMER|ACCESS|BEARER"

# Check for extra spaces or quotes
# Correct: CONSUMER_KEY=abc123
# Wrong:   CONSUMER_KEY="abc123"  (remove quotes)
# Wrong:   CONSUMER_KEY = abc123  (remove spaces around =)

# Test credentials separately
python -c "import tweepy; print(tweepy.Client(bearer_token='YOUR_TOKEN').get_me())"
```

#### Issue: Changes not taking effect

**Symptoms:**
- Modified .env but bot behavior unchanged

**Solution:**
```bash
# Bot reads .env only at startup
# You must restart the bot after changes:

# Stop the bot (Ctrl+C)
# Edit .env
nano .env

# Restart the bot
python overseer_bot.py
```

#### Issue: setup_env.py fails

**Symptoms:**
- Script crashes or errors

**Solution:**
```bash
# Ensure Python 3.6+
python --version

# Run from repository root
pwd
ls -la .env.example  # Should exist

# Check Python path
which python  # Unix
where python  # Windows

# Try with explicit Python 3
python3 setup_env.py
```

### Getting Help

If you encounter issues:

1. **Check logs:**
   ```bash
   tail -f overseer_ai.log
   grep ERROR overseer_ai.log
   ```

2. **Verify .env format:**
   ```bash
   # Each line should be: KEY=value
   # No spaces around =
   # No quotes around values
   # No trailing spaces
   ```

3. **Test minimal configuration:**
   ```bash
   # Create minimal .env with only required vars
   python setup_env.py
   # Enter only Twitter credentials and admin auth
   # Skip all optional sections
   ```

4. **Compare with example:**
   ```bash
   # Check for missing variables
   diff .env.example .env
   ```

---

## Cloud Deployment

### Important: Don't Use .env Files in Production!

For cloud platforms (Render, Heroku, Railway, AWS, etc.), **do not use .env files**. Instead, set environment variables through your platform's interface.

### Platform-Specific Instructions

#### Render.com

1. Go to your service dashboard
2. Navigate to **Environment** tab
3. Click **Add Environment Variable**
4. Add each variable:
   - Key: `CONSUMER_KEY`
   - Value: `your_actual_key`
5. Click **Save Changes**
6. Service will automatically redeploy

**Example:**
```
CONSUMER_KEY = abc123def456
CONSUMER_SECRET = xyz789uvw012
...
```

#### Heroku

**Via Dashboard:**
1. Go to app → Settings → Config Vars
2. Click **Reveal Config Vars**
3. Add each variable

**Via CLI:**
```bash
heroku config:set CONSUMER_KEY=abc123
heroku config:set CONSUMER_SECRET=xyz789
# ... etc for all variables

# View all config vars
heroku config

# Restart after adding vars
heroku restart
```

#### Railway

1. Go to project → Variables tab
2. Click **+ New Variable**
3. Add each variable
4. Save (auto-deploys)

#### AWS (Multiple Options)

**Option 1: ECS Task Definitions**
```json
{
  "environment": [
    {"name": "CONSUMER_KEY", "value": "abc123"},
    {"name": "CONSUMER_SECRET", "value": "xyz789"}
  ]
}
```

**Option 2: AWS Parameter Store**
```bash
aws ssm put-parameter \
  --name "/overseer-bot/CONSUMER_KEY" \
  --value "abc123" \
  --type "SecureString"
```

**Option 3: AWS Secrets Manager**
```bash
aws secretsmanager create-secret \
  --name overseer-bot-credentials \
  --secret-string '{"CONSUMER_KEY":"abc123",...}'
```

#### Docker

**Option 1: docker run with --env-file**
```bash
docker run --env-file .env overseer-bot
```

**Option 2: docker-compose**
```yaml
services:
  bot:
    image: overseer-bot
    env_file: .env
    # Or inline:
    environment:
      CONSUMER_KEY: abc123
      CONSUMER_SECRET: xyz789
```

**Security Note:** For Docker, keep `.env` on host only, never in image!

### Cloud Best Practices

✅ Use platform's secret management
✅ Rotate credentials regularly
✅ Use separate credentials per environment (dev/staging/prod)
✅ Enable audit logging
✅ Use service accounts where possible
✅ Never include secrets in `render.yaml`, `heroku.yml`, etc.

❌ Never commit secrets to Git
❌ Never use .env files in containers
❌ Never store secrets in plain text files on servers

---

## Summary

### Quick Reference

| Task | Command |
|------|---------|
| Interactive setup | `python setup_env.py` |
| Manual copy | `cp .env.example .env` |
| Edit (Unix) | `nano .env` or `vim .env` |
| Edit (Windows) | `notepad .env` |
| Set permissions | `chmod 600 .env` |
| Generate password | `openssl rand -base64 32` |
| Generate API key | `openssl rand -hex 32` |
| Verify git ignore | `git status` (should not show .env) |

### Key Takeaways

1. ✅ `.env` is **MANUAL** - no auto-creation or auto-updates
2. ✅ Use `setup_env.py` for easy interactive setup
3. ✅ Always create `.env` from `.env.example` template
4. ✅ Never commit `.env` to version control
5. ✅ Use platform environment variables for cloud deployments
6. ✅ Set restrictive file permissions
7. ✅ Generate strong passwords and API keys
8. ✅ Restart bot after `.env` changes

---

## Related Documentation

- [README.md](./README.md) - Project overview and quick start
- [COMPLETE_SETUP_GUIDE.md](./COMPLETE_SETUP_GUIDE.md) - Full setup walkthrough
- [DOCUMENTATION.md](./DOCUMENTATION.md) - Complete technical documentation
- [SECURITY_GUIDE.md](./SECURITY_GUIDE.md) - Security best practices
- [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) - Production deployment guide

---

<div align="center">

**🔒 Keep your credentials secure! 🔒**

*Never commit `.env` • Always use strong passwords • Regularly rotate secrets*

</div>
