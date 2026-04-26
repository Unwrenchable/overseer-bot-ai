# 📚 Documentation Index — Overseer Bot AI

**Quick navigation guide for all documentation**

---

## 🚀 Start Here

| File | Purpose |
|------|---------|
| **[README.md](./README.md)** | Overview, quick start, deployment, full API reference |
| **[.env.example](./.env.example)** | Copy to `.env` and fill in credentials |

---

## 📖 User Guides

### [USER_INTERACTION_GUIDE.md](./USER_INTERACTION_GUIDE.md) 🗣️
How to interact with the live bot on Twitter.

- Mention `@OverseerBot` to get responses
- Price check queries (`what's SOL price?`)
- Token safety checks (share a contract address)
- Response timing (15–30 min on Basic/Pro tier)
- Example interactions & FAQ

---

### [WALLET_UI_GUIDE.md](./WALLET_UI_GUIDE.md) 💰
Dashboard wallet features and manual control tools.

- Setting up Solana, ETH, and BSC wallet tracking
- Using the Wallet tab in the dashboard
- Running manual token safety checks and price checks via the Tools tab
- API usage examples for the wallet and tools endpoints

---

## 🛡️ Safety & Best Practices

### [TWITTER_BEST_PRACTICES.md](./TWITTER_BEST_PRACTICES.md) 🐦
Avoiding shadow bans and Twitter API restrictions.

- Bot rate usage (`<5%` of Twitter's limits — very safe)
- Randomized posting intervals to appear human
- Signs of shadow banning and recovery steps
- How to adjust broadcast frequency

---

## 🔧 Technical Reference

### [DOCUMENTATION.md](./DOCUMENTATION.md) 📘
Comprehensive technical guide.

- Architecture (single-process Flask + APScheduler)
- Installation and setup
- Full configuration reference
- API endpoint reference
- Webhook integration
- Security setup
- Deployment guide
- Troubleshooting

---

## 🔐 Security & Deployment

### [SECURITY_GUIDE.md](./SECURITY_GUIDE.md) 🔒
Credential management and security hardening.

- Generating strong admin passwords and webhook keys
- Protecting the dashboard and API (HTTP Basic Auth)
- Securing the game event webhook
- Platform-specific deployment notes (Render, Heroku, Docker)
- Security best practices and DO/DON'T list

### [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) ✅
Step-by-step pre-deployment verification.

- Environment variable checklist
- Local testing steps
- Post-deployment smoke tests
- Ongoing maintenance schedule

---

## 📦 Dependencies

### [DEPENDENCIES.md](./DEPENDENCIES.md)
Python dependency notes, version constraints, and optional extras.

---

## 🎯 Quick Task Guide

| I want to… | Go to |
|------------|-------|
| Install and run the bot | [README.md — Quick Start](./README.md#-quick-start) |
| Interact on Twitter | [USER_INTERACTION_GUIDE.md](./USER_INTERACTION_GUIDE.md) |
| Set up wallet tracking | [WALLET_UI_GUIDE.md](./WALLET_UI_GUIDE.md) |
| Avoid shadow bans | [TWITTER_BEST_PRACTICES.md](./TWITTER_BEST_PRACTICES.md) |
| Secure my deployment | [SECURITY_GUIDE.md](./SECURITY_GUIDE.md) |
| Deploy to production | [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) |
| Understand the architecture | [DOCUMENTATION.md](./DOCUMENTATION.md) |
| Access the dashboard | [README.md — Access the Dashboard](./README.md#access-the-dashboard) |
| Troubleshoot issues | [README.md — Troubleshooting](./README.md#-troubleshooting) |
| Call the API | [README.md — API Reference](./README.md#-api-reference) |

---

## 📂 File Overview

```
overseer-bot-ai/
│
├── 💻 CODE
│   ├── overseer_bot.py          # Main application (Flask + APScheduler + all bot logic)
│   ├── api_client.py            # HTTP polling client & alert aggregation
│   ├── gunicorn_config.py       # Production server config (workers=1)
│   ├── setup_env.py             # Interactive .env generator
│   ├── test_twitter_bot.py      # Unit test suite
│   ├── render.yaml              # Render.com deployment manifest
│   ├── requirements.txt
│   ├── requirements-lock.txt
│   └── .env.example             # Environment template (no secrets)
│
├── 📖 DOCUMENTATION
│   ├── README.md                # START HERE
│   ├── DOCUMENTATION_INDEX.md   # This file
│   ├── DOCUMENTATION.md         # Full technical reference
│   ├── DEPLOYMENT_CHECKLIST.md  # Deployment verification
│   ├── SECURITY_GUIDE.md        # Security hardening
│   ├── TWITTER_BEST_PRACTICES.md
│   ├── USER_INTERACTION_GUIDE.md
│   ├── WALLET_UI_GUIDE.md
│   └── DEPENDENCIES.md
```

---

<div align="center">

**All documentation centralized and current.**  
*The Overseer provides guidance. The wasteland is documented.*

</div>
