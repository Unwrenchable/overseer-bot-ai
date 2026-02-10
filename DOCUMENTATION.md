# 📚 Overseer Bot AI - Complete Documentation

**Version:** 2.0  
**Last Updated:** 2026-02-10  
**Status:** Production Ready

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Architecture - Bot & Dashboard Integration](#-architecture)
3. [Installation & Setup](#-installation--setup)
4. [Configuration](#-configuration)
5. [Features Deep Dive](#-features-deep-dive)
6. [API Reference](#-api-reference)
7. [Webhook Integration](#-webhook-integration)
8. [Security Setup](#-security-setup)
9. [Deployment Guide](#-deployment-guide)
10. [Monitoring & Maintenance](#-monitoring--maintenance)
11. [Troubleshooting](#-troubleshooting)
12. [Advanced Topics](#-advanced-topics)

---

## 🎯 Overview

### What is Overseer Bot AI?

Overseer Bot AI is a production-ready Twitter automation bot that combines cryptocurrency intelligence with Fallout-themed personality. It serves multiple purposes:

- **Social Media Automation** - Automated Twitter engagement with personality
- **Cryptocurrency Intelligence** - Real-time price monitoring and alerts
- **Token Safety Analysis** - Honeypot detection and risk scoring
- **Event Broadcasting** - Game and blockchain event announcements
- **Web Monitoring** - Real-time dashboard for oversight

### Key Capabilities

✅ **Twitter Automation** - Posts, mentions, retweets, scheduled content  
✅ **Price Monitoring** - SOL, BTC, ETH tracking with configurable alerts  
✅ **Safety Checker** - Token contract analysis via honeypot.is API  
✅ **Webhook Server** - Receives events from games and external bots  
✅ **Monitoring Dashboard** - Beautiful Vault-Tec themed web UI  
✅ **Multi-Platform** - Runs on Render, Heroku, Railway, AWS, etc.

---

## 🏗️ Architecture

### **IMPORTANT: Bot & Dashboard Run Together** ✅

**Q: Will the Twitter bot and web dashboard interfere with each other?**  
**A: NO - They are designed to work together seamlesslyecho ___BEGIN___COMMAND_OUTPUT_MARKER___ ; PS1= ; PS2= ; unset HISTFILE ; EC=0 ; echo ___BEGIN___COMMAND_DONE_MARKER___0 ; }*

The application runs as a **single process** with two components:



### How They Work Together

1. ✅ **Flask** runs in main thread (non-blocking)
2. ✅ **APScheduler** runs in background thread
3. ✅ Both share memory (activity logs, price cache)
4. ✅ Thread-safe locks prevent conflicts
5. ✅ Dashboard shows real-time bot activity

### Benefits of Running Together

- 🎯 Monitor bot status without SSH access
- 📊 View real-time price data and alerts  
- 🔍 Debug issues through activity logs
- ⏰ Check scheduler job timing
- 🔒 Single deployment, single configuration

### Performance Impact

- **Minimal** - Flask is lightweight when idle
- **No degradation** for Twitter tasks
- **Dashboard overhead** only when accessed
- **Recommended** for production use

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.9+
- pip package manager
- Twitter Developer Account
- 512MB RAM minimum

### Quick Start

