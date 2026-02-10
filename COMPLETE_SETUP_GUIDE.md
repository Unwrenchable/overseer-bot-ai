# 🚀 Complete Setup Guide - Overseer Bot with Wallet UI

This guide walks you through setting up the Overseer Bot with full wallet functionality for manual trading and monitoring.

---

## 📋 Table of Contents

1. [Quick Start (5 minutes)](#quick-start)
2. [Full Setup with Wallet (15 minutes)](#full-setup-with-wallet)
3. [Deployment to Production](#deployment)
4. [Troubleshooting](#troubleshooting)

---

## Quick Start

**Just want monitoring and Twitter automation? Start here:**

### Step 1: Clone and Install

```bash
git clone https://github.com/atomicfizzcaps/overseer-bot-ui.git
cd overseer-bot-ui
pip install -r requirements.txt
```

### Step 2: Configure Twitter API

```bash
cp .env.example .env
nano .env
```

Add your Twitter API credentials:
```env
CONSUMER_KEY=your_twitter_consumer_key
CONSUMER_SECRET=your_twitter_consumer_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_SECRET=your_twitter_access_secret
BEARER_TOKEN=your_twitter_bearer_token

ADMIN_USERNAME=admin
ADMIN_PASSWORD=change_me_to_something_secure

# Wallet features disabled for quick start
ENABLE_WALLET_UI=false
```

### Step 3: Run

```bash
python overseer_bot.py
```

### Step 4: Access Dashboard

Open http://localhost:5000 in your browser.

**Login:** admin / your_password

✅ **You now have:**
- Twitter bot posting automatically
- Price monitoring (SOL, BTC, ETH)
- Web dashboard with manual tools
- Token safety checker
- Manual price checker

---

## Full Setup with Wallet

**Want full wallet integration? Follow these steps:**

### Step 1: Install All Dependencies

```bash
cd overseer-bot-ui
pip install -r requirements.txt
```

This installs:
- Twitter API client (tweepy)
- Crypto price feeds (ccxt)
- **Solana SDK** (solana, solders, base58)
- **Ethereum/BSC SDK** (web3)
- Flask web server
- Scheduler (apscheduler)

### Step 2: Generate Wallet Keys

#### For Solana (Optional)

**Option A: Create New Wallet**
```bash
# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# Generate new keypair
solana-keygen new --no-bip39-passphrase --outfile ~/.config/solana/bot-wallet.json

# View address
solana-keygen pubkey ~/.config/solana/bot-wallet.json

# Get private key (base58)
cat ~/.config/solana/bot-wallet.json
# Copy the array and convert, or just use the file content directly
```

**Option B: Use Existing Wallet**
If you have a Phantom or Solflare wallet, export the private key.

#### For Ethereum/BSC (Optional)

**Option A: Create New Wallet (Python)**
```python
from web3 import Web3
account = Web3().eth.account.create()
print(f"Address: {account.address}")
print(f"Private Key: {account.key.hex()[2:]}")  # Remove 0x
```

**Option B: Use Existing Wallet**
Export private key from MetaMask or other wallet.

### Step 3: Configure Environment

```bash
cp .env.example .env
nano .env
```

**Complete .env configuration:**

```env
# ===== TWITTER API (Required) =====
CONSUMER_KEY=your_twitter_consumer_key
CONSUMER_SECRET=your_twitter_consumer_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_SECRET=your_twitter_access_secret
BEARER_TOKEN=your_twitter_bearer_token

# ===== ADMIN AUTH (Required) =====
ADMIN_USERNAME=admin
ADMIN_PASSWORD=$(openssl rand -base64 32)  # Generate secure password

# ===== WALLET FEATURES (Optional) =====
ENABLE_WALLET_UI=true

# Solana Wallet
SOLANA_PRIVATE_KEY=your_base58_private_key_here
SOLANA_RPC_ENDPOINT=https://api.mainnet-beta.solana.com

# Ethereum/BSC Wallet (same private key for both)
ETH_PRIVATE_KEY=your_hex_private_key_without_0x
ETH_RPC_ENDPOINT=https://eth.public-rpc.com
BSC_RPC_ENDPOINT=https://bsc-dataseed1.binance.org

# ===== WEBHOOK (Optional) =====
WEBHOOK_API_KEY=$(openssl rand -hex 32)  # For Token-scalper integration

# ===== SERVER =====
PORT=5000
```

### Step 4: Secure Your Configuration

```bash
# Ensure .env is in .gitignore (already done)
cat .gitignore | grep .env

# Set restrictive permissions
chmod 600 .env

# Never commit .env!
git status  # Should not show .env
```

### Step 5: Run the Bot

```bash
python overseer_bot.py
```

Expected output:
```
2026-02-10 12:00:00 - VAULT-TEC OVERSEER LOG - INFO - ✅ Solana wallet initialized: ABC123...XYZ789
2026-02-10 12:00:00 - VAULT-TEC OVERSEER LOG - INFO - ✅ ETH/BSC wallet initialized: 0x123...789
2026-02-10 12:00:00 - VAULT-TEC OVERSEER LOG - INFO - Flask monitoring UI started on port 5000
2026-02-10 12:00:00 - VAULT-TEC OVERSEER LOG - INFO - Scheduler started successfully
```

### Step 6: Explore the Dashboard

Open http://localhost:5000

**Login:** admin / your_password

**Explore the tabs:**

1. **📊 MONITORING** - View bot status, prices, scheduled jobs
2. **💰 WALLET** - Click "CHECK WALLET STATUS" to see balances
3. **🔧 TOOLS** - Try the token safety checker and price checker
4. **🔗 API** - See available API endpoints

---

## Deployment

### Deploy to Render.com (Recommended)

1. **Fork the repository**
   - Go to https://github.com/atomicfizzcaps/overseer-bot-ui
   - Click "Fork" button

2. **Connect to Render**
   - Go to https://render.com
   - Sign up / Log in
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your forked repository

3. **Configure Environment Variables**
   
   In Render dashboard, add these environment variables:
   
   ```
   CONSUMER_KEY = your_twitter_key
   CONSUMER_SECRET = your_twitter_secret
   ACCESS_TOKEN = your_twitter_token
   ACCESS_SECRET = your_twitter_access_secret
   BEARER_TOKEN = your_twitter_bearer
   
   ADMIN_USERNAME = admin
   ADMIN_PASSWORD = your_secure_password
   
   ENABLE_WALLET_UI = true
   SOLANA_PRIVATE_KEY = your_solana_key
   ETH_PRIVATE_KEY = your_eth_key
   
   WEBHOOK_API_KEY = your_webhook_key
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Access at: `https://your-app-name.onrender.com`

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-bot-name

# Set environment variables
heroku config:set CONSUMER_KEY=your_key
heroku config:set CONSUMER_SECRET=your_secret
# ... (set all variables)

# Deploy
git push heroku main

# Open app
heroku open
```

### Deploy with Docker

**Create Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "overseer_bot.py"]
```

**Build and run:**
```bash
# Build
docker build -t overseer-bot .

# Run
docker run -p 5000:5000 --env-file .env overseer-bot
```

---

## Troubleshooting

### Wallet Features Not Working

**Symptom:** Wallet tab shows "WALLET FEATURES DISABLED"

**Solutions:**

1. Check dependencies:
   ```bash
   pip list | grep -E "solana|web3|base58"
   ```
   
   Should show:
   ```
   base58        2.1.1
   solana        0.30.0
   solders       0.18.0
   web3          6.11.0
   ```

2. Verify .env configuration:
   ```bash
   cat .env | grep -E "ENABLE_WALLET|PRIVATE_KEY"
   ```

3. Check logs:
   ```bash
   tail -f overseer_ai.log | grep -i wallet
   ```

### Bot Not Tweeting

**Symptom:** Bot starts but doesn't post tweets

**Solutions:**

1. Verify Twitter API credentials:
   ```bash
   # All 5 credentials required
   cat .env | grep -E "CONSUMER|ACCESS|BEARER"
   ```

2. Check rate limits:
   ```bash
   grep "rate limit" overseer_ai.log
   ```

3. Test credentials manually:
   ```python
   import tweepy
   client = tweepy.Client(bearer_token="your_bearer")
   print(client.get_me())
   ```

### Price Data Not Loading

**Symptom:** Prices show "N/A" in dashboard

**Solutions:**

1. Check internet connectivity
2. Try alternative exchanges (Binance may be geo-blocked)
3. Use CoinGecko fallback (automatic)
4. Check logs:
   ```bash
   grep "price" overseer_ai.log
   ```

### Dashboard Not Accessible

**Symptom:** Can't access http://localhost:5000

**Solutions:**

1. Check port is not in use:
   ```bash
   lsof -i :5000
   ```

2. Try different port:
   ```bash
   export PORT=8080
   python overseer_bot.py
   ```

3. Check firewall:
   ```bash
   # Linux
   sudo ufw status
   
   # Allow port
   sudo ufw allow 5000
   ```

### Authentication Issues

**Symptom:** Wrong username/password errors

**Solutions:**

1. Verify credentials in .env:
   ```bash
   cat .env | grep ADMIN
   ```

2. Reset password:
   ```bash
   # Generate new password
   openssl rand -base64 32
   
   # Update .env
   ADMIN_PASSWORD=new_generated_password
   
   # Restart bot
   ```

---

## Security Checklist

Before going to production:

- [ ] Change default `ADMIN_PASSWORD`
- [ ] Generate strong `WEBHOOK_API_KEY`
- [ ] Use HTTPS (automatic on Render/Heroku)
- [ ] Never commit `.env` file
- [ ] Use read-only wallets for monitoring
- [ ] Set restrictive file permissions (`chmod 600 .env`)
- [ ] Review security warnings in logs
- [ ] Enable 2FA on hosting platform
- [ ] Use strong Twitter API credentials
- [ ] Regularly update dependencies

---

## Next Steps

### Integrate with Token-Scalper

See [TOKEN_SCALPER_SETUP.md](./TOKEN_SCALPER_SETUP.md) for:
- Configuring Token-scalper bot
- Setting up wallet monitoring
- Connecting webhooks
- Receiving rug pull alerts

### Customize the Bot

Edit `overseer_bot.py` to:
- Add more tokens to monitor
- Adjust price alert thresholds
- Change tweet frequency
- Modify personality messages
- Add custom features

### Monitor Performance

- Check logs: `tail -f overseer_ai.log`
- View dashboard: http://localhost:5000
- Monitor Twitter API usage
- Track wallet balances
- Review security warnings

---

## Getting Help

### Documentation

- [README.md](./README.md) - Project overview
- [WALLET_UI_GUIDE.md](./WALLET_UI_GUIDE.md) - Wallet features in depth
- [UI_VISUAL_GUIDE.md](./UI_VISUAL_GUIDE.md) - UI layout reference
- [TOKEN_SCALPER_SETUP.md](./TOKEN_SCALPER_SETUP.md) - Token-scalper integration
- [DOCUMENTATION.md](./DOCUMENTATION.md) - Complete technical docs

### Support

- 🐛 Report issues on GitHub
- 💬 Check logs for errors
- 📧 Contact maintainers
- 🔍 Search existing issues

### Common Resources

- **Twitter Developer Portal:** https://developer.twitter.com/
- **Solana Documentation:** https://docs.solana.com/
- **Web3.py Documentation:** https://web3py.readthedocs.io/
- **Render Documentation:** https://render.com/docs
- **Heroku Documentation:** https://devcenter.heroku.com/

---

## Summary

You now have a fully functional Overseer Bot with:

✅ Twitter automation (posts, mentions, retweets)
✅ Cryptocurrency price monitoring
✅ Wallet integration (Solana, ETH, BSC)
✅ Manual token safety checking
✅ Manual price checking
✅ Web dashboard with 4 tabs
✅ RESTful API endpoints
✅ Production-ready deployment config

**The bot runs 24/7 and provides both automated and manual control.**

---

<div align="center">

**☢️ Welcome to Vault 77 ☢️**

*Your Fallout-themed crypto intelligence command center*

**Stay Safe. Trade Smart. Monitor Everything.**

</div>
