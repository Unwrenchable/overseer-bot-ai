# 🔗 Token-Scalper Integration & Wallet Setup Guide

## 📖 Overview

This guide explains how to configure wallets for the **Token-scalper bot** and integrate it with the **Overseer Bot** for automated rug pull alerts, high-potential token discoveries, and airdrop notifications.

---

## 🎯 What is Token-Scalper?

**Token-scalper** is a separate bot that:
- Monitors blockchain transactions for new tokens
- Analyzes liquidity and trading patterns
- Detects potential rug pulls
- Identifies high-potential opportunities
- Tracks airdrops and token launches

**Integration with Overseer Bot:**
- Token-scalper sends alerts via webhook to Overseer
- Overseer posts these alerts to Twitter automatically
- Provides community warnings and opportunities

---

## 🔧 Prerequisites

Before setting up Token-scalper:

- ✅ Overseer Bot deployed and running
- ✅ Node.js 16+ installed (for Token-scalper)
- ✅ RPC endpoints for blockchains you want to monitor
- ✅ Wallet addresses to monitor (your trading wallets)
- ✅ Basic knowledge of blockchain and wallets

---

## 📁 Token-Scalper Repository

### Clone the Repository

```bash
# Clone Token-scalper bot
git clone https://github.com/Unwrenchable/Token-scalper.git
cd Token-scalper

# Install dependencies
npm install
```

### Repository Structure

```
Token-scalper/
├── config.json          # Main configuration file
├── wallets.json         # Wallet addresses to monitor
├── index.js             # Main bot file
├── package.json         # Dependencies
└── README.md            # Token-scalper docs
```

---

## 💼 Configuring Wallets

### Step 1: Create `wallets.json`

This file contains the wallet addresses you want Token-scalper to monitor for transactions.

**Create the file:**

```bash
cd Token-scalper
nano wallets.json
```

**Format:**

```json
{
  "ethereum": [
    "0x1234567890123456789012345678901234567890",
    "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
  ],
  "bsc": [
    "0x9876543210987654321098765432109876543210",
    "0xfedcbafedcbafedcbafedcbafedcbafedcbafed"
  ],
  "polygon": [
    "0x1111111111111111111111111111111111111111"
  ]
}
```

### Step 2: Understanding Wallet Configuration

**Structure:**
```json
{
  "chain_name": [
    "wallet_address_1",
    "wallet_address_2"
  ]
}
```

**Supported Chains:**
- `ethereum` - Ethereum mainnet
- `bsc` - Binance Smart Chain
- `polygon` - Polygon (Matic)
- `arbitrum` - Arbitrum
- `optimism` - Optimism
- `avalanche` - Avalanche C-Chain
- `fantom` - Fantom Opera

### Step 3: Adding Your Wallets

**Example: Monitoring Your Trading Wallets**

```json
{
  "ethereum": [
    "0xYourMainWallet...",
    "0xYourTradingWallet...",
    "0xYourHoldingWallet..."
  ],
  "bsc": [
    "0xYourBSCWallet1...",
    "0xYourBSCWallet2..."
  ]
}
```

**What gets monitored:**
- New token approvals
- Large swaps/trades
- Liquidity additions/removals
- Token transfers
- Contract interactions

### Step 4: Save the File

```bash
# Save and exit (Ctrl+O, Enter, Ctrl+X in nano)
```

---

## ⚙️ Configuring Token-Scalper

### Step 1: Create `config.json`

This is the main configuration file for Token-scalper.

```bash
cd Token-scalper
nano config.json
```

### Step 2: Basic Configuration

```json
{
  "rpc_endpoints": {
    "ethereum": "https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY",
    "bsc": "https://bsc-dataseed1.binance.org",
    "polygon": "https://polygon-rpc.com"
  },
  "monitoring": {
    "enabled_chains": ["ethereum", "bsc"],
    "check_interval": 60,
    "min_liquidity_usd": 10000,
    "min_market_cap_usd": 50000
  },
  "rug_pull_detection": {
    "enabled": true,
    "liquidity_drop_threshold": 0.5,
    "alert_on_removal": true
  },
  "high_potential": {
    "enabled": true,
    "min_score": 75,
    "factors": {
      "liquidity_growth": true,
      "holder_distribution": true,
      "contract_verified": true
    }
  },
  "social_media": {
    "overseer_webhook_url": "https://your-overseer-bot.onrender.com/token-scalper-alert",
    "overseer_api_key": "your_webhook_api_key_from_overseer_env"
  }
}
```

### Step 3: Configuration Breakdown

#### RPC Endpoints

RPC endpoints allow Token-scalper to read blockchain data.

**Free Options:**
```json
"rpc_endpoints": {
  "ethereum": "https://eth.public-rpc.com",
  "bsc": "https://bsc-dataseed1.binance.org",
  "polygon": "https://polygon-rpc.com"
}
```

**Paid Options (Recommended for reliability):**
```json
"rpc_endpoints": {
  "ethereum": "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY",
  "bsc": "https://bsc-dataseed1.binance.org",
  "polygon": "https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY"
}
```

**Get API Keys:**
- **Alchemy:** https://www.alchemy.com/ (Free tier: 300M compute units/month)
- **Infura:** https://www.infura.io/ (Free tier: 100k requests/day)
- **QuickNode:** https://www.quicknode.com/ (Free trial available)

#### Monitoring Settings

```json
"monitoring": {
  "enabled_chains": ["ethereum", "bsc", "polygon"],
  "check_interval": 60,              // Check every 60 seconds
  "min_liquidity_usd": 10000,        // Only track tokens with $10k+ liquidity
  "min_market_cap_usd": 50000        // Only track tokens with $50k+ market cap
}
```

#### Rug Pull Detection

```json
"rug_pull_detection": {
  "enabled": true,
  "liquidity_drop_threshold": 0.5,   // Alert if liquidity drops 50%+
  "alert_on_removal": true            // Alert when liquidity fully removed
}
```

#### High Potential Detection

```json
"high_potential": {
  "enabled": true,
  "min_score": 75,                   // Minimum score 0-100
  "factors": {
    "liquidity_growth": true,        // Check if liquidity is growing
    "holder_distribution": true,     // Check if holders are well distributed
    "contract_verified": true        // Prefer verified contracts
  }
}
```

### Step 4: Connect to Overseer Bot

**Critical Section:**

```json
"social_media": {
  "overseer_webhook_url": "YOUR_OVERSEER_BOT_URL/token-scalper-alert",
  "overseer_api_key": "YOUR_WEBHOOK_API_KEY"
}
```

**Find Your Values:**

1. **Overseer Webhook URL:**
   - Local: `http://localhost:5000/token-scalper-alert`
   - Render: `https://your-app-name.onrender.com/token-scalper-alert`
   - Heroku: `https://your-app-name.herokuapp.com/token-scalper-alert`

2. **Overseer API Key:**
   - From your Overseer Bot `.env` file
   - Variable name: `WEBHOOK_API_KEY`
   - Generate one if empty: `openssl rand -hex 32`

**Example:**

```json
"social_media": {
  "overseer_webhook_url": "https://overseer-bot-ai.onrender.com/token-scalper-alert",
  "overseer_api_key": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
}
```

---

## 🔐 Security Best Practices

### Protecting Your Configuration

1. **Never commit sensitive files**
   ```bash
   # Add to .gitignore
   echo "config.json" >> .gitignore
   echo "wallets.json" >> .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables for secrets**
   ```bash
   # Instead of hardcoding API keys in config.json:
   export ALCHEMY_API_KEY="your_key_here"
   export OVERSEER_WEBHOOK_KEY="your_webhook_key"
   ```

3. **Restrict file permissions**
   ```bash
   chmod 600 config.json
   chmod 600 wallets.json
   ```

### Wallet Privacy

**Important:** The wallets you add to `wallets.json` are only used for **monitoring**. Token-scalper:
- ✅ Only **reads** blockchain data (public info)
- ✅ Never has access to private keys
- ✅ Cannot make transactions
- ✅ Cannot move funds

**You're safe if:**
- You only add wallet **addresses** (0x...)
- You never add private keys or seed phrases
- You keep config files secure

---

## 🚀 Running Token-Scalper

### Start the Bot

```bash
# Navigate to Token-scalper directory
cd Token-scalper

# Start the bot
npm start

# Or run in background
nohup npm start > scalper.log 2>&1 &
```

### Verify It's Working

```bash
# Check logs
tail -f scalper.log

# You should see:
# - "Token-scalper started"
# - "Monitoring X wallets on Y chains"
# - "Connected to Overseer Bot at [URL]"
```

### Test the Integration

**Send a test alert:**

```bash
curl -X POST https://your-overseer-bot.onrender.com/token-scalper-alert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_webhook_api_key" \
  -d '{
    "alert_type": "high_potential",
    "token_symbol": "TEST",
    "token_address": "0x1234567890123456789012345678901234567890",
    "confidence": 0.85,
    "predicted_gain": 150.0
  }'
```

**Check Overseer Bot:**
- Visit dashboard: `https://your-overseer-bot.onrender.com/`
- Check activity log for "Token-scalper alert received"
- Check Twitter for posted tweet

---

## 📊 Example Wallet Setup

### For Day Traders

```json
{
  "ethereum": [
    "0xYourHotWallet...",
    "0xYourDEXWallet..."
  ],
  "bsc": [
    "0xYourPancakeSwapWallet...",
    "0xYourBakerySwapWallet..."
  ]
}
```

**What you'll get:**
- Alerts when tokens you've interacted with show suspicious activity
- Notifications about liquidity changes in your holdings
- Warnings if tokens in your wallet are potential rug pulls

### For Wallet Watchers

Monitor successful traders' wallets:

```json
{
  "ethereum": [
    "0xSuccessfulTraderWallet1...",
    "0xWhaleWallet2...",
    "0xSmartMoneyWallet3..."
  ]
}
```

**What you'll get:**
- Notifications when these wallets buy new tokens
- Copy-trading opportunities
- Early discovery of trending tokens

### For Project Owners

Monitor your own project:

```json
{
  "bsc": [
    "0xYourProjectTreasuryWallet...",
    "0xYourLiquidityWallet...",
    "0xYourMarketingWallet..."
  ]
}
```

**What you'll get:**
- Alerts if liquidity is removed unexpectedly
- Notifications about large sells
- Security monitoring for your token

---

## 🔔 Alert Types

### 1. Rug Pull Alert

**When:** Token-scalper detects liquidity removal or suspicious activity

**Overseer Bot Posts:**
```
🚨 RUG PULL ALERT 🚨

Token: $SCAM
Contract: 0x1234...5678

⚠️ Liquidity REMOVED
💸 Loss: $50,000

AVOID THIS TOKEN!
#CryptoAlert #RugPull
```

### 2. High Potential Alert

**When:** Token-scalper identifies promising opportunity

**Overseer Bot Posts:**
```
💎 HIGH POTENTIAL TOKEN 💎

Token: $MOON
Contract: 0xabcd...ef12

Confidence: 85%
Predicted Gain: +150%

DYOR before investing!
#Crypto #Opportunity
```

### 3. Airdrop Alert

**When:** Token-scalper finds airdrop opportunity

**Overseer Bot Posts:**
```
🎁 AIRDROP ALERT 🎁

Token: $FREE
Amount: 1,000 tokens

Claim: https://airdrop.link

Act fast, limited time!
#Airdrop #Crypto
```

---

## 🛠️ Troubleshooting

### Token-Scalper Not Starting

**Problem:** `npm start` fails

**Solutions:**
```bash
# Reinstall dependencies
rm -rf node_modules
npm install

# Check Node.js version
node --version  # Should be 16+

# Check for syntax errors in config.json
cat config.json | jq .  # Should parse without errors
```

### Wallets Not Being Monitored

**Problem:** No alerts being generated

**Checklist:**
- [ ] `wallets.json` exists and is valid JSON
- [ ] Wallet addresses are in correct format (0x + 40 hex chars)
- [ ] RPC endpoints are working (test with curl)
- [ ] Chains are enabled in `config.json`
- [ ] Check Token-scalper logs for errors

### Overseer Not Receiving Alerts

**Problem:** Token-scalper runs but Overseer doesn't post

**Checklist:**
- [ ] `overseer_webhook_url` is correct
- [ ] `overseer_api_key` matches Overseer's `WEBHOOK_API_KEY`
- [ ] Overseer Bot is running
- [ ] Firewall allows incoming webhooks
- [ ] Check Overseer logs: `grep "token-scalper" overseer_ai.log`

**Test Connection:**
```bash
# From Token-scalper server
curl -X POST $OVERSEER_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $OVERSEER_API_KEY" \
  -d '{"alert_type":"test"}'

# Should return: {"status":"success"}
```

### RPC Endpoint Errors

**Problem:** "RPC request failed" in logs

**Solutions:**
1. **Check endpoint status:**
   ```bash
   curl -X POST https://your-rpc-endpoint \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
   ```

2. **Use alternative endpoints:**
   - Switch to different RPC provider
   - Use multiple endpoints for redundancy

3. **Check rate limits:**
   - Free tiers have limits
   - Upgrade to paid plan if needed

---

## 📈 Advanced Configuration

### Multi-Chain Monitoring

```json
{
  "ethereum": [
    "0xWallet1...",
    "0xWallet2..."
  ],
  "bsc": [
    "0xWallet3...",
    "0xWallet4..."
  ],
  "polygon": [
    "0xWallet5..."
  ],
  "arbitrum": [
    "0xWallet6..."
  ]
}
```

### Selective Monitoring

Monitor specific tokens only:

```json
{
  "monitoring": {
    "whitelist_tokens": [
      "0xTokenAddress1...",
      "0xTokenAddress2..."
    ],
    "blacklist_tokens": [
      "0xScamToken1...",
      "0xSpamToken2..."
    ]
  }
}
```

### Custom Thresholds

```json
{
  "rug_pull_detection": {
    "liquidity_drop_threshold": 0.3,    // More sensitive (30%)
    "holder_concentration_max": 0.2,    // Alert if top holder has >20%
    "price_impact_threshold": 0.1       // Alert on 10% price impact
  }
}
```

---

## 📝 Configuration Templates

### Minimal Setup (Quick Start)

```json
{
  "rpc_endpoints": {
    "bsc": "https://bsc-dataseed1.binance.org"
  },
  "monitoring": {
    "enabled_chains": ["bsc"],
    "check_interval": 120
  },
  "social_media": {
    "overseer_webhook_url": "http://localhost:5000/token-scalper-alert",
    "overseer_api_key": ""
  }
}
```

### Production Setup (Recommended)

```json
{
  "rpc_endpoints": {
    "ethereum": "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY",
    "bsc": "https://bsc-dataseed1.binance.org",
    "polygon": "https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY"
  },
  "monitoring": {
    "enabled_chains": ["ethereum", "bsc", "polygon"],
    "check_interval": 60,
    "min_liquidity_usd": 10000,
    "min_market_cap_usd": 50000
  },
  "rug_pull_detection": {
    "enabled": true,
    "liquidity_drop_threshold": 0.5,
    "alert_on_removal": true
  },
  "high_potential": {
    "enabled": true,
    "min_score": 75
  },
  "social_media": {
    "overseer_webhook_url": "https://your-overseer.onrender.com/token-scalper-alert",
    "overseer_api_key": "your_secure_api_key_here"
  }
}
```

---

## ✅ Setup Checklist

### Initial Setup

- [ ] Clone Token-scalper repository
- [ ] Install dependencies (`npm install`)
- [ ] Create `wallets.json` with your addresses
- [ ] Create `config.json` with RPC endpoints
- [ ] Get RPC API keys (Alchemy, Infura, or QuickNode)
- [ ] Set Overseer webhook URL in config
- [ ] Set Overseer API key in config
- [ ] Test configuration: `npm test` (if available)

### Security

- [ ] Add `config.json` to `.gitignore`
- [ ] Add `wallets.json` to `.gitignore`
- [ ] Never commit API keys or wallet addresses
- [ ] Use environment variables for secrets
- [ ] Restrict file permissions (`chmod 600`)

### Testing

- [ ] Start Token-scalper: `npm start`
- [ ] Check logs for errors
- [ ] Send test webhook to Overseer
- [ ] Verify Overseer receives and posts alert
- [ ] Monitor for 1 hour to ensure stability

### Production

- [ ] Run Token-scalper on server/VPS
- [ ] Use process manager (PM2, systemd)
- [ ] Set up log rotation
- [ ] Monitor resource usage
- [ ] Set up alerts for downtime

---

## 📞 Need Help?

### Resources

- **Token-scalper Repo:** https://github.com/Unwrenchable/Token-scalper
- **Overseer Bot Docs:** See `DOCUMENTATION.md`
- **Webhook Testing:** See `API Reference` section in main docs

### Common Questions

**Q: Do I need Token-scalper to use Overseer Bot?**  
A: No! Overseer works standalone for price monitoring and Twitter engagement. Token-scalper is optional for advanced alerts.

**Q: Can I monitor wallets I don't own?**  
A: Yes! You can monitor any public wallet address. Token-scalper only reads public blockchain data.

**Q: How many wallets can I monitor?**  
A: Depends on your RPC provider's rate limits. Start with 5-10 and scale up as needed.

**Q: Does this cost money?**  
A: Free RPC endpoints work but have limits. Paid RPC plans ($10-50/month) recommended for serious monitoring.

---

<div align="center">

**Token-scalper + Overseer Bot = Complete Crypto Intelligence**

🔍 Monitor Transactions | 🚨 Detect Rug Pulls | 💎 Find Opportunities

</div>
