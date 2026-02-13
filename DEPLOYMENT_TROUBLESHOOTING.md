# Deployment Troubleshooting Guide

## Overview

This guide helps diagnose and fix deployment issues for the Overseer Bot.

## Common Deployment Issues

### Issue 1: Module Import Fails (Gunicorn Cannot Start)

**Symptoms:**
- Gunicorn exits with status 1
- Error: "Traceback... importlib.import_module..."
- No open ports detected

**Root Cause:**
The bot module initialization was failing when Twitter credentials were not configured, preventing Gunicorn from importing the application.

**Solution (✅ FIXED):**
The bot now includes graceful degradation for missing Twitter credentials:
- The bot detects if all required Twitter credentials are present
- If credentials are missing, the bot logs a warning and runs in **monitoring-only mode**
- The Flask app starts successfully regardless of Twitter credential status
- All Twitter-dependent functions check `TWITTER_ENABLED` flag before executing

**Monitoring-Only Mode Features:**
When Twitter credentials are not configured:
- ✅ Flask monitoring dashboard is accessible
- ✅ Price monitoring continues (but alerts are not tweeted)
- ✅ Webhook endpoints are available
- ✅ Bot logs all activities
- ❌ Twitter posting is disabled
- ❌ Twitter mention checking is disabled
- ❌ Retweet functionality is disabled

### Issue 2: Missing Environment Variables

**Symptoms:**
- Bot starts in monitoring-only mode
- Logs show: "⚠️ Twitter credentials not fully configured!"

**Solution:**
Set all required environment variables in Render.com dashboard:
1. Go to your service → Environment tab
2. Add these variables:
   - `CONSUMER_KEY` - Your Twitter API consumer key
   - `CONSUMER_SECRET` - Your Twitter API consumer secret
   - `ACCESS_TOKEN` - Your Twitter access token
   - `ACCESS_SECRET` - Your Twitter access secret
   - `BEARER_TOKEN` - Your Twitter bearer token
3. Save changes
4. Redeploy the service

### Issue 3: Default Admin Password Warning

**Symptoms:**
- Logs show: "⚠️ SECURITY WARNING: Using default admin password!"

**Solution:**
1. Generate a secure password:
   ```bash
   openssl rand -base64 32
   ```
2. Set the `ADMIN_PASSWORD` environment variable in Render.com dashboard
3. Redeploy

## Deployment Checklist

Before deploying to Render.com:

- [ ] All Twitter API credentials are configured in environment variables
- [ ] `ADMIN_PASSWORD` is set to a secure value (not default)
- [ ] `WEBHOOK_API_KEY` is configured if using webhooks
- [ ] Wallet credentials are configured if using wallet features (optional)
- [ ] Port binding is configured (`$PORT` environment variable is used)

## Testing Deployment Locally

Test the deployment configuration locally before pushing:

```bash
# Test without credentials (monitoring-only mode)
gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 2 --timeout 120 overseer_bot:app

# Test with credentials
export CONSUMER_KEY=your_key
export CONSUMER_SECRET=your_secret
export ACCESS_TOKEN=your_token
export ACCESS_SECRET=your_secret
export BEARER_TOKEN=your_bearer_token
gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 2 --timeout 120 overseer_bot:app
```

## Monitoring Deployment Health

After deployment, check these indicators:

1. **Service Status**: Should show "Live" in Render.com dashboard
2. **Logs**: Look for:
   - ✅ "Twitter clients initialized successfully" (if credentials are set)
   - ⚠️ "Twitter credentials not fully configured" (if in monitoring mode)
   - ✅ "Flask app initialized. Ready to serve on port..."
   - ✅ "VAULT-TEC OVERSEER ONLINE"

3. **Monitoring Dashboard**: Access `https://your-service.onrender.com/` to verify:
   - Dashboard loads correctly
   - Uptime is counting
   - Scheduler jobs are listed
   - Price data is being fetched

## Emergency Recovery

If deployment completely fails:

1. **Check Render.com logs** for the exact error message
2. **Verify Python version** - Bot requires Python 3.9+
3. **Check dependencies** - Ensure `requirements.txt` is up-to-date
4. **Roll back** to previous working version if needed
5. **Contact support** with full error logs

## Getting Help

If issues persist:
1. Collect the full deployment logs from Render.com
2. Check if the issue is listed in this guide
3. Review the code changes in the latest commit
4. Open an issue with:
   - Full error message
   - Deployment logs
   - Environment configuration (without sensitive values)

## Technical Details

### Module Initialization Flow

```
1. Import dependencies (tweepy, flask, etc.)
2. Load configuration from environment variables
3. Check if Twitter credentials are complete → Set TWITTER_ENABLED flag
4. Initialize wallet clients (optional, with error handling)
5. Initialize Twitter clients (if TWITTER_ENABLED, with error handling)
6. Initialize Flask app
7. Start background scheduler
8. Post activation tweet (if TWITTER_ENABLED)
9. Ready to serve requests
```

### Error Handling Strategy

The bot uses defensive programming to ensure it can always start:
- All optional features have `try-except` blocks
- Twitter client initialization is wrapped in error handling
- All Twitter functions check `TWITTER_ENABLED` before executing
- Missing credentials result in warnings, not errors
- Flask app initializes regardless of other failures

This ensures that even if Twitter, wallets, or other features fail, the monitoring dashboard remains accessible.
