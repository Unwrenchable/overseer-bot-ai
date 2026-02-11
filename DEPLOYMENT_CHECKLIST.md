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
  python overseer_bot.py
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
- [ ] `CONSUMER_KEY` - Twitter API
- [ ] `CONSUMER_SECRET` - Twitter API
- [ ] `ACCESS_TOKEN` - Twitter API
- [ ] `ACCESS_SECRET` - Twitter API  
- [ ] `BEARER_TOKEN` - Twitter API
- [ ] `ADMIN_USERNAME` - Dashboard login (change from 'admin')
- [ ] `ADMIN_PASSWORD` - Dashboard password (use generated strong password)

#### Recommended
- [ ] `WEBHOOK_API_KEY` - For securing webhooks (highly recommended)
- [ ] `PORT` - Default 5000 (optional)

#### Optional
- [ ] `HUGGING_FACE_TOKEN` - For AI features

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
- [ ] Share webhook API key securely with Token-scalper admin

### Step 6: Configure Token-scalper Integration

If using Token-scalper bot:

- [ ] Update Token-scalper's `config.json`:
  ```json
  {
    "social_media": {
      "overseer_bot_enabled": true,
      "overseer_webhook_url": "https://your-overseer-bot.com/token-scalper-alert",
      "overseer_api_key": "your_WEBHOOK_API_KEY_here"
    }
  }
  ```
- [ ] Test webhook from Token-scalper
- [ ] Verify alerts appear in Overseer Bot logs

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

### Recommended
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
4. Update Token-scalper configuration
5. Review access logs for unauthorized access
6. Document incident

### Dashboard Being Attacked
1. Check logs for attack patterns
2. Block attacking IPs at firewall level
3. Consider temporarily disabling dashboard
4. Rotate credentials as precaution
5. Report incident to hosting provider

## Support

For issues or questions:
1. Check `SECURITY_GUIDE.md` for detailed setup instructions
2. Review `AUTHENTICATION_IMPLEMENTATION.md` for technical details
3. Check logs: `tail -f overseer_ai.log`
4. Open an issue on GitHub

---

**Last Updated**: 2026-02-10
**Version**: 1.0.0
