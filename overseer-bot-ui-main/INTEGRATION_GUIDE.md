# 🔗 Integration Guide - Event Communication System

This guide explains how to integrate overseer-bot-ui with overseer-bot-ai and Token-scalper for unified event communication and monitoring.

## Overview

The overseer-bot-ui acts as a central dashboard that aggregates alerts and status from multiple external systems:

- **overseer-bot-ai**: AI-powered bot for intelligent trading decisions
- **Token-scalper**: Automated trading bot for token opportunities
- **overseer-bot-ui**: Central monitoring dashboard (this application)

## Architecture

```
┌─────────────────┐         ┌──────────────────┐
│ overseer-bot-ai │         │ Token-scalper    │
│                 │         │                  │
│ /api/status     │         │ /api/status      │
│ /api/alerts     │         │                  │
└────────┬────────┘         └────────┬─────────┘
         │                           │
         │  REST API (polling)       │
         │  every 10-30s             │
         │                           │
         └───────────┬───────────────┘
                     ↓
         ┌─────────────────────┐
         │ overseer-bot-ui     │
         │                     │
         │ - API Client        │
         │ - Dashboard UI      │
         │ - Alert Display     │
         │ - Health Monitor    │
         └─────────────────────┘
```

## Expected API Endpoints

### overseer-bot-ai

The overseer-bot-ai service should implement the following REST endpoints:

#### 1. Status Endpoint

**Endpoint:** `GET /api/status`

**Purpose:** Health check and current bot status

**Authentication:** Bearer token (optional)
```http
Authorization: Bearer YOUR_API_KEY
```

**Response Format:**
```json
{
  "status": "running",
  "uptime": "2h 15m 30s",
  "version": "1.0.0",
  "timestamp": "2026-02-11T22:45:00Z",
  "active_trades": 3,
  "total_alerts": 15
}
```

**Fields:**
- `status` (string): Current status - `"running"`, `"stopped"`, `"error"`
- `uptime` (string): How long the bot has been running
- `version` (string): Bot version number
- `timestamp` (string): ISO 8601 timestamp
- `active_trades` (integer, optional): Number of active trades
- `total_alerts` (integer, optional): Total alerts generated

#### 2. Alerts Endpoint

**Endpoint:** `GET /api/alerts`

**Purpose:** Retrieve recent alerts and events

**Query Parameters:**
- `limit` (integer, optional): Maximum number of alerts to return (default: 50)
- `since` (string, optional): ISO 8601 timestamp to get alerts after

**Authentication:** Bearer token (optional)
```http
Authorization: Bearer YOUR_API_KEY
```

**Response Format:**
```json
[
  {
    "id": "alert-123",
    "type": "trade",
    "timestamp": "2026-02-11T22:40:00Z",
    "message": "Executed BUY order for SOL/USDT",
    "data": {
      "symbol": "SOL/USDT",
      "action": "BUY",
      "amount": 10.5,
      "price": 155.75,
      "total": 1635.375
    },
    "severity": "info"
  },
  {
    "id": "alert-124",
    "type": "rugpull",
    "timestamp": "2026-02-11T22:42:15Z",
    "message": "Potential rugpull detected for token XYZ",
    "data": {
      "token_address": "0x123...",
      "token_name": "ScamCoin",
      "risk_score": 95,
      "reason": "Liquidity removed"
    },
    "severity": "critical"
  },
  {
    "id": "alert-125",
    "type": "airdrop",
    "timestamp": "2026-02-11T22:43:00Z",
    "message": "New airdrop opportunity detected",
    "data": {
      "token_name": "NewToken",
      "airdrop_amount": 1000,
      "claim_url": "https://example.com/claim"
    },
    "severity": "info"
  }
]
```

**Alert Types:**
- `trade` - Trade execution alerts (buy/sell)
- `rugpull` - Rugpull detection warnings
- `airdrop` - Airdrop opportunities
- `status` - Status updates and heartbeats
- `error` - Error messages
- `warning` - Warning messages

**Severity Levels:**
- `info` - Informational messages
- `warning` - Warning messages
- `critical` - Critical alerts requiring attention

### Token-scalper

The Token-scalper service should implement:

#### Status Endpoint

**Endpoint:** `GET /api/status`

**Purpose:** Health check and current bot status

**Authentication:** Bearer token (optional)
```http
Authorization: Bearer YOUR_API_KEY
```

**Response Format:**
```json
{
  "status": "running",
  "uptime": "5h 32m 10s",
  "version": "2.1.0",
  "timestamp": "2026-02-11T22:45:00Z",
  "monitored_tokens": 25,
  "active_positions": 5
}
```

## Event Schema

All events/alerts follow a common schema for consistency:

```typescript
interface Alert {
  id: string;              // Unique alert identifier
  type: string;            // Alert type (trade, rugpull, airdrop, status, etc.)
  timestamp: string;       // ISO 8601 timestamp
  message: string;         // Human-readable message
  data: object;            // Alert-specific data
  severity?: string;       // Optional: info, warning, critical
  source?: string;         // Optional: System that generated the alert
}
```

### Alert Type Details

#### Trade Alert
```json
{
  "type": "trade",
  "data": {
    "symbol": "SOL/USDT",
    "action": "BUY" | "SELL",
    "amount": 10.5,
    "price": 155.75,
    "total": 1635.375,
    "exchange": "binance"
  }
}
```

#### Rugpull Alert
```json
{
  "type": "rugpull",
  "data": {
    "token_address": "0x123...",
    "token_name": "ScamCoin",
    "risk_score": 95,
    "reason": "Liquidity removed",
    "chain": "ethereum"
  }
}
```

#### Airdrop Alert
```json
{
  "type": "airdrop",
  "data": {
    "token_name": "NewToken",
    "token_symbol": "NEW",
    "airdrop_amount": 1000,
    "claim_url": "https://example.com/claim",
    "eligibility": "All holders"
  }
}
```

#### Status Alert
```json
{
  "type": "status",
  "data": {
    "status": "running",
    "uptime": "2h 15m",
    "last_activity": "2026-02-11T22:45:00Z"
  }
}
```

## Configuration

### Environment Variables

Add the following environment variables to your `.env` file:

```bash
# ============================================================
# EXTERNAL API INTEGRATION
# ============================================================

# Overseer-bot-ai Configuration
OVERSEER_BOT_AI_URL=https://your-overseer-ai.onrender.com
OVERSEER_BOT_AI_API_KEY=your_api_key_here

# Token-scalper Configuration
TOKEN_SCALPER_URL=https://your-token-scalper.onrender.com
TOKEN_SCALPER_API_KEY=your_api_key_here

# Polling Configuration
POLL_INTERVAL=15        # Seconds between API polls (default: 15)
REQUEST_TIMEOUT=5       # HTTP request timeout in seconds (default: 5)
```

### Configuration Options

#### `OVERSEER_BOT_AI_URL`
- **Description:** Base URL of the overseer-bot-ai service
- **Format:** Full URL including protocol (http/https)
- **Example:** `https://overseer-ai.onrender.com`
- **Required:** No (feature disabled if not set)

#### `OVERSEER_BOT_AI_API_KEY`
- **Description:** API key for authenticating with overseer-bot-ai
- **Format:** Bearer token string
- **Required:** Only if overseer-bot-ai requires authentication

#### `TOKEN_SCALPER_URL`
- **Description:** Base URL of the Token-scalper service
- **Format:** Full URL including protocol (http/https)
- **Example:** `https://token-scalper.onrender.com`
- **Required:** No (feature disabled if not set)

#### `TOKEN_SCALPER_API_KEY`
- **Description:** API key for authenticating with Token-scalper
- **Format:** Bearer token string
- **Required:** Only if Token-scalper requires authentication

#### `POLL_INTERVAL`
- **Description:** How often to poll external APIs (in seconds)
- **Default:** 15 seconds
- **Recommended Range:** 10-30 seconds
- **Note:** Lower values = more frequent updates but higher API usage

#### `REQUEST_TIMEOUT`
- **Description:** HTTP request timeout in seconds
- **Default:** 5 seconds
- **Recommended Range:** 3-10 seconds

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   cd overseer-bot-ui
   ```

2. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

3. **Configure external APIs**
   Edit `.env` and add your API endpoints:
   ```bash
   OVERSEER_BOT_AI_URL=http://localhost:8000
   OVERSEER_BOT_AI_API_KEY=dev-key-123
   
   TOKEN_SCALPER_URL=http://localhost:8001
   TOKEN_SCALPER_API_KEY=dev-key-456
   
   POLL_INTERVAL=15
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python overseer_bot.py
   ```

6. **Access the dashboard**
   Open your browser to `http://localhost:5000`

### Production Deployment

#### Using Render.com

1. **Create Web Service** on Render.com

2. **Set Environment Variables** in Render dashboard:
   ```
   OVERSEER_BOT_AI_URL=https://your-overseer-ai.onrender.com
   OVERSEER_BOT_AI_API_KEY=your_production_api_key
   TOKEN_SCALPER_URL=https://your-token-scalper.onrender.com
   TOKEN_SCALPER_API_KEY=your_production_api_key
   POLL_INTERVAL=20
   ```

3. **Deploy** and verify logs show:
   ```
   Flask monitoring UI started on port 5000
   External API polling started for overseer-bot-ai and token-scalper
   ```

#### Using Heroku

1. **Create Heroku app**
   ```bash
   heroku create your-overseer-ui
   ```

2. **Set config vars**
   ```bash
   heroku config:set OVERSEER_BOT_AI_URL=https://your-overseer-ai.herokuapp.com
   heroku config:set OVERSEER_BOT_AI_API_KEY=your_api_key
   heroku config:set TOKEN_SCALPER_URL=https://your-token-scalper.herokuapp.com
   heroku config:set TOKEN_SCALPER_API_KEY=your_api_key
   heroku config:set POLL_INTERVAL=20
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

#### Using Docker

1. **Create `.env` file** with your configuration

2. **Run with Docker**
   ```bash
   docker run -d \
     --env-file .env \
     -p 5000:5000 \
     overseer-bot-ui:latest
   ```

## Testing the Integration

### 1. Check Health Status

Access the dashboard at `http://localhost:5000` and verify:

- **External Systems Health** section shows status of both systems
- Status indicators show:
  - `✓ HEALTHY` - Service is reachable and responding
  - `✗ UNREACHABLE` - Service is not responding
  - `○ DISABLED` - Service URL not configured

### 2. Verify Alert Display

In the **Recent Alerts** section, you should see:
- Chronological list of alerts from both systems
- Alert types properly labeled (TRADE, RUGPULL, AIRDROP, STATUS)
- Color-coded alert borders
- Source system clearly indicated

### 3. Check API Endpoints

Test the new API endpoints:

```bash
# Check aggregated alerts
curl -u admin:password http://localhost:5000/api/alerts

# Check health status
curl -u admin:password http://localhost:5000/api/health
```

### 4. Monitor Logs

Check logs for successful polling:
```
INFO - Flask monitoring UI started on port 5000
INFO - External API polling started
INFO - Starting API polling (interval: 15s)
INFO - Alert added: status from overseer-bot-ai
```

## Troubleshooting

### No Alerts Appearing

**Problem:** Dashboard shows "No alerts received from external systems yet."

**Solutions:**
1. Check environment variables are set correctly
2. Verify external services are running and accessible
3. Check logs for connection errors
4. Test endpoints manually with curl:
   ```bash
   curl http://your-overseer-ai.com/api/status
   curl http://your-overseer-ai.com/api/alerts
   ```

### Health Status Shows "UNREACHABLE"

**Problem:** External system shows as unreachable

**Solutions:**
1. Verify the service is running
2. Check URL format (must include `http://` or `https://`)
3. Ensure API key is correct (if required)
4. Check network connectivity
5. Verify firewall rules allow outbound connections

### Authentication Errors

**Problem:** Logs show "401 Unauthorized" errors

**Solutions:**
1. Verify API keys are set correctly
2. Check if external services require authentication
3. Ensure API key format matches service expectations
4. Test authentication manually with curl:
   ```bash
   curl -H "Authorization: Bearer YOUR_KEY" http://service/api/status
   ```

### High CPU/Memory Usage

**Problem:** Application using too many resources

**Solutions:**
1. Increase `POLL_INTERVAL` to reduce API calls
2. Reduce `MAX_ALERTS` in `api_client.py` to store fewer alerts
3. Check for memory leaks in logs
4. Monitor external API response times

## API Reference

### New Dashboard Endpoints

#### GET /api/alerts

Returns aggregated alerts from all external systems.

**Authentication:** HTTP Basic Auth

**Response:**
```json
{
  "alerts": [
    {
      "timestamp": "2026-02-11T22:45:00Z",
      "type": "trade",
      "source": "overseer-bot-ai",
      "message": "Executed BUY order for SOL/USDT",
      "data": {...}
    }
  ],
  "health": {
    "overseer_bot_ai": {
      "status": "healthy",
      "last_check": "2026-02-11T22:45:12Z",
      "last_success": "2026-02-11T22:45:12Z",
      "error": null
    },
    "token_scalper": {
      "status": "healthy",
      "last_check": "2026-02-11T22:45:12Z",
      "last_success": "2026-02-11T22:45:12Z",
      "error": null
    }
  }
}
```

#### GET /api/health

Returns health status of external systems only.

**Authentication:** HTTP Basic Auth

**Response:**
```json
{
  "overseer_bot_ai": {
    "status": "healthy",
    "last_check": "2026-02-11T22:45:12Z",
    "last_success": "2026-02-11T22:45:12Z",
    "error": null
  },
  "token_scalper": {
    "status": "unhealthy",
    "last_check": "2026-02-11T22:45:12Z",
    "last_success": "2026-02-11T22:40:00Z",
    "error": "Connection timeout"
  }
}
```

**Status Values:**
- `healthy` - Service responding normally
- `unhealthy` - Service not responding or returning errors
- `disabled` - Service URL not configured
- `unknown` - Service status not yet checked

## Best Practices

### 1. Polling Frequency

- **Development:** 10-15 seconds for faster feedback
- **Production:** 15-30 seconds to reduce API load
- **High-Traffic:** 30-60 seconds if rate limits are an issue

### 2. Error Handling

- Services should gracefully handle missing external APIs
- Dashboard continues working even if external services are down
- Clear error messages help diagnose connectivity issues

### 3. Security

- Always use HTTPS in production
- Keep API keys secret and rotate regularly
- Use environment variables, never hardcode credentials
- Enable authentication on all external APIs

### 4. Monitoring

- Check dashboard health indicators regularly
- Monitor logs for connection errors
- Set up alerts for prolonged outages
- Track API response times

### 5. Scaling

- Consider adding Redis for alert caching in high-traffic scenarios
- Use webhooks instead of polling for real-time updates
- Implement rate limiting if needed
- Add database persistence for long-term alert storage

## Future Enhancements

Potential improvements to the integration system:

1. **WebSocket Support** - Real-time updates instead of polling
2. **Alert Filtering** - Filter alerts by type, severity, or source
3. **Alert Acknowledgment** - Mark alerts as read/acknowledged
4. **Historical Data** - Database storage for alert history
5. **Alert Rules** - Custom notification rules and thresholds
6. **Multi-System Support** - Easy addition of more external systems
7. **Grafana Integration** - Export metrics for visualization
8. **Slack/Discord Notifications** - Forward alerts to messaging platforms

## Support

For issues or questions:

1. Check logs in `overseer_ai.log`
2. Review troubleshooting section above
3. Verify environment configuration
4. Test external APIs independently
5. Open GitHub issue with detailed logs and configuration

## License

This integration guide is part of the overseer-bot-ui project.
