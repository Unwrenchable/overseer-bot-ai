# 📘 Overseer Bot AI — Complete Technical Documentation

**Version:** 3.0  
**Status:** Production Ready  

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Architecture](#-architecture)
3. [Installation & Setup](#-installation--setup)
4. [Configuration Reference](#-configuration-reference)
5. [Scheduler Jobs](#-scheduler-jobs)
6. [LLM / AI Pipeline](#-llm--ai-pipeline)
7. [Cryptocurrency Features](#-cryptocurrency-features)
8. [Twitter Integration](#-twitter-integration)
9. [API Reference](#-api-reference)
10. [Webhook Integration](#-webhook-integration)
11. [Security Setup](#-security-setup)
12. [Deployment Guide](#-deployment-guide)
13. [Monitoring & Maintenance](#-monitoring--maintenance)
14. [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

**Overseer Bot AI** is a single-process Python application that runs as a Twitter automation bot and web monitoring dashboard simultaneously.

**The bot persona:** OVERSEER-77, a corrupted Vault-Tec AI from Vault 77, tweeting from 200+ years post-apocalypse. It promotes the Atomic Fizz Caps game (`$CAPS` token, [atomicfizzcaps.xyz](https://www.atomicfizzcaps.xyz)) while providing real-time crypto price monitoring and alerts.

### Key Capabilities

| Capability | Details |
|-----------|---------|
| Twitter Automation | Scheduled broadcasts, mention responses, retweet hunting |
| Crypto Intelligence | Real-time SOL/BTC/ETH monitoring, threshold alerts |
| Token Safety | Honeypot detection via honeypot.is API |
| Event Webhooks | Game events (`/overseer-event`) trigger tweets |
| Built-in Dashboard | Flask web UI — status, prices, wallet balances, tools |
| AI Responses | OpenAI / xAI / Hugging Face (all optional) |
| Token Scanner | DexScreener + rugcheck.xyz scanner (optional, `ENABLE_SCALPER=true`) |

---

## 🏗️ Architecture

### Single-Process Design

The entire application runs as **one process** with two active components:

```
gunicorn (workers=1)
└── overseer_bot:app
    ├── Flask (main thread) — serves dashboard + API
    └── APScheduler (background thread) — runs all bot tasks
```

> ⚠️ **Always use `workers=1`.** The bot stores all state in memory (price cache, activity log, tweet dedup window, scheduler). Multiple workers cause duplicate tweets and inconsistent state.

### Module Structure

| File | Role |
|------|------|
| `overseer_bot.py` | Everything — Flask app, APScheduler jobs, Twitter client, LLM pipeline, price monitoring, webhook handlers, dashboard HTML |
| `api_client.py` | HTTP polling client; tracks health of external services; aggregates alerts |
| `gunicorn_config.py` | Production server config; `post_worker_init` calls `initialize_bot()` |
| `setup_env.py` | Standalone interactive `.env` generator — not imported by the bot |
| `test_twitter_bot.py` | Unit test suite (54 tests) |

### Runtime Feature Flags

These module-level booleans gate all feature use:

| Flag | Set to `True` when… |
|------|---------------------|
| `TWITTER_ENABLED` | All 5 Twitter credentials are present in env |
| `TWITTER_READ_ENABLED` | `TWITTER_ENABLED` **and** `get_me()` probe succeeds (Basic/Pro tier only) |
| `LLM_ENABLED` | Any of `OPENAI_API_KEY`, `XAI_API`, or `HUGGING_FACE_TOKEN` is set |
| `WALLET_ENABLED` | `solana`, `solders`, or `web3` packages import successfully |

### Thread Safety

- Price cache protected by `threading.Lock`
- Activity log and alert history protected by `threading.Lock`
- Tweet dedup window uses in-memory set protected by lock
- APScheduler uses its own internal thread pool

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.9+
- pip
- Twitter Developer Account (at minimum Free tier for write access)
- 512 MB RAM minimum

### Steps

```bash
# 1. Clone
git clone https://github.com/Unwrenchable/overseer-bot-ai.git
cd overseer-bot-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env — or run the interactive wizard:
python setup_env.py

# 4. Run (development)
python overseer_bot.py

# 5. Run (production — ALWAYS use this)
gunicorn -c gunicorn_config.py overseer_bot:app
```

### Run Tests

```bash
python test_twitter_bot.py
# All 54 tests should pass. No real credentials required — all external APIs are mocked.
```

---

## ⚙️ Configuration Reference

All configuration is via environment variables. Copy `.env.example` → `.env` and fill in values. Never commit `.env`.

### Twitter (all 5 required for `TWITTER_ENABLED=True`)

| Variable | Description |
|----------|-------------|
| `CONSUMER_KEY` | Twitter app consumer key |
| `CONSUMER_SECRET` | Twitter app consumer secret |
| `ACCESS_TOKEN` | Twitter user access token |
| `ACCESS_SECRET` | Twitter user access secret |
| `BEARER_TOKEN` | Twitter bearer token |

### Dashboard Auth

| Variable | Default | Description |
|----------|---------|-------------|
| `ADMIN_USERNAME` | `admin` | Dashboard login username |
| `ADMIN_PASSWORD` | `vault77secure` | **Change this!** Dashboard password |

### LLM / AI (any one enables `LLM_ENABLED`)

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key (tried first) |
| `OPENAI_BASE_URL` | Custom OpenAI-compatible base URL |
| `LLM_MODEL` | Model name for OpenAI/compatible provider |
| `XAI_API` | xAI/Grok API key (tried second) |
| `XAI_MODEL` | xAI model name |
| `HUGGING_FACE_TOKEN` | Hugging Face token (tried third) |
| `HF_MODEL` | Hugging Face model name |

### Wallet (optional)

| Variable | Description |
|----------|-------------|
| `ENABLE_WALLET_UI` | `true` to show Wallet tab in dashboard |
| `SOLANA_PRIVATE_KEY` | Solana wallet private key |
| `SOLANA_RPC_ENDPOINT` | Solana RPC URL |
| `ETH_PRIVATE_KEY` | Ethereum wallet private key |
| `ETH_RPC_ENDPOINT` | Ethereum RPC URL |
| `BSC_RPC_ENDPOINT` | BSC RPC URL |

### Built-in Token Scanner (optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_SCALPER` | `false` | Enable DexScreener + rugcheck scanner |
| `SCALPER_SCAN_INTERVAL` | `300` | Seconds between new-token scans |
| `SCALPER_POOL_MONITOR_INTERVAL` | `60` | Seconds between rug-pull monitor polls |
| `SCALPER_MIN_OPPORTUNITY_SCORE` | `60` | Min score (0–100) to trigger high-potential alert |
| `SCALPER_MIN_LIQUIDITY_USD` | `10000` | Min USD liquidity to consider a token |

### Other

| Variable | Default | Description |
|----------|---------|-------------|
| `WEBHOOK_API_KEY` | _(empty)_ | Secures `POST /overseer-event`; if empty, auth is skipped |
| `PORT` | `5000` | HTTP server port |
| `RENDER_EXTERNAL_URL` | _(empty)_ | Your public Render URL; used by keep-alive ping |

---

## ⏰ Scheduler Jobs

All jobs are registered in `initialize_bot()` using APScheduler.

| Job | Function | Schedule |
|-----|----------|----------|
| Price Alerts | `check_price_alerts` | Every 5 min |
| Market Summary | `post_market_summary` | 08:00, 14:00, 20:00 daily |
| Broadcast | `overseer_broadcast` | Random 60–120 min interval |
| Mention Response | `overseer_respond` | Random 15–30 min interval |
| Retweet Hunt | `overseer_retweet_hunt` | Every 60 min |
| Daily Diagnostic | `overseer_diagnostic` | 08:00 daily |
| Keep-alive Ping | `keep_alive_ping` | Every 14 min |

`overseer_respond` and `overseer_retweet_hunt` are silently skipped when `TWITTER_READ_ENABLED=False` (Free tier).

---

## 🤖 LLM / AI Pipeline

### Generation Chain

`generate_llm_response(prompt, max_tokens, context)` tries providers in order:

1. **OpenAI** — `_generate_openai_response()` (also works with OpenAI-compatible providers via `OPENAI_BASE_URL`)
2. **xAI** — `_generate_xai_response()`
3. **Hugging Face** — `_generate_hf_chat_response()`

Falls back gracefully to curated static content if no LLM is configured or all providers fail.

### Tweet Generation

`generate_overseer_tweet(topic, context, max_chars=270)` wraps the chain with the full `OVERSEER_SYSTEM_PROMPT` persona. Responses are scored by `_score_response()`, which penalises:
- Generic phrases
- All-caps headers
- Responses exceeding 270 characters

### Persona Rules

- Character: **OVERSEER-77**, corrupted Vault-Tec AI from Vault 77
- Token: `$CAPS` (never `AFCAPS`)
- Effective tweet limit: 270 chars (hard Twitter limit is 280)
- No all-caps headers, 0–2 emoji max, no generic "War never changes" closings
- Elon/X references: dry, in-character, ≤1 in 12 posts

---

## 💰 Cryptocurrency Features

### Price Monitoring

`MONITORED_TOKENS` (module-level dict) defines what to monitor:

```python
MONITORED_TOKENS = {
    "SOL/USDT":  {"exchange": "binance", "alert_threshold_up": 5,  "alert_threshold_down": 5,  "check_interval": 5},
    "BTC/USDT":  {"exchange": "binance", "alert_threshold_up": 3,  "alert_threshold_down": 3,  "check_interval": 5},
    "ETH/USDT":  {"exchange": "binance", "alert_threshold_up": 4,  "alert_threshold_down": 4,  "check_interval": 5},
}
```

Prices are fetched via **CCXT** (Binance first). If Binance returns a geo-block error, the bot automatically falls back to **CoinGecko** for that symbol.

### Alert Cooldowns

- `PRICE_ALERT_COOLDOWN_SECONDS = 3600` — each symbol has a 1-hour cooldown between alerts to prevent spam
- `TWEET_DEDUP_WINDOW_SECONDS = 86400` — global 24-hour duplicate tweet guard

### Market Summary

`post_market_summary()` runs at 08:00, 14:00, and 20:00. It fetches current prices for all monitored tokens and posts an in-character summary tweet.

---

## 🐦 Twitter Integration

### API Clients

- **Tweepy `Client`** (v2 API) — all tweet posting via `client.create_tweet()`
- **Tweepy `API`** (v1.1) — media upload only via `api_v1.media_upload()`

### Free vs. Paid Tier

| Feature | Free tier | Basic / Pro |
|---------|-----------|-------------|
| Post tweets | ✅ | ✅ |
| Read mentions | ❌ | ✅ |
| Search tweets | ❌ | ✅ |
| `overseer_respond` runs | ❌ silently skipped | ✅ |
| `overseer_retweet_hunt` runs | ❌ silently skipped | ✅ |

The bot detects the tier at startup by attempting `get_me()`. If it fails, `TWITTER_READ_ENABLED` is set to `False`.

### Duplicate Tweet Guard

- `_tweet_hash(text)` → SHA-256 of normalised text
- `is_duplicate_tweet(text)` checks the in-memory 24-hour window
- `mark_tweet_sent(text)` records the hash
- `_is_twitter_duplicate_error(exception)` catches error code 187 or "duplicate" in response body

---

## 🔌 API Reference

All endpoints except `/health` require **HTTP Basic Auth** (`ADMIN_USERNAME` / `ADMIN_PASSWORD`).

### Dashboard

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/` | Basic | Monitoring dashboard (HTML) |
| `GET` | `/health` | None | Health check JSON |

### Status & Data

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/status` | Bot status — uptime, flags, version |
| `GET` | `/api/prices` | Current token prices |
| `GET` | `/api/jobs` | Scheduler jobs with next-run times |
| `GET` | `/api/activities` | Last 50 activity log entries |
| `GET` | `/api/alerts` | Recent price alerts and errors |
| `GET` | `/api/health` | Service health summary |

### Wallet & Tools

| Method | Path | Body | Description |
|--------|------|------|-------------|
| `GET` | `/api/wallet/status` | — | Wallet balances (Solana, ETH, BSC) |
| `POST` | `/api/check-token` | `{"address": "0x..."}` | Token safety analysis |
| `POST` | `/api/price-check` | `{"symbol": "SOL"}` | Manual price check |

### Webhooks

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/overseer-event` | `WEBHOOK_API_KEY` (if set) | Game event webhook |

---

## 🤝 Webhook Integration

### Game Event Webhook

The bot listens for game events at `POST /overseer-event`. If `WEBHOOK_API_KEY` is set, the request must include `X-API-Key: <key>` or `Authorization: Bearer <key>`.

```bash
curl -X POST https://your-bot.onrender.com/overseer-event \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_webhook_api_key" \
  -d '{"event_type": "perk", "player_address": "0x123...", "perk_name": "Bloody Mess"}'
```

Supported `event_type` values: `perk`, `quest`, `swap`, `nft`, `level_up`, `moonpay`, `location`.

Each event type triggers a themed OVERSEER-77 tweet.

### Webhook API Key (Optional)

If `WEBHOOK_API_KEY` is empty, webhook endpoints accept requests without authentication (useful for local development). **Set it in production.**

---

## 🔐 Security Setup

### Quick Setup

```bash
# Generate credentials
export ADMIN_PASSWORD=$(openssl rand -base64 32)
export WEBHOOK_API_KEY=$(openssl rand -hex 32)
echo "ADMIN_PASSWORD=$ADMIN_PASSWORD"
echo "WEBHOOK_API_KEY=$WEBHOOK_API_KEY"
```

Add these to your `.env` (local) or platform environment variables (cloud).

### What Is Protected

| Endpoint | Auth Method |
|----------|-------------|
| `GET /` (dashboard) | HTTP Basic Auth |
| `GET /api/*` | HTTP Basic Auth |
| `POST /overseer-event` | `WEBHOOK_API_KEY` (if set) |
| `GET /health` | Public — no auth |

### Production Checklist

- [ ] Changed `ADMIN_PASSWORD` from default `vault77secure`
- [ ] Set `WEBHOOK_API_KEY` to a 32+ char random string
- [ ] HTTPS enabled (automatic on Render, Heroku, Railway)
- [ ] `.env` is in `.gitignore` and not committed
- [ ] Secrets set via platform env vars, not in `render.yaml`

See [SECURITY_GUIDE.md](./SECURITY_GUIDE.md) for detailed platform-specific instructions.

---

## 🌐 Deployment Guide

### Render.com (Recommended)

The repo includes `render.yaml` and `gunicorn_config.py` for zero-config deployment.

1. Fork the repo
2. Create a **Web Service** on [render.com](https://render.com) pointing to your fork
3. Set environment variables in the **Environment** tab (do NOT put secrets in `render.yaml`)
4. Render runs `gunicorn -c gunicorn_config.py overseer_bot:app` automatically

**Important:** `gunicorn_config.py` calls `initialize_bot()` in the `post_worker_init` hook. This starts APScheduler and all bot jobs after the worker process is ready.

### Other Platforms

```bash
# Heroku Procfile
web: gunicorn -c gunicorn_config.py overseer_bot:app

# Railway — set start command in Railway settings
gunicorn -c gunicorn_config.py overseer_bot:app

# Docker CMD
CMD ["gunicorn", "-c", "gunicorn_config.py", "overseer_bot:app"]
```

### Single-Worker Rule

**Never set `workers > 1`.** The bot:
- Stores price cache, activity log, and tweet dedup state in memory
- Uses APScheduler with a single job store — multiple workers would run duplicate jobs
- `gunicorn_config.py` enforces `workers = 1`

---

## 📊 Monitoring & Maintenance

### Dashboard

Access `https://your-bot.onrender.com/` to view:

- **Status panel** — uptime, `TWITTER_ENABLED`, `LLM_ENABLED`, `WALLET_ENABLED` flags
- **Price panel** — live prices with 24h % change for all monitored tokens
- **Jobs panel** — scheduler job list with next-run timestamps
- **Activity log** — last 50 bot actions with timestamps
- **Alerts panel** — recent price alerts and errors
- **Wallet tab** — Solana, ETH, BSC balances (when `ENABLE_WALLET_UI=true`)
- **Tools tab** — manual token safety checker, manual price check

### Logs

```bash
tail -f overseer_ai.log          # live
grep ERROR overseer_ai.log       # errors only
grep "price alert" overseer_ai.log
grep "duplicate" overseer_ai.log  # duplicate tweet attempts
```

### Keep-Alive

`keep_alive_ping` runs every 14 minutes and pings `RENDER_EXTERNAL_URL/health` to prevent Render's free tier from spinning down the service.

---

## 🐛 Troubleshooting

### Bot not tweeting

1. Verify all 5 Twitter credentials: `grep -c '=.' .env` should show 5+ lines with values
2. Check app permissions in X Developer Portal → set to **Read and write**, then regenerate `ACCESS_TOKEN` / `ACCESS_SECRET`
3. Check `overseer_ai.log` for `401 Unauthorized` or `403 Forbidden`
4. Restart service after credential changes

### Dashboard 401 / can't log in

1. Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` are set
2. Avoid special shell characters in passwords when testing with `curl` — quote the argument: `-u "admin:p@ss!word"`
3. Clear browser cache/cookies for the site

### Duplicate tweets in production

- Ensure `workers=1` in `gunicorn_config.py`
- Do not run `python overseer_bot.py` alongside gunicorn

### Price data missing / all zeros

1. Binance may be geo-blocked — check logs for "falling back to CoinGecko"
2. If CoinGecko also fails, check outbound network from your host
3. `grep "price" overseer_ai.log | tail -20`

### Mentions not being responded to

1. Free tier is write-only. Check logs for `Free tier — write-only mode`
2. Upgrade to Twitter Basic or Pro for mention reading
3. Verify `BEARER_TOKEN` is valid

### LLM / AI tweets not working

1. Verify at least one LLM key is set (`OPENAI_API_KEY`, `XAI_API`, or `HUGGING_FACE_TOKEN`)
2. Check `grep "LLM" overseer_ai.log` for errors
3. Bot falls back to static content automatically — this is normal behaviour without an LLM key

### Tests failing

```bash
pip install -r requirements.txt   # ensure deps are installed
python test_twitter_bot.py        # all 54 tests should pass
```

Tests mock all external APIs — no real credentials needed.

---

*The Overseer has spoken. Vault 77 documentation is complete.*