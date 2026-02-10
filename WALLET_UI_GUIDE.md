# 💰 Wallet UI & Manual Control Guide

## 📖 Overview

The Overseer Bot now includes an enhanced web UI with **wallet integration** and **manual control features**. This allows you to:

- 💰 **Monitor wallet balances** (Solana, Ethereum, BSC)
- 🔍 **Check token safety** manually (honeypot detection)
- 💱 **Check cryptocurrency prices** on-demand
- 🎮 **Control the bot manually** without relying only on automation

---

## 🎯 Features

### 1. Monitoring Dashboard (Existing + Enhanced)
- Real-time bot status and uptime
- Token price monitoring
- Scheduler job tracking
- Activity logging
- Now with a **tabbed interface** for better organization

### 2. Wallet Interface (NEW)
- View wallet connection status
- Check wallet balances (SOL, ETH, BNB)
- Real-time balance updates
- Support for multiple blockchains

### 3. Manual Tools (NEW)
- **Token Safety Checker** - Analyze any token for scams/honeypots
- **Price Checker** - Get real-time prices for any trading pair
- Manual control without waiting for scheduled jobs

### 4. API Documentation
- Complete API reference
- Example curl commands
- Authentication guide

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd /path/to/overseer-bot-ui
pip install -r requirements.txt
```

This will install:
- `solana` - Solana blockchain integration
- `web3` - Ethereum/BSC integration
- `base58` - Key encoding/decoding
- All existing dependencies

### Step 2: Configure Wallets (Optional)

If you want to use wallet features, update your `.env` file:

```bash
# Copy example if you don't have .env yet
cp .env.example .env

# Edit .env with your favorite editor
nano .env
```

Add wallet configuration:

```env
# Enable wallet UI features
ENABLE_WALLET_UI=true

# Solana wallet (optional)
SOLANA_PRIVATE_KEY=your_base58_encoded_private_key
SOLANA_RPC_ENDPOINT=https://api.mainnet-beta.solana.com

# Ethereum wallet (optional)
ETH_PRIVATE_KEY=your_hex_private_key_without_0x
ETH_RPC_ENDPOINT=https://eth.public-rpc.com

# BSC uses same wallet as ETH
BSC_RPC_ENDPOINT=https://bsc-dataseed1.binance.org
```

**⚠️ SECURITY WARNING:**
- Keep your `.env` file secure
- Never commit private keys to version control
- Use strong passwords for admin access
- Consider using read-only wallets for monitoring

### Step 3: Start the Bot

```bash
python overseer_bot.py
```

### Step 4: Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

Login with credentials from your `.env` file:
- **Username:** Value of `ADMIN_USERNAME` (default: `admin`)
- **Password:** Value of `ADMIN_PASSWORD` (**⚠️ CHANGE THIS!**)

---

## 📊 Using the New UI

### Tabbed Interface

The dashboard now has **4 main tabs**:

#### 1. 📊 MONITORING Tab
- Bot status (uptime, scheduler jobs)
- Real-time token prices
- Scheduled jobs with next run times
- Recent activity log

**What you can do:**
- Monitor automated operations
- See what the bot is doing
- Check price changes
- View activity history

#### 2. 💰 WALLET Tab

**If Wallet Features are ENABLED:**
- Click **"CHECK WALLET STATUS"** to view:
  - Connected wallet addresses
  - Current balances (SOL, ETH, BNB)
  - Connection status
  - Real-time updates

**If Wallet Features are DISABLED:**
- Instructions for enabling wallet features
- Step-by-step setup guide

#### 3. 🔧 TOOLS Tab

**Token Safety Checker:**
1. Enter a token contract address
2. Select the blockchain (Ethereum, BSC, Polygon, etc.)
3. Click **"CHECK TOKEN SAFETY"**
4. View results:
   - ✅ Safe / ⚠️ Risky
   - Risk score (0-100)
   - Warnings (high taxes, honeypot, etc.)

**Manual Price Checker:**
1. Enter a trading pair (e.g., `SOL/USDT`, `BTC/USDT`)
2. Select exchange (Binance or Coinbase)
3. Click **"CHECK PRICE"**
4. View results:
   - Current price
   - 24h change (%)
   - 24h high/low
   - 24h volume

#### 4. 🔗 API Tab

Complete API documentation:
- List of all endpoints
- Authentication guide
- Example curl commands
- Webhook information

---

## 🔧 Configuration Options

### Wallet Configuration

#### Solana Wallet Setup

**Generate a new wallet:**
```bash
# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# Generate new keypair
solana-keygen new --no-bip39-passphrase

# View your public address
solana-keygen pubkey ~/.config/solana/id.json

# Get your private key (base58 encoded)
cat ~/.config/solana/id.json
```

**Add to .env:**
```env
SOLANA_PRIVATE_KEY=your_base58_private_key_from_file
```

#### Ethereum/BSC Wallet Setup

**If you have an existing wallet:**
```env
# Your private key (hex format, without 0x prefix)
ETH_PRIVATE_KEY=abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
```

**Generate a new wallet (Python):**
```python
from web3 import Web3

# Generate new account
account = Web3().eth.account.create()
print(f"Address: {account.address}")
print(f"Private Key: {account.key.hex()[2:]}")  # Remove 0x prefix
```

#### RPC Endpoints

**Free Options:**
- Solana: `https://api.mainnet-beta.solana.com`
- Ethereum: `https://eth.public-rpc.com`
- BSC: `https://bsc-dataseed1.binance.org`

**Paid Options (Recommended for reliability):**
- Alchemy: https://www.alchemy.com/ (Free tier available)
- Infura: https://www.infura.io/ (Free tier available)
- QuickNode: https://www.quicknode.com/ (Free trial)

---

## 🛠️ Manual Operations

### Checking Token Safety

**Use Case:** Before investing in a new token, check if it's safe.

**Steps:**
1. Go to **🔧 TOOLS** tab
2. Paste token contract address
3. Select correct blockchain
4. Click **"CHECK TOKEN SAFETY"**

**Example Results:**

**Safe Token:**
```
✅ Token appears SAFE
Risk Score: 15/100
Warnings: None
```

**Risky Token:**
```
⚠️ Token has RISKS
Risk Score: 85/100
Warnings:
- High sell tax: 15%
- 🛑 HONEYPOT DETECTED!
```

### Checking Prices Manually

**Use Case:** Check a price without waiting for scheduled updates.

**Steps:**
1. Go to **🔧 TOOLS** tab
2. Enter trading pair (e.g., `MATIC/USDT`)
3. Select exchange
4. Click **"CHECK PRICE"**

**Example Results:**
```
MATIC/USDT on binance
Price: $0.85
24h Change: +5.23%
24h High: $0.87
24h Low: $0.80
24h Volume: 15,234,567
```

---

## 🔗 API Usage

### Authentication

All API endpoints require HTTP Basic Authentication:

```bash
curl -u admin:your_password http://localhost:5000/api/status
```

### Wallet Status API

```bash
# Get wallet balances
curl -u admin:password http://localhost:5000/api/wallet/status
```

**Response:**
```json
{
  "enabled": true,
  "wallets": {
    "solana": {
      "address": "ABC123...",
      "balance": 5.42,
      "currency": "SOL",
      "connected": true
    },
    "ethereum": {
      "address": "0x123...",
      "balance": 0.15,
      "currency": "ETH",
      "connected": true
    }
  }
}
```

### Token Safety Check API

```bash
# Check token safety
curl -X POST http://localhost:5000/api/wallet/check-token \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d '{
    "token_address": "0x1234567890123456789012345678901234567890",
    "chain": "bsc"
  }'
```

**Response:**
```json
{
  "is_safe": false,
  "risk_score": 85,
  "warnings": [
    "High sell tax: 15%",
    "HONEYPOT DETECTED"
  ],
  "honeypot": true
}
```

### Manual Price Check API

```bash
# Check price
curl -X POST http://localhost:5000/api/price/check \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "SOL/USDT",
    "exchange": "binance"
  }'
```

**Response:**
```json
{
  "symbol": "SOL/USDT",
  "exchange": "binance",
  "price": 125.43,
  "change_24h": 3.45,
  "high_24h": 128.50,
  "low_24h": 120.10,
  "volume_24h": 1234567,
  "timestamp": "2026-02-10T12:34:56"
}
```

---

## 🔒 Security Best Practices

### 1. Protect Your Private Keys

**DO:**
- ✅ Store private keys in `.env` file
- ✅ Add `.env` to `.gitignore`
- ✅ Use environment variables on hosting platforms
- ✅ Use read-only/monitoring wallets when possible
- ✅ Backup your keys securely offline

**DON'T:**
- ❌ Commit private keys to version control
- ❌ Share private keys with anyone
- ❌ Store keys in plain text files in public directories
- ❌ Use production wallets with large balances for testing

### 2. Admin Authentication

**Change default password:**
```bash
# Generate secure password
openssl rand -base64 32

# Add to .env
ADMIN_PASSWORD=your_generated_secure_password
```

### 3. HTTPS in Production

When deploying to production:
- Use HTTPS (automatic on Render, Heroku, etc.)
- Consider using a reverse proxy (nginx, Cloudflare)
- Enable firewall rules to restrict access

### 4. Wallet API Key

Generate a webhook API key:
```bash
openssl rand -hex 32
```

Add to `.env`:
```env
WEBHOOK_API_KEY=your_generated_key
```

---

## 🌐 Deployment

### Render.com

Update `render.yaml` to include wallet environment variables:

```yaml
services:
  - type: web
    name: overseer-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python overseer_bot.py
    envVars:
      - key: ENABLE_WALLET_UI
        value: "true"
      - key: SOLANA_PRIVATE_KEY
        sync: false
      - key: SOLANA_RPC_ENDPOINT
        value: "https://api.mainnet-beta.solana.com"
      # ... existing vars ...
```

### Heroku

```bash
# Set wallet environment variables
heroku config:set ENABLE_WALLET_UI=true
heroku config:set SOLANA_PRIVATE_KEY=your_key
heroku config:set SOLANA_RPC_ENDPOINT=https://api.mainnet-beta.solana.com

# Deploy
git push heroku main
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "overseer_bot.py"]
```

---

## 🐛 Troubleshooting

### Wallet Features Not Working

**Problem:** Wallet tab shows "WALLET FEATURES DISABLED"

**Solutions:**
1. Check dependencies are installed:
   ```bash
   pip install solana solders base58 web3
   ```

2. Verify `.env` configuration:
   ```env
   ENABLE_WALLET_UI=true
   SOLANA_PRIVATE_KEY=your_key  # Must not be empty
   ```

3. Check logs for errors:
   ```bash
   tail -f overseer_ai.log | grep -i wallet
   ```

### Invalid Private Key

**Problem:** "Failed to initialize wallet" error

**Solutions:**
- Solana: Ensure key is base58 encoded (from `id.json` file)
- Ethereum: Ensure key is hex format without `0x` prefix
- Check for extra spaces or newlines in `.env` file

### API Requests Failing

**Problem:** 401 Unauthorized errors

**Solutions:**
- Verify admin credentials in `.env`
- Check you're using HTTP Basic Auth format
- Test with curl:
  ```bash
  curl -u admin:password http://localhost:5000/api/status
  ```

### Price Check Not Working

**Problem:** "Error: symbol not found" or exchange errors

**Solutions:**
- Use correct trading pair format: `TOKEN/USDT` (uppercase)
- Verify exchange supports the pair (try different exchange)
- Check if exchange API is accessible from your location

---

## 📝 Example Workflows

### Workflow 1: Daily Token Research

1. Hear about a new token on social media
2. Go to **🔧 TOOLS** → Token Safety Checker
3. Enter token address and select blockchain
4. Review risk score and warnings
5. If safe, check current price manually
6. Make informed decision

### Workflow 2: Portfolio Monitoring

1. Configure wallets in `.env`
2. Go to **💰 WALLET** tab
3. Click "CHECK WALLET STATUS"
4. View current balances across all chains
5. Compare with prices in **📊 MONITORING** tab
6. Calculate total portfolio value

### Workflow 3: Market Analysis

1. Go to **🔧 TOOLS** → Manual Price Checker
2. Check multiple trading pairs:
   - `BTC/USDT`
   - `ETH/USDT`
   - `SOL/USDT`
   - `MATIC/USDT`
3. Compare 24h changes
4. Identify trending tokens
5. Set up automated alerts for interesting pairs

---

## 🎯 Advanced Usage

### Running Without Wallet Features

If you only want monitoring and manual tools (no wallet integration):

```env
ENABLE_WALLET_UI=false
# or simply leave wallet keys empty
SOLANA_PRIVATE_KEY=
ETH_PRIVATE_KEY=
```

The UI will still provide:
- Token safety checking
- Price checking
- Monitoring dashboard
- API access

### Using Multiple Wallets

Currently supports one wallet per blockchain. To monitor multiple wallets:

**Option 1:** Use the API programmatically
```python
import requests

wallets = ['wallet1_key', 'wallet2_key', 'wallet3_key']
for key in wallets:
    # Update .env or environment
    # Restart app or call API
    pass
```

**Option 2:** Use separate instances
- Run multiple bot instances
- Each with different wallet configuration
- Access different ports

### Webhook Integration with Token-Scalper

The wallet UI works alongside Token-Scalper alerts:

1. Configure Token-Scalper to send webhooks
2. Overseer receives alerts at `/token-scalper-alert`
3. View alerts in activity log
4. Manually check suspicious tokens with safety checker
5. Verify prices with manual price checker

---

## 🙏 Credits & Resources

- **Solana Documentation:** https://docs.solana.com/
- **Web3.py Documentation:** https://web3py.readthedocs.io/
- **Honeypot.is API:** https://honeypot.is/
- **CCXT Exchange Library:** https://github.com/ccxt/ccxt

---

## 📞 Support

### Need Help?

- 📖 Read the [Complete Documentation](./DOCUMENTATION.md)
- 🔍 Check [Token-Scalper Setup](./TOKEN_SCALPER_SETUP.md)
- 🐛 Report issues on GitHub
- 💬 Check logs in `overseer_ai.log`

### Common Questions

**Q: Do I need to configure wallets to use the bot?**  
A: No! Wallets are optional. The bot works fine for monitoring and Twitter automation without any wallet configuration.

**Q: Is it safe to put my private keys in .env?**  
A: It's reasonably safe if you follow best practices (never commit .env, use strong admin password, enable HTTPS). However, consider using read-only/monitoring wallets instead of your main trading wallets.

**Q: Can I use the same wallet on multiple chains?**  
A: For ETH/BSC, yes (they use the same address format). For Solana, you need a separate wallet.

**Q: What if I don't have any crypto?**  
A: You can still use all the manual tools (token checker, price checker) without owning any crypto or configuring wallets.

---

<div align="center">

**💰 Trade Smart. Stay Safe. ☢️**

*Built with Python • Powered by Solana, Ethereum, BSC • Secured by Vault-Tec*

</div>
