# Overseer Bot UI - CoinGecko Rate Limit Handling

## Problem
You are hitting CoinGecko's free API rate limits (429 errors). This causes price fetches to fail and can break your monitoring/alerts.

## Solution
Implement a simple in-memory cache and exponential backoff for CoinGecko requests. This will:
- Avoid repeated requests for the same token within a short window (e.g., 1 minute)
- Retry with increasing delay if a 429 is received

## Implementation Steps
1. Add a global dict to cache CoinGecko responses with timestamps.
2. Before making a request, check if a recent cached value exists (e.g., <60s old).
3. If a 429 is received, wait and retry (exponential backoff, up to a max wait).
4. Log when using cached data due to rate limiting.

## Example Code Snippet

Add to overseer_bot.py:

```python
COINGECKO_CACHE = {}
COINGECKO_CACHE_TTL = 60  # seconds
COINGECKO_BACKOFF = 5     # initial backoff in seconds
COINGECKO_MAX_BACKOFF = 60

def get_token_price_coingecko(symbol):
    ...
    now = time.time()
    cache_key = f"{symbol}_coingecko"
    # Use cache if recent
    if cache_key in COINGECKO_CACHE:
        cached = COINGECKO_CACHE[cache_key]
        if now - cached['timestamp'] < COINGECKO_CACHE_TTL:
            logging.info(f"Using cached CoinGecko price for {symbol}")
            return cached['data']
    backoff = COINGECKO_BACKOFF
    while True:
        try:
            ... # (existing request code)
            result = {...}
            COINGECKO_CACHE[cache_key] = {'timestamp': now, 'data': result}
            return result
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logging.warning(f"CoinGecko rate limited. Backing off {backoff}s...")
                time.sleep(backoff)
                backoff = min(backoff * 2, COINGECKO_MAX_BACKOFF)
                continue
            raise
        except Exception as e:
            logging.error(f"Failed to fetch price from CoinGecko for {symbol}: {e}")
            return None
```

## Next Steps
- Implement this logic in overseer_bot.py for robust CoinGecko usage.
- Consider persistent caching (e.g., Redis) for production.
