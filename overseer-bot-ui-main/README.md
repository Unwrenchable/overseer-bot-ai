# ☢️ Overseer Bot AI - Vault 77

<div align="center">

![Vault-Tec](https://img.shields.io/badge/VAULT--TEC-77-green?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-OPERATIONAL-green?style=for-the-badge)
![Python](https://img.shields.io/badge/PYTHON-3.9%2B-blue?style=for-the-badge)

**A Fallout-themed Twitter bot with cryptocurrency intelligence**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Deployment](#-deployment)

</div>

---

## 📖 About

**Overseer Bot AI** is a sophisticated Twitter automation bot that combines:
- 🎮 **Game Promotion** - Promotes "Atomic Fizz Caps" game
- 💰 **Crypto Intelligence** - Real-time token price monitoring & alerts
- 🛡️ **Token Safety Analysis** - Detects honeypots and scams
- 🎭 **Fallout Personality** - Immersive Vault-Tec themed content
- 📊 **Monitoring Dashboard** - Beautiful web UI for oversight

## ✨ Features

### Twitter Automation
- ✅ Automated broadcasts every 2-4 hours with varied content
- ✅ Responds to mentions every 15-30 minutes
- ✅ Hunts and retweets relevant content hourly
- ✅ Daily diagnostic reports at 8 AM
- ✅ AI-powered contextual responses (optional Hugging Face)

### Cryptocurrency Intelligence
- 📈 Real-time price monitoring (SOL, BTC, ETH)
- 🚨 Automated price alerts (3-5% threshold movements)
- 📊 Market summaries 3x daily (8 AM, 2 PM, 8 PM)
- 🔍 Token safety checker (honeypot detection, tax analysis)
- 💎 CoinGecko fallback for geo-restricted exchanges

### Event Integration
- 🎮 Game event webhooks (perks, quests, swaps, NFTs, level-ups)
- 💰 Token-scalper alerts (rug pulls, high potential, airdrops)
- 🌐 MoonPay funding notifications
- 🗺️ Location claim announcements
- 🔗 **External API integration** (overseer-bot-ai, Token-scalper) - NEW!
- 📡 **Unified alert dashboard** with health monitoring - NEW!

### Monitoring Dashboard
- 🖥️ Beautiful Vault-Tec themed web UI with **tabbed interface**
- 💰 **Wallet integration** (Solana, Ethereum, BSC) - NEW!
- 🔧 **Manual control tools** (token checker, price checker) - NEW!
- 📊 Real-time status, uptime, and scheduler jobs
- 💹 Live token prices with 24h changes
- 📝 Activity log (last 50 events)
- 🔒 HTTP Basic Auth protected
- 🔌 RESTful API endpoints

## 🗣️ How to Interact with the Bot

**Mention the bot on Twitter:** `@OverseerBot` (replace with your bot handle)

### Quick Examples

**Check Token Prices:**
```
@OverseerBot what's SOL price?
@OverseerBot how much is Bitcoin?
```

**Token Safety Check:**
```
@OverseerBot is 0x1234567890123456789012345678901234567890 safe?
```

**General Queries:**
```
@OverseerBot what's happening in the wasteland?
```

**Response Time:** 15-30 minutes (bot checks mentions periodically)

📖 **Full interaction guide:** [USER_INTERACTION_GUIDE.md](./USER_INTERACTION_GUIDE.md)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Twitter Developer Account ([Get API keys](https://developer.twitter.com/))
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Unwrenchable/overseer-bot-ai.git
cd overseer-bot-ai

# 2. Install dependencies
pip install -r requirements.txt

# Note: Production deployments use requirements-lock.txt for faster builds
# See DEPENDENCIES.md for details on dependency management

# 3. Configure environment variables
# Option A: Interactive setup (recommended)
python setup_env.py

# Option B: Manual setup
cp .env.example .env
# Then edit .env with your Twitter API keys and credentials

# 4. Run the bot
python overseer_bot.py
```

> 💡 **Tip:** Use `python setup_env.py` for guided configuration with automatic secure credential generation!

### Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

Login with credentials from your `.env` file:
- **Username:** Value of `ADMIN_USERNAME` (default: `admin`)
- **Password:** Value of `ADMIN_PASSWORD` (**⚠️ CHANGE THIS!**)

**New UI Features:**
- 📊 **Monitoring Tab** - Real-time bot status and automated tasks
- 💰 **Wallet Tab** - View wallet balances (Solana, ETH, BSC)
- 🔧 **Tools Tab** - Manual token safety checker & price checker
- 🔗 **API Tab** - Complete API documentation
- 🚨 **Alerts Section** - Live alerts from external systems (NEW!)
- 🔗 **Health Monitoring** - External system status tracking (NEW!)

📖 **See [WALLET_UI_GUIDE.md](./WALLET_UI_GUIDE.md) for complete wallet setup and usage**

📖 **See [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) for external API integration setup**

## ⚙️ Configuration

### 📝 About .env Files - IMPORTANT!

**🚨 Environment variables in overseer-bot-ui are MANUAL only:**

- ✅ `.env.example` is a **TEMPLATE** committed to Git (contains no secrets)
- ✅ `.env` must be **MANUALLY CREATED** by you (it's in `.gitignore` and never committed)
- ❌ The bot does **NOT** auto-create or auto-update `.env` files
- ❌ There is **NO** automatic configuration management at runtime

**What this means:**
- You must manually copy `.env.example` to `.env` and edit it yourself
- Changes to configuration require manually editing the `.env` file
- The bot reads environment variables at startup using `os.getenv()`
- For cloud deployments (Render, Heroku, etc.), use platform environment variables

### 🛠️ Setup Environment Variables

**Choose your setup method:**

#### Option 1: Interactive Setup Script (Recommended for beginners)

The easiest way to create your `.env` file with guided prompts:

```bash
# Run the interactive setup script
python setup_env.py
```

The script will:
- ✅ Guide you through all required and optional settings
- ✅ Generate secure passwords and API keys
- ✅ Validate your inputs
- ✅ Create a properly formatted `.env` file
- ✅ Set appropriate file permissions

#### Option 2: Manual Setup

**Platform-specific instructions:**

<details>
<summary><strong>🐧 Linux / macOS</strong></summary>

```bash
# Copy the template
cp .env.example .env

# Edit with your preferred editor
nano .env
# or
vim .env
# or
code .env  # VS Code

# Set secure permissions (owner read/write only)
chmod 600 .env

# Verify it's not tracked by git
git status  # Should not show .env
```
</details>

<details>
<summary><strong>🪟 Windows (Command Prompt)</strong></summary>

```cmd
REM Copy the template
copy .env.example .env

REM Edit with Notepad
notepad .env

REM Or use any text editor you prefer
REM - Notepad++
REM - VS Code
REM - Sublime Text

REM Verify it's not tracked by git
git status
```

**Security Note:** On Windows, right-click `.env` → Properties → Security tab → Restrict access to your user account only.
</details>

<details>
<summary><strong>🪟 Windows (PowerShell)</strong></summary>

```powershell
# Copy the template
Copy-Item .env.example .env

# Edit with Notepad
notepad .env

# Or use VS Code
code .env

# Verify it's not tracked by git
git status
```
</details>

<details>
<summary><strong>☁️ Cloud Platforms (Render, Heroku, Railway, etc.)</strong></summary>

**Do NOT use .env files on cloud platforms!**

Instead, set environment variables in your platform's dashboard:

- **Render.com**: Dashboard → Environment → Environment Variables
- **Heroku**: Dashboard → Settings → Config Vars (or use `heroku config:set VAR=value`)
- **Railway**: Dashboard → Variables tab
- **AWS**: Use Parameter Store, Secrets Manager, or ECS task definitions
- **Docker**: Use `--env-file` flag or docker-compose `env_file` directive

See `.env.example` for the complete list of variables and their descriptions.
</details>

### 📋 Required Configuration Values

Edit your `.env` file with these **required** values:

```env
# Twitter API Credentials (Required)
CONSUMER_KEY=your_twitter_consumer_key
CONSUMER_SECRET=your_twitter_consumer_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_SECRET=your_twitter_access_secret
BEARER_TOKEN=your_twitter_bearer_token

# Dashboard Authentication (Required)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password_here
```

Get Twitter API credentials from: https://developer.twitter.com/

### 🔧 Optional Configuration Values

```env
# Optional - Wallet Features
ENABLE_WALLET_UI=true
SOLANA_PRIVATE_KEY=your_solana_private_key        # Optional
ETH_PRIVATE_KEY=your_eth_private_key              # Optional

# Optional - External API Integration
OVERSEER_BOT_AI_URL=https://your-overseer-ai.onrender.com
OVERSEER_BOT_AI_API_KEY=your_api_key              # Optional
TOKEN_SCALPER_URL=https://your-token-scalper.onrender.com
TOKEN_SCALPER_API_KEY=your_api_key                # Optional
POLL_INTERVAL=15                                   # Seconds between polls

# Optional - Other
HUGGING_FACE_TOKEN=your_hugging_face_token  # For AI responses
WEBHOOK_API_KEY=your_webhook_api_key        # For external webhooks
PORT=5000                                    # Web server port
```

**See `.env.example` for complete documentation of all variables.**

📖 **For detailed setup instructions, troubleshooting, and platform-specific guides, see [ENV_SETUP_GUIDE.md](./ENV_SETUP_GUIDE.md)**

### 🔐 Generate Secure Credentials

**Linux / macOS / Git Bash:**
```bash
# Generate secure admin password
openssl rand -base64 32

# Generate webhook API key
openssl rand -hex 32
```

**Windows (PowerShell):**
```powershell
# Generate secure password (32 characters)
$bytes = New-Object Byte[] 32
[Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
[Convert]::ToBase64String($bytes)

# Or use the Python setup script:
python setup_env.py
```

### ⚠️ Security Checklist

Before running in production:

- [ ] Created `.env` from `.env.example` template
- [ ] Changed default `ADMIN_PASSWORD` to a strong password
- [ ] Generated strong `WEBHOOK_API_KEY` (if using webhooks)
- [ ] Verified `.env` is in `.gitignore` (it is by default)
- [ ] Set restrictive file permissions on `.env` (Unix: `chmod 600 .env`)
- [ ] NEVER commit `.env` to version control
- [ ] For cloud deployment, use platform environment variables (not `.env` files)

## 📊 Monitored Tokens

By default, the bot monitors:

| Token | Alert Threshold | Check Interval |
|-------|----------------|----------------|
| SOL/USDT | ±5% | 5 minutes |
| BTC/USDT | ±3% | 5 minutes |
| ETH/USDT | ±4% | 5 minutes |

Configure in `overseer_bot.py` → `MONITORED_TOKENS`

## 🌐 Deployment

### Render.com (Recommended)

The repository includes `render.yaml` for one-click deployment:

1. Fork this repository
2. Connect to [Render.com](https://render.com)
3. Create a new Web Service
4. Set environment variables in Render dashboard
5. **Choose instance type:**
   - **Free tier**: Good for testing (spins down after inactivity)
   - **Starter ($7/mo)**: Recommended for production (always-on, no cold starts)
   - See upgrade instructions in `render.yaml` comments
6. Deploy!

**📝 Important:** The free tier spins down after 15 minutes of inactivity, causing 30-60 second delays on first access. For production use, upgrade to at least the Starter plan for always-on service.

### Other Platforms

Compatible with:
- **Heroku** - Use `Procfile`: `web: python overseer_bot.py`
- **Railway** - Auto-detects Python
- **AWS/GCP/Azure** - Use container or VM deployment
- **Docker** - Create `Dockerfile` with Python 3.9+ base

## 📚 Documentation

**📑 [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md) - Complete navigation guide for all docs**

Comprehensive documentation available:

### Essential Guides

- 📘 **[DOCUMENTATION.md](./DOCUMENTATION.md)** - Complete all-in-one technical guide
  - Architecture and components
  - API reference
  - Security hardening
  - Troubleshooting guide
  - Advanced configuration

- 🐦 **[TWITTER_BEST_PRACTICES.md](./TWITTER_BEST_PRACTICES.md)** - Avoid shadow bans
  - Rate limit safety (bot uses < 5% of limits!)
  - Twitter API compliance
  - Best practices for automated accounts
  - Monitoring and adjustment guidance

- 🗣️ **[USER_INTERACTION_GUIDE.md](./USER_INTERACTION_GUIDE.md)** - How to interact with the bot
  - How to mention @OverseerBot to get responses
  - Price check queries (SOL, BTC, ETH)
  - Token safety checks (honeypot detection)
  - Example interactions and timing expectations

- 🔗 **[TOKEN_SCALPER_SETUP.md](./TOKEN_SCALPER_SETUP.md)** - Wallet configuration
  - How to add wallets for Token-scalper bot
  - Webhook integration between bots
  - RPC endpoint configuration
  - Alert types and monitoring

- 💰 **[WALLET_UI_GUIDE.md](./WALLET_UI_GUIDE.md)** - NEW! Wallet & Manual Control Guide
  - Complete wallet setup (Solana, ETH, BSC)
  - Using the enhanced tabbed UI
  - Manual token safety checking
  - Manual price checking
  - API usage examples

- 🔧 **[ENV_SETUP_GUIDE.md](./ENV_SETUP_GUIDE.md)** - NEW! Environment Variable Setup Guide
  - Understanding .env files (manual configuration only)
  - Interactive setup script usage
  - Platform-specific setup instructions (Windows, Mac, Linux)
  - Cloud deployment configuration
  - Security best practices
  - Troubleshooting configuration issues

### Quick Reference

- [Security Setup](./DOCUMENTATION.md#-security-setup)
- [API Endpoints](./DOCUMENTATION.md#-api-reference)
- [Webhook Integration](./DOCUMENTATION.md#-webhook-integration)
- [Troubleshooting](./DOCUMENTATION.md#-troubleshooting)

## 🔐 Security

**⚠️ IMPORTANT:** Before deploying to production:

1. ✅ Change default `ADMIN_PASSWORD`
2. ✅ Generate strong `WEBHOOK_API_KEY`
3. ✅ Enable HTTPS (automatic on most platforms)
4. ✅ Review security warnings in logs
5. ✅ Keep credentials secret (never commit `.env`)

See [Security Guide](./DOCUMENTATION.md#-security-setup) for details.

## 🛠️ Development

### Project Structure

```
overseer-bot-ai/
├── overseer_bot.py          # Main bot application
├── requirements.txt         # Python dependencies (development)
├── requirements-lock.txt    # Locked dependencies (production)
├── .env.example            # Environment template
├── render.yaml             # Render.com config
├── README.md               # This file
├── DOCUMENTATION.md        # Complete documentation
├── DEPENDENCIES.md         # Dependency management guide
└── price_cache.json        # Price cache (generated)
```

### Key Components

- **Scheduler** - APScheduler for automated tasks
- **Twitter Client** - Tweepy for Twitter API v2
- **Price Module** - CCXT for cryptocurrency exchanges
- **Web Server** - Flask for monitoring dashboard
- **Safety Checker** - Honeypot.is API integration

## 📊 Monitoring

### Dashboard Features

Access the dashboard at `http://localhost:5000/`:

- 🟢 **Bot Status** - Uptime, active jobs, cache stats
- 💹 **Price Monitor** - Live token prices, 24h changes
- ⏰ **Scheduler** - Next run times for all jobs
- 📝 **Activity Log** - Last 50 bot activities
- 🔌 **API Access** - JSON endpoints for integration

### API Endpoints

All endpoints require HTTP Basic Auth:

```bash
# Get bot status
curl -u admin:password http://localhost:5000/api/status

# Get current prices
curl -u admin:password http://localhost:5000/api/prices

# Get scheduler jobs
curl -u admin:password http://localhost:5000/api/jobs

# Get recent activities
curl -u admin:password http://localhost:5000/api/activities
```

## 🤝 Webhook Integration

### Game Event Webhook

Send game events to `/overseer-event`:

```bash
curl -X POST http://localhost:5000/overseer-event \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_webhook_api_key" \
  -d '{
    "event_type": "perk",
    "player_address": "0x123...",
    "perk_name": "Bloody Mess",
    "amount": 100
  }'
```

### Token-Scalper Webhook

Receive alerts from Token-scalper bot at `/token-scalper-alert`:

```bash
curl -X POST http://localhost:5000/token-scalper-alert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_webhook_api_key" \
  -d '{
    "alert_type": "rug_pull",
    "token_symbol": "SCAM",
    "severity": "critical"
  }'
```

## 🐛 Troubleshooting

### Common Issues

**Bot not tweeting?**
- Verify all 5 Twitter API credentials in `.env`
- Check `overseer_ai.log` for authentication errors
- Ensure Twitter account has proper permissions

**Dashboard not accessible?**
- Check `PORT` environment variable (default: 5000)
- Verify `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`
- Check firewall rules if deployed remotely

**Price data missing?**
- Binance may be geo-blocked (bot uses CoinGecko fallback)
- Check network connectivity
- Review logs: `grep "price" overseer_ai.log`

**Mentions not responding?**
- Verify `BEARER_TOKEN` is valid
- Check Twitter API rate limits
- Ensure bot account is not suspended

See [Complete Troubleshooting Guide](./DOCUMENTATION.md#-troubleshooting)

## 📝 Logs

View application logs:

```bash
# Live tail
tail -f overseer_ai.log

# Search for errors
grep ERROR overseer_ai.log

# Filter by feature
grep "price alert" overseer_ai.log
grep "mention response" overseer_ai.log
```

## 🎮 Personality System

The bot features a sophisticated personality system:

- **5 Tone Variations** - Glitch, ominous, sarcastic, corporate, neutral
- **Time-Aware Messages** - Different content for morning/afternoon/evening/night
- **Threat Levels** - GREEN/YELLOW/ORANGE/RED/PURPLE status updates
- **100+ Unique Lines** - Lore drops, vault logs, ads, survivor notes

## 🔄 Scheduler Jobs

The bot runs these automated tasks:

| Job | Frequency | Description |
|-----|-----------|-------------|
| Broadcast | 2-4 hours | Random Vault-Tec content |
| Mention Response | 15-30 min | Reply to @mentions |
| Retweet Hunt | 1 hour | Find & RT relevant content |
| Daily Diagnostic | 8 AM | System status report |
| Price Check | 5 minutes | Monitor token prices |
| Market Summary | 3x daily | Price overview (8 AM, 2 PM, 8 PM) |

## 🌟 Advanced Features

- **Multi-Token Support** - Monitor unlimited tokens (edit `MONITORED_TOKENS`)
- **Custom Thresholds** - Per-token alert sensitivity
- **Geo-Smart Pricing** - Auto-fallback from Binance to CoinGecko
- **Thread-Safe Caching** - Concurrent request handling
- **Extensible Webhooks** - Easy integration with external services
- **Optional AI** - Works with or without Hugging Face

## 📜 License

This project is open source. See repository for license details.

## 🙏 Credits

- **Fallout Universe** - Bethesda Game Studios
- **Atomic Fizz Caps** - [atomicfizzcaps.xyz](https://www.atomicfizzcaps.xyz)
- **Token-Scalper Integration** - [Token-scalper bot](https://github.com/Unwrenchable/Token-scalper)

## 📞 Support

- 📖 Read the [Complete Documentation](./DOCUMENTATION.md)
- 🔗 Check [Integration Guide](./INTEGRATION_GUIDE.md) for external API setup
- 🐛 Report issues on GitHub
- 💬 Check logs in `overseer_ai.log`
- 📊 Monitor dashboard at `/`

---

<div align="center">

**⚠️ The Overseer is watching. The wasteland awaits. ⚠️**

*Built with Python • Powered by Twitter API • Secured by Vault-Tec*

</div>
