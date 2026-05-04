# 🚀 Deployment Checklist

Use this checklist to ensure secure deployment of the Overseer Bot AI with authentication.

## ⚠️ Security First: About .env Files

**CRITICAL:** Before you start:

- The `.env.example` file in the repository is a **TEMPLATE** (committed to Git)
- `.env.example` contains NO actual secrets, only placeholders
- NEVER put actual secrets in `.env.example`
- ALWAYS create a separate `.env` file for actual secrets (gitignored, NOT committed)

## Pre-Deployment (Local Testing)

- [ ] Copy `.env.example` to `.env` (create your own copy)
- [ ] Generate strong credentials:

  ```bash
  openssl rand -base64 32  # For ADMIN_PASSWORD
  openssl rand -hex 32     # For WEBHOOK_API_KEY
  ```

- [ ] Fill in all required environment variables in YOUR `.env` file (not .env.example!)
- [ ] Verify `.env` is in `.gitignore` (it is!)
- [ ] Test locally:

  ```bash
  # Development mode (Flask dev server)
  python overseer_bot.py

  # OR Production mode locally (Gunicorn)
  gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 2 overseer_bot:app
  # Should see security warning if using default password
  ```

- [ ] Test dashboard access (should require login)
- [ ] Test API endpoints (should require auth)
- [ ] Test webhooks (should require API key if configured)
- [ ] VERIFY `.env` is not committed: `git status` (should not show .env)

## Production Deployment

### Step 1: Environment Variables

Set these on your hosting platform (Render, Heroku, etc.):

#### Required

- [ ] `CONSUMER_KEY` — Twitter "API Key" (from the App's *Keys and tokens* page)
- [ ] `CONSUMER_SECRET` — Twitter "API Key Secret" (same page)
- [ ] `ACCESS_TOKEN` — Twitter "Access Token" (user-level; regenerate **after** setting Read+Write permissions)
- [ ] `ACCESS_SECRET` — Twitter "Access Token Secret" (paired with `ACCESS_TOKEN`)
- [ ] `BEARER_TOKEN` — App-only read token (shown on *Keys and tokens* page)
- [ ] `ADMIN_USERNAME` — Dashboard login (change from 'admin')
- [ ] `ADMIN_PASSWORD` — Dashboard password (use generated strong password)

#### Recommended

- [ ] `WEBHOOK_API_KEY` - For securing webhooks (highly recommended)
- [ ] `PORT` - Default 5000 (optional)

#### AI / LLM (at least one recommended for AI-generated tweets)

> The bot uses a **primary → fallback** AI chain. Set whichever keys you have;
> the bot automatically selects the best available provider in order.

| Priority | Variable | Provider | Where to get it |
|----------|----------|----------|-----------------|
| **Primary** | `XAI_API` | xAI (Grok) | [console.x.ai](https://console.x.ai/) |
| | `XAI_MODEL` | *(optional)* model name | Default: `grok-3-mini` |
| Fallback 1 | `OPENAI_API_KEY` | OpenAI / compatible | [platform.openai.com](https://platform.openai.com/api-keys) |
| | `OPENAI_BASE_URL` | *(optional)* | Override for Groq, Together, Ollama |
| | `LLM_MODEL` | *(optional)* | Default: `gpt-4o-mini` |
| Fallback 2 | `HUGGING_FACE_TOKEN` | Hugging Face | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |

- [ ] `XAI_API` — Primary AI (Grok) — **recommended if you have an xAI key**
- [ ] `OPENAI_API_KEY` — First fallback (OpenAI or compatible)
- [ ] `HUGGING_FACE_TOKEN` — Last-resort fallback (free tier available)

### Step 2: Verify Configuration

- [ ] All environment variables are set
- [ ] **NOT using default password** (`vault77secure`)
- [ ] **NOT using weak passwords** (< 20 characters)
- [ ] Credentials are unique (not reused from other services)

### Step 3: Deploy

- [ ] Push code to repository
- [ ] Trigger deployment on hosting platform
- [ ] Wait for deployment to complete
- [ ] Check logs for security warnings

### Step 4: Post-Deployment Testing

- [ ] Access dashboard URL (should prompt for login)
- [ ] Try wrong credentials (should reject with 401)
- [ ] Login with correct credentials (should succeed)
- [ ] Test API endpoint: `curl -u username:password https://your-bot/api/status`
- [ ] Test webhook without API key (should fail with 401 if key is set)
- [ ] Test webhook with API key (should succeed)
- [ ] Check logs for any Binance geo-block errors (should fallback to CoinGecko)
- [ ] Verify price data is being fetched successfully

### Step 5: Security Hardening

- [ ] Enable HTTPS (use Cloudflare, nginx, or hosting platform SSL)
- [ ] Configure firewall rules to restrict dashboard access (if possible)
- [ ] Set up monitoring/alerts for failed authentication attempts
- [ ] Document credentials in secure password manager

## Security Checks

### Critical

- [ ] ✅ Using HTTPS in production
- [ ] ✅ Not using default credentials
- [ ] ✅ Strong password (20+ characters, mixed case, numbers, symbols)
- [ ] ✅ Webhook API key is set (or consciously disabled)
- [ ] ✅ `.env` file is in `.gitignore` (never committed)

### Important

- [ ] ✅ Credentials stored in secure password manager
- [ ] ✅ Only authorized IPs can access dashboard (via firewall)
- [ ] ✅ Monitoring/logging enabled for security events
- [ ] ✅ Regular credential rotation scheduled (every 90 days)

### Recommended Security Measures

- [ ] ✅ Rate limiting on authentication endpoints
- [ ] ✅ Automated alerts for repeated failed logins
- [ ] ✅ Backup of environment variables in secure location
- [ ] ✅ Documentation of access procedures for team

## Troubleshooting

### Dashboard not accessible

- Check firewall rules
- Verify port is correct (default 5000)
- Check logs for startup errors

### Getting 401 Unauthorized

- Verify credentials are correct
- Check environment variables are set properly
- Try password without special shell characters first

### Webhooks failing with 401

- Verify `WEBHOOK_API_KEY` matches in both services
- Check Authorization header format: `Bearer <key>`
- Test with curl to isolate issue

### Binance geo-block errors

- Should automatically fallback to CoinGecko
- Check logs for "falling back to CoinGecko" message
- If CoinGecko also fails, check network connectivity

## Ongoing Maintenance

### Weekly

- [ ] Review access logs for suspicious activity
- [ ] Verify bot is functioning normally
- [ ] Check price data is being fetched

### Monthly

- [ ] Review and update firewall rules if needed
- [ ] Check for any security updates to dependencies
- [ ] Verify backups are working

### Quarterly (Every 90 days)

- [ ] Rotate credentials:
  - Generate new `ADMIN_PASSWORD`
  - Generate new `WEBHOOK_API_KEY`
  - Update in all services
- [ ] Review access logs
- [ ] Update dependencies: `pip install -U -r requirements.txt`

## Emergency Procedures

### Credentials Compromised

1. Immediately generate new credentials
2. Update environment variables on hosting platform
3. Restart service
4. Review access logs for unauthorized access
5. Document incident

### Dashboard Being Attacked

1. Check logs for attack patterns
2. Block attacking IPs at firewall level
3. Consider temporarily disabling dashboard
4. Rotate credentials as precaution
5. Report incident to hosting provider

## Support

For issues or questions:

1. Check `SECURITY_GUIDE.md` for detailed setup instructions
2. Check logs: `tail -f overseer_ai.log`
3. Open an issue on GitHub

---

**Last Updated**: 2026-02-10
**Version**: 1.0.0
