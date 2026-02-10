# Token Scalper Integration

## Overview

The Overseer Bot now includes advanced cryptocurrency price monitoring and alerting features, integrating token scalping functionality with the existing Fallout-themed personality.

## Features Added

### 1. Real-Time Price Monitoring
- Monitors multiple cryptocurrency tokens (SOL, BTC, ETH by default)
- Fetches live prices from Binance exchange using CCXT library
- Tracks 24-hour price changes, highs, lows, and volume
- Caches price data locally for comparison

### 2. Automated Price Alerts
- Detects significant price movements (configurable thresholds)
- Posts Twitter alerts when tokens surge or dip beyond thresholds
- Default thresholds: 5% for SOL, 3% for BTC, 4% for ETH
- Alerts include current price, percentage change, and 24h performance
- All alerts maintain the Overseer's Fallout-themed personality

### 3. Market Summary Reports
- Posts comprehensive market reports 3 times daily (8 AM, 2 PM, 8 PM)
- Shows current prices and 24h changes for all monitored tokens
- Uses emoji indicators (🟢 for gains, 🔴 for losses)
- Maintains wasteland-themed language

### 4. Price Query Responses
- Responds to Twitter mentions asking about token prices
- Supports queries for Bitcoin, Ethereum, and Solana
- Returns real-time price data with personality-driven responses
- Examples: "What's the SOL price?", "How's BTC doing?", "ETH market?"

### 5. Enhanced Market Context
- Integrates crypto market data into existing bot personality
- Adds market-themed Overseer commentary
- Maintains thematic consistency with Atomic Fizz Caps universe

## Configuration

### Monitored Tokens
Edit the `MONITORED_TOKENS` dictionary in `overseer_bot.py`:

```python
MONITORED_TOKENS = {
    'SOL/USDT': {
        'exchange': 'binance',
        'alert_threshold_up': 5.0,    # % increase to trigger alert
        'alert_threshold_down': 5.0,  # % decrease to trigger alert
        'check_interval': 5           # Minutes between checks
    },
    # Add more tokens here...
}
```

### Alert Frequency
- Price checks: Every 5 minutes (via scheduler)
- Market summaries: 8 AM, 2 PM, 8 PM daily
- Alerts only sent when thresholds exceeded

## Technical Implementation

### Dependencies
- **ccxt**: Cryptocurrency exchange integration library
- Supports 100+ exchanges (currently using Binance)
- Provides unified API for fetching market data

### Data Storage
- `price_cache.json`: Stores historical price data for comparison
- Enables detection of price changes over time
- Automatically created and updated

### Scheduler Jobs
New jobs added to APScheduler:
1. `check_price_alerts()` - Every 5 minutes
2. `post_market_summary()` - Cron schedule (3x daily)

### Functions Added
- `get_token_price()`: Fetches current price from exchange
- `calculate_price_change()`: Computes percentage change
- `check_price_alerts()`: Main monitoring loop
- `post_price_alert()`: Tweets price movement alerts
- `post_market_summary()`: Tweets market overview
- Enhanced `generate_contextual_response()`: Handles price queries

## Usage Examples

### Price Alert Tweet Example
```
🔔 MARKET ALERT 📈🚀

$SOL SURGE: +6.50%
Current: $155.75
24h Change: +8.23%

The wasteland economy shifts.

🎮 https://www.atomicfizzcaps.xyz
```

### Market Summary Tweet Example
```
📊 WASTELAND MARKET REPORT 📊

🟢 $SOL: $155.75 (+6.50%)
🔴 $BTC: $45,230.00 (-2.15%)
🟢 $ETH: $3,120.50 (+3.40%)

Market surveillance: nominal.

🎮 https://www.atomicfizzcaps.xyz
```

### Query Response Example
User: "@OverseerBot What's the SOL price?"

Bot: "@user 📈 $SOL: $155.75 (24h: +6.50%). The wasteland economy shifts. https://www.atomicfizzcaps.xyz"

## Personality Integration

All token scalping features maintain the Overseer's character:
- "The wasteland economy shifts."
- "Market radiation detected."
- "FizzCo Analytics reporting."
- "Vault-Tec market surveillance active."
- "The caps flow differently now."

## Customization

### Adding New Tokens
1. Add to `MONITORED_TOKENS` dictionary
2. Specify exchange, thresholds, and interval
3. Update price query keywords if needed

### Changing Exchanges
The CCXT library supports:
- Binance, Coinbase, Kraken, KuCoin
- Bitfinex, Huobi, OKX, and 100+ more

Simply change the `exchange` parameter in token config.

### Adjusting Alert Thresholds
Modify `alert_threshold_up` and `alert_threshold_down` values:
- Lower values = more frequent alerts
- Higher values = only major movements

### Scheduling Changes
Edit scheduler job parameters:
- Change `minutes` for price check frequency
- Modify `hour` in cron for summary timing

## Error Handling

The implementation includes:
- Try-catch blocks for API failures
- Logging of all errors and warnings
- Graceful fallback if price data unavailable
- Continues operation even if single token fails

## Security Notes

- No API keys required for public price data
- Uses read-only exchange APIs
- No trading or wallet access
- Purely informational/monitoring features

## Testing

Run the test suite:
```bash
python3 /tmp/test_token_features.py
```

Tests verify:
- Price data structure
- Calculation accuracy
- Configuration validity
- Cache operations
- Message formatting

## Future Enhancements

Potential additions:
- Support for more tokens/exchanges
- Historical price charts
- Trading volume analysis
- Multi-timeframe alerts (1h, 4h, 1d)
- Custom alert thresholds per user
- Technical indicator integration (RSI, MACD)
- Correlation analysis between tokens

## Troubleshooting

### No Alerts Being Posted
- Check if thresholds are too high
- Verify CCXT can access exchange API
- Review logs for fetch errors
- Ensure scheduler is running

### Incorrect Prices
- Verify exchange is operational
- Check token symbol format (BASE/QUOTE)
- Confirm exchange supports the pair
- Review CCXT documentation

### Rate Limiting
- CCXT handles rate limits automatically
- Reduce check frequency if needed
- Consider using multiple exchanges

## Integration Benefits

This integration provides:
1. **Real-time market intelligence** - Stay informed on crypto movements
2. **Automated monitoring** - No manual checking required
3. **Community engagement** - Followers get valuable market data
4. **Bot differentiation** - Unique combo of gaming + finance
5. **Traffic driver** - Market updates attract new followers
6. **Enhanced value** - More than just a game promotion bot

## Conclusion

The token scalper integration transforms the Overseer Bot from a simple game promotion tool into a comprehensive crypto-aware AI assistant while maintaining its unique Fallout-themed personality. The features are production-ready, well-tested, and seamlessly integrated with existing functionality.
