# Overseer Bot Monitoring UI - Visual Guide

## Dashboard Overview

The monitoring dashboard provides a comprehensive view of the Overseer Bot's status and activities in a Vault-Tec themed interface.

### Access
- **Development URL**: `http://localhost:5000/` (or the port specified in `PORT` environment variable)
- **Production URL**: `https://your-server.com/` (HTTPS required for production)
- **Design**: Dark theme with Fallout-inspired green/orange color scheme
- **Layout**: Responsive design for desktop and mobile

## Dashboard Sections

### 1. Header (Top Banner)
```
☢️ VAULT-TEC OVERSEER MONITORING TERMINAL ☢️
              VAULT 77 - REAL-TIME STATUS
           [REFRESH DATA] button
```
- Orange/amber header with glowing text effect
- Prominent refresh button for manual updates
- Vault-Tec branding consistent with bot personality

### 2. Status Grid (4 Cards)
Four status cards displayed in a grid:

**Card 1: UPTIME**
- Shows: Days, hours, minutes since bot start
- Example: "0d 2h 15m"
- Color: Orange text on dark background

**Card 2: SCHEDULER STATUS**
- Shows: Number of active scheduled jobs
- Example: "6 JOBS"
- Indicates automation health

**Card 3: PRICE CACHE**
- Shows: Number of cached token prices
- Example: "3" (for SOL, BTC, ETH)
- Tracks data freshness

**Card 4: SAFETY CACHE**
- Shows: Number of token safety checks cached
- Example: "5"
- Shows recent safety scan activity

### 3. Token Price Monitoring Table
```
📊 TOKEN PRICE MONITORING
┌──────────┬─────────┬───────────┬─────────────────────┐
│ Token    │ Price   │ 24h Change│ Last Updated        │
├──────────┼─────────┼───────────┼─────────────────────┤
│ SOL/USDT │ $155.75 │ +6.50%    │ 2026-02-10 09:42:15│
│ BTC/USDT │ $43,125 │ -5.20%    │ 2026-02-10 09:42:15│
│ ETH/USDT │ $3,120  │ +3.40%    │ 2026-02-10 09:42:15│
└──────────┴─────────┴───────────┴─────────────────────┘
```
- Green text for positive changes
- Red text for negative changes
- Real-time price data
- Timestamp shows data freshness

### 4. Scheduled Jobs Table
```
⏰ SCHEDULED JOBS
┌────────────────────────┬─────────────────────┐
│ Job Name               │ Next Run            │
├────────────────────────┼─────────────────────┤
│ overseer_broadcast     │ 2026-02-10 11:45:00│
│ overseer_respond       │ 2026-02-10 10:05:00│
│ overseer_retweet_hunt  │ 2026-02-10 11:00:00│
│ overseer_diagnostic    │ 2026-02-11 08:00:00│
│ check_price_alerts     │ 2026-02-10 09:50:00│
│ post_market_summary    │ 2026-02-10 14:00:00│
└────────────────────────┴─────────────────────┘
```
- Shows all scheduled automation
- Next run time for each job
- Helps predict bot activity

### 5. Recent Activity Log
```
📝 RECENT ACTIVITY
┌─────────────────────────────────────────────────────┐
│ 2026-02-10 09:42:15                                 │
│ MARKET_SUMMARY: Posted summary with 3 tokens       │
├─────────────────────────────────────────────────────┤
│ 2026-02-10 09:35:23                                 │
│ MENTION_REPLY: @user123: what is the sol price?... │
├─────────────────────────────────────────────────────┤
│ 2026-02-10 09:30:45                                 │
│ PRICE_ALERT: SOL/USDT +6.50% - $155.75            │
├─────────────────────────────────────────────────────┤
│ 2026-02-10 09:15:12                                 │
│ BROADCAST: status_report - 245 chars               │
├─────────────────────────────────────────────────────┤
│ 2026-02-10 09:00:00                                 │
│ STARTUP: Bot activated - OVERSEER                  │
└─────────────────────────────────────────────────────┘
```
- Scrollable activity log (last 50 events)
- Newest activities at top
- Activity types: STARTUP, BROADCAST, PRICE_ALERT, MENTION_REPLY, MARKET_SUMMARY, ERROR
- Timestamps for debugging
- Brief descriptions of each activity

### 6. API Endpoints Reference
```
🔗 API ENDPOINTS
• /api/status - Bot status JSON
• /api/prices - Current prices JSON
• /api/jobs - Scheduler jobs JSON
• /api/activities - Recent activities JSON
• POST /overseer-event - Webhook for events
• POST /token-scalper-alert - Webhook for alerts
```
- Links to JSON endpoints
- Useful for integrations
- Click to view raw data

## Color Scheme

**Background Colors:**
- Main background: `#1a1a1a` (dark gray)
- Section background: `#0a0a0a` (darker)
- Card background: `#0f0f0f` (medium dark)

**Text Colors:**
- Primary text: `#00ff00` (bright green - terminal style)
- Headers: `#ffaa00` (amber/orange - Vault-Tec)
- Positive values: `#00ff00` (green)
- Negative values: `#ff4444` (red)
- Timestamps: `#888888` (gray)

**Borders:**
- Main borders: `#ffaa00` (amber/orange)
- Section borders: `#00ff00` (green)
- Card borders: `#00aa00` (darker green)

**Effects:**
- Text shadow on headers: Glowing amber effect
- Hover effects on buttons
- Responsive grid layout

## Usage Tips

1. **Monitoring Health**: Check uptime and job counts to ensure bot is running properly
2. **Price Tracking**: Monitor token prices and changes for market awareness
3. **Activity Tracking**: Review recent activities to see what bot has been doing
4. **Error Detection**: Look for ERROR entries in activity log
5. **Job Timing**: Check next run times to predict when bot will post
6. **API Integration**: Use JSON endpoints for custom monitoring tools

## Mobile View

The dashboard is responsive and adapts to mobile screens:
- Status cards stack vertically
- Tables scroll horizontally if needed
- Text remains readable
- All functionality available

## Performance

- Dashboard loads instantly (static HTML rendering)
- Minimal server resources (Flask development server)
- Auto-refresh requires manual button click
- No real-time WebSocket (reduces complexity)

## Security Considerations

**⚠️ CRITICAL: Production Security Requirements**

The monitoring dashboard is designed for development and internal use. Before deploying to production, you **MUST** implement these security measures:

### 1. Authentication (REQUIRED for Production)
- The dashboard has NO authentication by default
- Anyone who can reach your server can view bot activities and data
- **Solution**: Add authentication middleware or use a reverse proxy with auth
- Example: HTTP Basic Auth, OAuth, or IP whitelisting

### 2. HTTPS (REQUIRED for Production)
- The development server uses HTTP (unencrypted)
- Bot activities, price data, and operational details are sent in plain text
- **Solution**: Use a reverse proxy (nginx/Apache) with SSL/TLS certificates
- Never expose the dashboard over HTTP on public networks

### 3. Production WSGI Server (REQUIRED for Production)
- Flask's development server is NOT production-ready
- Cannot handle concurrent requests efficiently or securely
- **Solution**: Use Gunicorn, uWSGI, or similar production WSGI server
- Example: `gunicorn --bind 0.0.0.0:5000 overseer_bot:app`

### 4. Network Binding
- Currently binds to `0.0.0.0` (all interfaces) for accessibility
- **Development**: OK for local testing
- **Production**: Consider binding to `127.0.0.1` and using reverse proxy
- Or implement firewall rules to restrict access

### 5. Data Exposure
- Dashboard shows: bot activities, prices, timestamps, errors
- Does NOT show: Twitter credentials, API keys, secrets
- Still consider this operational data sensitive

### Security Checklist for Production:
- [ ] Add authentication (HTTP Basic Auth minimum)
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Replace Flask dev server with Gunicorn/uWSGI
- [ ] Implement rate limiting
- [ ] Add firewall rules or IP whitelisting
- [ ] Monitor access logs
- [ ] Consider read-only database user if adding DB

### Development Use Only
For development and internal monitoring on trusted networks, the current setup is acceptable. The read-only nature prevents accidental damage, but the lack of authentication means anyone with network access can view your bot's operations.
