# ☢️ Overseer Bot AI - Vault 77

<div align="center">

![Vault-Tec](https://img.shields.io/badge/VAULT--TEC-77-green?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-OPERATIONAL-green?style=for-the-badge)
![Python](https://img.shields.io/badge/PYTHON-3.9%2B-blue?style=for-the-badge)

**A Fallout-themed Twitter bot with cryptocurrency intelligence**

[Features](#-features) • [Quick Start](#-quick-start) • [Configuration](#-configuration) • [Deployment](#-deployment) • [Documentation](#-documentation)

</div>

---

## 📖 About

**Overseer Bot AI** is a single-process Python bot built on Flask + APScheduler. It combines:
- 🎭 **Fallout Personality** — OVERSEER-77, a corrupted Vault-Tec AI from Vault 77, tweeting from 200 years post-apocalypse
- 🎮 **Game Promotion** — Promotes the Atomic Fizz Caps game ([atomicfizzcaps.xyz](https://www.atomicfizzcaps.xyz))
- 💰 **Crypto Intelligence** — Real-time token price monitoring & alerts
- 🛡️ **Token Safety Analysis** — Detects honeypots and scams
- 📊 **Built-in Monitoring Dashboard** — Vault-Tec themed web UI, no separate front-end needed

---

## ✨ Features

### Twitter Automation
- ✅ Automated broadcasts every 1–2 hours with varied Vault-Tec content
- ✅ Responds to @mentions every 15–30 minutes (Basic/Pro tier)
- ✅ Hunts and retweets relevant content hourly (Basic/Pro tier)
- ✅ Daily diagnostic reports at 8 AM
- ✅ AI-powered contextual responses (OpenAI, xAI, or Hugging Face — all optional)

### Cryptocurrency Intelligence
- 📈 Real-time price monitoring (SOL, BTC, ETH)
- 🚨 Automated price alerts on configurable threshold movements (SOL ±5%, BTC ±3%, ETH ±4%)
- 📊 Market summaries 3× daily (8 AM, 2 PM, 8 PM)
- 🔍 Token safety checker (honeypot detection via honeypot.is)
- 💎 CoinGecko fallback when Binance is geo-blocked

### Built-in Token Scanner
- 🔭 DexScreener + rugcheck.xyz scanning for new Solana tokens (enable with `ENABLE_SCALPER=true`)
- 🚨 Rug-pull detection and high-potential token alerts
- 💬 Alerts posted as tweets automatically

### Event Integration
- 🎮 Game event webhooks (`POST /overseer-event`) — perks, quests, swaps, NFTs, level-ups
- 🌐 MoonPay funding notifications
- 🗺️ Location claim announcements

### Monitoring Dashboard
- 🖥️ Vault-Tec themed web UI at `/` with tabbed interface
- 💰 **Wallet tab** — Solana, Ethereum, BSC balances
- 🔧 **Tools tab** — manual token safety checker & price checker
- 📊 Real-time status, uptime, scheduler jobs
- 💹 Live token prices with 24h changes
- 📝 Activity log (last 50 events)
- 🔒 HTTP Basic Auth protected
- 🔌 RESTful JSON API

---

## 🗣️ How to Interact with the Bot

**Mention the bot on Twitter:** `@OverseerBot` (replace with your actual bot handle)

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

**Response Time:** 15–30 minutes (bot checks mentions periodically)

> ⚠️ Mention responses and retweet hunting require a **Twitter Basic or Pro tier** account. Free tier is write-only.

📖 **Full interaction guide:** [USER_INTERACTION_GUIDE.md](./USER_INTERACTION_GUIDE.md)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Twitter Developer Account ([developer.twitter.com](https://developer.twitter.com/))
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Unwrenchable/overseer-bot-ai.git
cd overseer-bot-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# 4. Run the bot (development mode)
python overseer_bot.py
```

For production always use Gunicorn with **exactly 1 worker** (multiple workers cause duplicate tweets):

```bash
gunicorn -c gunicorn_config.py overseer_bot:app
```

### Access the Dashboard

```
http://localhost:5000
```

Login with your `.env` credentials:
- **Username:** `ADMIN_USERNAME` (default: `admin`)
- **Password:** `ADMIN_PASSWORD` (**⚠️ change this before deploying!**)

Dashboard tabs:
- 📊 **Monitoring** — real-time bot status and scheduler jobs
- 💰 **Wallet** — Solana, ETH, BSC balances
- 🔧 **Tools** — manual token safety checker & price checker
- 🔗 **API** — built-in API documentation

📖 **Wallet setup:** [WALLET_UI_GUIDE.md](./WALLET_UI_GUIDE.md)

---

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and fill in your values. **Never commit `.env`** — it is in `.gitignore`.

```env
# ── Twitter / X API (all 5 required) ──────────────────────────────────────
# Get all five from https://developer.twitter.com/ → your App → Keys and tokens
# ⚠️  Set App permissions to "Read and Write" BEFORE generating your Access Token
#
# CONSUMER_KEY     = "API Key"             (identifies your App)
# CONSUMER_SECRET  = "API Key Secret"      (App-level secret)
# ACCESS_TOKEN     = "Access Token"        (tied to your X account, write access)
# ACCESS_SECRET    = "Access Token Secret" (paired with ACCESS_TOKEN)
# BEARER_TOKEN     = "Bearer Token"        (app-only read token)
CONSUMER_KEY=your_api_key
CONSUMER_SECRET=your_api_key_secret
ACCESS_TOKEN=your_access_token
ACCESS_SECRET=your_access_token_secret
BEARER_TOKEN=your_bearer_token

# ── Dashboard auth (required) ─────────────────────────────────────────────
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change_me_strong_password   # ⚠️  CHANGE THIS

# ── AI / LLM (at least one enables AI-generated tweets) ───────────────────
# Priority order: xAI → OpenAI → HuggingFace
# xAI (Grok) is called first; others are only used if xAI is unavailable/fails
XAI_API=                  # PRIMARY  — xAI (Grok) key  — https://console.x.ai/
XAI_MODEL=grok-3-mini     # optional, default shown
OPENAI_API_KEY=           # FALLBACK 1 — OpenAI / Groq / Together / Ollama
LLM_MODEL=gpt-4o-mini     # optional, default shown
HUGGING_FACE_TOKEN=       # FALLBACK 2 — free tier available

# ── Wallet features (optional) ────────────────────────────────────────────
ENABLE_WALLET_UI=true
SOLANA_PRIVATE_KEY=                        # optional
ETH_PRIVATE_KEY=                           # optional

# ── Built-in token scanner (optional) ────────────────────────────────────
ENABLE_SCALPER=false

# ── Other ─────────────────────────────────────────────────────────────────
WEBHOOK_API_KEY=                           # secures /overseer-event
RENDER_EXTERNAL_URL=                       # your public URL — enables keep-alive ping
PORT=5000
```

Use `setup_env.py` for an interactive credential wizard:

```bash
python setup_env.py
```

### Generate Secure Credentials

```bash
openssl rand -base64 32   # ADMIN_PASSWORD
openssl rand -hex 32      # WEBHOOK_API_KEY
```

---

## 📊 Monitored Tokens (Defaults)

| Token | Alert Threshold | Check Interval |
|-------|----------------|----------------|
| SOL/USDT | ±5% | 5 minutes |
| BTC/USDT | ±3% | 5 minutes |
| ETH/USDT | ±4% | 5 minutes |

Edit `MONITORED_TOKENS` in `overseer_bot.py` to add or adjust symbols.

---

## 🔄 Scheduler Jobs

| Job | Frequency | Description |
|-----|-----------|-------------|
| Broadcast | 60–120 min random | Vault-Tec content, lore, ads |
| Mention Response | 15–30 min random | Reply to @mentions (Basic/Pro) |
| Retweet Hunt | 60 min | Find & RT relevant content (Basic/Pro) |
| Daily Diagnostic | 08:00 daily | System status tweet |
| Price Alerts | 5 min | Monitor token price thresholds |
| Market Summary | 08:00, 14:00, 20:00 | Daily price overview tweets |
| Keep-alive Ping | 14 min | Prevents Render.com sleep |

---

## 🌐 Deployment

### Render.com (Recommended)

The repo ships with `render.yaml` and `gunicorn_config.py` for zero-config Render deployment:

1. Fork this repository
2. Create a new **Web Service** on [Render.com](https://render.com) pointing to your fork
3. Set environment variables in the Render dashboard (do **not** put secrets in `render.yaml`)
4. Deploy — Render runs `gunicorn -c gunicorn_config.py overseer_bot:app` automatically

> **Single-worker rule:** `gunicorn_config.py` is pre-set to `workers = 1`. Never increase this — the bot stores state in memory and multiple workers cause duplicate tweets and race conditions.

### Other Platforms

| Platform | Start command |
|----------|--------------|
| **Heroku** | `web: gunicorn -c gunicorn_config.py overseer_bot:app` (Procfile) |
| **Railway** | Add gunicorn start command in Railway settings |
| **AWS / GCP / Azure** | Container or VM with Python 3.9+ + Gunicorn |
| **Docker** | Python 3.9+ base image, copy repo, `CMD ["gunicorn", "-c", "gunicorn_config.py", "overseer_bot:app"]` |

**Local development only:**

```bash
python overseer_bot.py   # Flask dev server — not for production
```

---

## 🔌 API Reference

All endpoints except `/health` require **HTTP Basic Auth**.

```bash
curl -u admin:your_password https://your-domain.com/api/status
```

### Monitoring
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Monitoring dashboard (HTML) |
| `GET` | `/health` | Health check — no auth required |
| `GET` | `/api/status` | Bot status (uptime, flags, version) |
| `GET` | `/api/prices` | Current token prices |
| `GET` | `/api/jobs` | Scheduler job list with next-run times |
| `GET` | `/api/activities` | Last 50 bot activities |
| `GET` | `/api/alerts` | Recent price and error alerts |
| `GET` | `/api/health` | Service health summary |

### Wallet & Tools
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/wallet/status` | Wallet balances (Solana, ETH, BSC) |
| `POST` | `/api/check-token` | Token safety analysis — body: `{"address":"0x..."}` |
| `POST` | `/api/price-check` | Manual price check — body: `{"symbol":"SOL"}` |

### Webhooks
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/overseer-event` | Game event webhook (requires `WEBHOOK_API_KEY` if set) |

---

## 🤝 Webhook Integration

### Game Event Webhook

```bash
curl -X POST https://your-bot.onrender.com/overseer-event \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_webhook_api_key" \
  -d '{
    "event_type": "perk",
    "player_address": "0x123...",
    "perk_name": "Bloody Mess",
    "amount": 100
  }'
```

Supported `event_type` values: `perk`, `quest`, `swap`, `nft`, `level_up`, `moonpay`, `location`.

---

## 🛠️ Project Structure

```
overseer-bot-ai/
├── overseer_bot.py          # Main application — Flask + APScheduler + all bot logic
├── api_client.py            # HTTP polling client & alert aggregation
├── gunicorn_config.py       # Production server config (workers=1)
├── setup_env.py             # Interactive .env generator (run standalone)
├── test_twitter_bot.py      # Unit test suite
├── render.yaml              # Render.com deployment manifest
├── requirements.txt         # Python dependencies
├── requirements-lock.txt    # Pinned dependency versions
├── .env.example             # Environment variable template (no secrets)
│
├── README.md                # This file
├── DOCUMENTATION.md         # Full technical reference
├── DOCUMENTATION_INDEX.md   # Doc navigation guide
├── DEPLOYMENT_CHECKLIST.md  # Pre-deployment checklist
├── SECURITY_GUIDE.md        # Security hardening guide
├── TWITTER_BEST_PRACTICES.md
├── USER_INTERACTION_GUIDE.md
├── WALLET_UI_GUIDE.md
└── DEPENDENCIES.md
```

### Key Components

| Component | File | Description |
|-----------|------|-------------|
| Scheduler | `overseer_bot.py` | APScheduler — all automated tasks |
| Twitter Client | `overseer_bot.py` | Tweepy v2 for posting, v1.1 for media |
| Price Module | `overseer_bot.py` | CCXT + CoinGecko fallback |
| LLM Pipeline | `overseer_bot.py` | OpenAI → xAI → Hugging Face chain |
| Web Server | `overseer_bot.py` | Flask — dashboard + API |
| Token Scanner | `overseer_bot.py` | DexScreener + rugcheck.xyz (optional) |
| Alert Aggregator | `api_client.py` | Health tracking + alert history |

---

## 🔐 Security

Before deploying to production:

1. ✅ Change default `ADMIN_PASSWORD` from `vault77secure`
2. ✅ Generate a strong `WEBHOOK_API_KEY` (`openssl rand -hex 32`)
3. ✅ Enable HTTPS (automatic on Render / Heroku / Railway)
4. ✅ Never commit `.env` to Git
5. ✅ Review `SECURITY_GUIDE.md` for full hardening checklist

---

## 🐛 Troubleshooting

**Bot not tweeting?**
- Verify all 5 Twitter credentials in `.env`
- No quotes or extra spaces around `=` in `.env` values
- Set app permissions to **Read and write** in the X Developer Portal
- After changing permissions, regenerate `ACCESS_TOKEN` / `ACCESS_SECRET`
- Check `overseer_ai.log` for auth errors

**Dashboard not accessible?**
- Check `PORT` env var (default: 5000)
- Verify `ADMIN_USERNAME` / `ADMIN_PASSWORD`
- Check firewall rules for remote deployments

**Price data missing?**
- Binance may be geo-blocked — bot auto-falls back to CoinGecko
- Check `grep "price" overseer_ai.log`

**Mentions not responding?**
- Free tier is write-only; upgrade to Basic/Pro for mention reading
- Check logs for `Free tier — write-only mode`

**Seeing duplicate tweets in production?**
- Ensure `workers=1` in `gunicorn_config.py` — never increase this

📖 Full troubleshooting: [DOCUMENTATION.md](./DOCUMENTATION.md#-troubleshooting)

---

## 📝 Logs

```bash
tail -f overseer_ai.log          # live tail
grep ERROR overseer_ai.log       # errors only
grep "price alert" overseer_ai.log
grep "mention response" overseer_ai.log
```

---

## 📚 Documentation

| File | Contents |
|------|----------|
| [DOCUMENTATION.md](./DOCUMENTATION.md) | Full technical reference — architecture, API, troubleshooting |
| [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md) | Doc navigation guide |
| [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) | Step-by-step pre-deployment checklist |
| [SECURITY_GUIDE.md](./SECURITY_GUIDE.md) | Credential management & hardening |
| [TWITTER_BEST_PRACTICES.md](./TWITTER_BEST_PRACTICES.md) | Rate limits, shadow ban prevention |
| [USER_INTERACTION_GUIDE.md](./USER_INTERACTION_GUIDE.md) | How to interact with the bot on Twitter |
| [WALLET_UI_GUIDE.md](./WALLET_UI_GUIDE.md) | Wallet configuration & dashboard tools |
| [DEPENDENCIES.md](./DEPENDENCIES.md) | Python dependency notes |

---

## 📜 License

This project is open source. See repository for license details.

## 🙏 Credits

- **Fallout Universe** — Bethesda Game Studios
- **Atomic Fizz Caps** — [atomicfizzcaps.xyz](https://www.atomicfizzcaps.xyz)

---

<div align="center">

**⚠️ The Overseer is watching. The wasteland awaits. ⚠️**

*Built with Python • Powered by Twitter API • Secured by Vault-Tec*

</div>
