# Token-Scalper Integration Guide

## Overview

The Overseer Bot now integrates advanced features from the Token-scalper bot, adding sophisticated cryptocurrency safety analysis, rug pull detection, and airdrop discovery capabilities.

## New Features

### 1. Token Safety Checker

The bot can now analyze token contracts for safety issues including:

- **Honeypot Detection** - Identifies tokens that prevent selling
- **Tax Analysis** - Warns about excessive buy/sell taxes
- **Risk Scoring** - 0-100 scale (higher = more dangerous)
- **Contract Verification** - Checks if contract is verified

**Usage in Twitter Mentions:**
```
@OverseerBot is 0x1234...5678 safe?
@OverseerBot check this token 0xABCD...
@OverseerBot scam check 0x9876...
```

**Responses:**
- ✅ Low risk (0-30): "No major red flags detected"
- ⚠️ Medium risk (31-70): "Proceed with caution"
- 🚨 High risk (71-100): "HIGH RISK detected"
- 🛑 Honeypot: "HONEYPOT DETECTED - AVOID"

### 2. Rug Pull Alerts

Receives and posts alerts from Token-scalper bot about suspicious tokens:

**Webhook Endpoint:** `/token-scalper-alert`

**Alert Types:**
- Developer wallet dumping tokens
- Suspicious contract modifications
- Liquidity removal
- Large holder sells

**Example Alert:**
```
🛑 RUG PULL WARNING 🛑

Token: ScamCoin
Contract: 0x1234...
Severity: HIGH

Developer dumping 50% of holdings

The wasteland claims another scam.

#RugPull #CryptoScam #StaySafe

🎮 https://www.atomicfizzcaps.xyz
```

### 3. High Potential Token Signals

Posts about tokens with high opportunity scores:

**Criteria:**
- Strong liquidity
- Verified contracts
- Good developer reputation
- Positive sentiment
- Technical indicators

**Example Signal:**
```
🚀 HIGH POTENTIAL TOKEN 🚀

Token: GoodCoin
Score: 88/100
Signals: High liquidity • Verified contract • Strong community

Opportunity detected in the wasteland.

DYOR • Not Financial Advice

🎮 https://www.atomicfizzcaps.xyz
```

### 4. Airdrop Announcements

Discovers and shares legitimate airdrop opportunities:

**Features:**
- Quality filtering
- Value estimation
- Legitimacy verification
- Direct links

**Example Announcement:**
```
🎁 AIRDROP OPPORTUNITY 🎁

Project: NewProtocol
Est. Value: $500-1000
Link: https://protocol.xyz

Free caps detected. The wasteland provides.

Verify legitimacy • DYOR

🎮 https://www.atomicfizzcaps.xyz
```

## Integration with Token-Scalper Bot

### Webhook Setup

The Overseer Bot exposes a webhook endpoint that Token-scalper can call:

**Endpoint:** `POST /token-scalper-alert`

**Payload Format:**
```json
{
  "type": "rug_pull",
  "token_name": "ScamToken",
  "token_address": "0x...",
  "severity": "high",
  "details": "Developer dumping 50% of holdings",
  "timestamp": "2026-02-10T09:00:00Z"
}
```

**Alert Types:**
1. `rug_pull` - Scam/rug pull warning
2. `high_potential` - High opportunity token
3. `airdrop` - Airdrop opportunity

### Token-Scalper Configuration

Add to Token-scalper's `config.json`:

```json
{
  "social_media": {
    "enabled": true,
    "overseer_bot_enabled": true,
    "overseer_webhook_url": "https://your-bot-url.com/token-scalper-alert",
    "overseer_api_key": "your_api_key_here",
    "min_risk_score": 70,
    "alert_on_rug_pull": true,
    "alert_on_high_potential": true
  }
}
```

## Query Examples

### Token Safety Queries
```
User: "@OverseerBot is 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb safe?"
Bot: "✅ Risk Score: 25/100. No major red flags detected. DYOR. [link]"

User: "@OverseerBot check scam 0xBADC0FFEE..."
Bot: "🛑 HONEYPOT DETECTED. This token is contaminated. The wasteland claims another scam. Avoid. [link]"
```

### General Safety Queries
```
User: "@OverseerBot how to check if token is safe?"
Bot: "Safety checks: Look for honeypots, high taxes, locked liquidity. The wasteland is full of scams. [link]"
```

### Airdrop Queries
```
User: "@OverseerBot any good airdrops?"
Bot: "🎁 Airdrop intel coming soon. The Overseer monitors opportunities. Stay alert. [link]"
```

## Personality Integration

All Token-scalper features maintain the Overseer's Fallout-themed personality:

**Rug Pull Alerts:**
- "The wasteland claims another scam."
- "Vault-Tec Market Surveillance detected suspicious activity."
- "Overseer protocols: Avoid this contamination."

**High Potential:**
- "Opportunity detected in the wasteland."
- "FizzCo Analytics: Potential moonshot identified."
- "The Overseer sees potential here."

**Airdrops:**
- "Free caps detected. The wasteland provides."
- "Vault-Tec Airdrop Alert: Opportunity incoming."
- "Claim your share of the wasteland economy."

**Safety Checks:**
- "This token is contaminated."
- "The wasteland is full of scams."
- "Vault-Tec safety protocol activated."

## Security Considerations

### Token Safety Checks
- **Rate Limited**: API calls are cached for 1 hour
- **No Trading**: Only analysis, no actual trading
- **Third-party API**: Uses honeypot.is API
- **Not Financial Advice**: All responses include disclaimers

### Webhook Security
- **Validate Payloads**: Check source and structure
- **API Key**: Optional authentication
- **Error Handling**: Failed alerts don't crash bot
- **Logging**: All alerts logged for audit

## Technical Implementation

### Token Safety Checker
```python
check_token_safety(token_address, chain='eth')
```
- Uses honeypot.is API
- Returns risk assessment
- Caches results
- Handles errors gracefully

### Alert Handlers
- `handle_rug_pull_alert()` - Posts scam warnings
- `handle_high_potential_alert()` - Posts opportunities
- `handle_airdrop_alert()` - Posts airdrops

### Response Enhancement
- Regex pattern matching for contract addresses
- Contextual analysis of queries
- Personality-consistent responses
- Character limit compliance

## Testing

### Test Token Safety Check
```python
# Test with a known safe token
result = check_token_safety('0x1234...', 'eth')
print(f"Safe: {result['is_safe']}")
print(f"Risk: {result['risk_score']}/100")
```

### Test Webhook
```bash
curl -X POST http://localhost:5000/token-scalper-alert \
  -H "Content-Type: application/json" \
  -d '{
    "type": "rug_pull",
    "token_name": "TestToken",
    "token_address": "0x123...",
    "severity": "high",
    "details": "Test alert"
  }'
```

## Future Enhancements

Potential additions:
- **Developer reputation tracking** - Track scam devs
- **Automated airdrop finding** - Schedule searches
- **Multi-chain support** - BSC, Polygon, etc.
- **AI analysis integration** - GPT-4 risk assessment
- **Community voting** - Token safety crowdsourcing
- **Whitelist/blacklist** - Known good/bad tokens

## Troubleshooting

### Safety Checks Failing
- Check honeypot.is API status
- Verify token address format
- Check network connectivity
- Review cache expiration

### Webhook Not Receiving
- Verify endpoint URL
- Check firewall/port settings
- Test with curl
- Review logs for errors

### Responses Too Long
- Truncation logic in place
- Fallback messages used
- Review character limits
- Check emoji usage

## Conclusion

The Token-scalper integration transforms the Overseer Bot into a comprehensive crypto safety advisor, protecting the community from scams while identifying legitimate opportunities. All features maintain the bot's unique Fallout-themed personality while providing valuable, actionable intelligence.

**Remember:** All analysis is for informational purposes only. Always DYOR (Do Your Own Research) and never invest more than you can afford to lose.

---

*"The wasteland is full of scams. The Overseer keeps watch."*  
— Overseer V-Bot, Vault 77
