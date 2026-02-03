# Redis Integration Guide

## Overview

The Overseer Bot now supports Redis for persistent state management. This is particularly useful when deploying to cloud platforms like Render, where local file storage can be unreliable across restarts and doesn't work well with multiple instances.

## What Changed

### Previous Behavior
- Used local JSON file (`processed_mentions.json`) to track which mentions have been processed
- File could be lost on redeployments
- Doesn't work well with multiple instances

### Current Behavior
- **Automatically uses Redis when available** (configured via environment variables)
- **Gracefully falls back to file-based storage** if Redis is not configured or unavailable
- **Dual-write strategy**: Always writes to both Redis (if available) and local file as backup

## Setting Up Redis

### Option 1: Use Existing Redis (e.g., from atomicfizzcaps.xyz)

**Can I share my game's Redis instance with this bot?**

✅ **Yes, you can!** The bot uses namespaced keys (`overseer:*`) to prevent conflicts with your game's data.

**Important considerations:**
- ✅ **Safe to share** - Different key prefixes prevent data conflicts
- ⚠️ **No cross-bot enhancement** - The bots won't share data or communicate
- ⚠️ **Capacity** - Redis free tier (30MB) shared between all apps
- ⚠️ **Performance** - Multiple apps use the same Redis instance
- ⚠️ **Shared fate** - If Redis fails, both systems are affected

**To use your existing Redis from atomicfizzcaps.xyz:**

1. **Use the same Redis credentials in Render:**
   - Go to your Render dashboard for the Overseer Bot
   - Navigate to your service → Environment
   - Add the following environment variables with YOUR game's Redis credentials:
     ```
     REDIS_HOST=redis-11657.c322.us-east-1-2.ec2.cloud.redislabs.com
     REDIS_PORT=11657
     REDIS_USERNAME=default
     REDIS_PASSWORD=your-redis-password-from-game
     ```
   - Save and redeploy

2. **Verify key isolation:**
   - Overseer Bot uses keys like: `overseer:processed_mentions.json`
   - Your game likely uses different key patterns
   - They won't interfere with each other

### Option 2: Create a Separate Redis Instance (Recommended for Production)

For better isolation and scalability:

1. **Get a new Redis instance:**
   - Sign up at [Redis Cloud](https://redis.com/try-free/) or your preferred Redis provider
   - Create a new database specifically for the Overseer Bot
   - Note down the connection details

2. **Configure in Render:**
   - Use the new Redis credentials instead
   - This keeps your game and bot completely independent

### Option 3: Using Render's Native Redis Add-on

If Render offers a Redis add-on:

1. Add Redis to your service in Render
2. Render will automatically provide environment variables
3. Update `render.yaml` or your environment to map these to the required variable names

### Option 4: Continue Using File Storage

If you don't want to use Redis:
- **Do nothing!** The bot will continue to work with file-based storage
- The fallback mechanism ensures compatibility

## Will Sharing Redis "Enhance" Your Other Bot?

**Short answer: No, they won't enhance each other.**

Here's why:
- **Independent applications** - Each bot uses its own key namespace
  - Overseer Bot: `overseer:*` keys
  - Your game: (whatever keys it uses)
- **No data sharing** - They don't communicate or share state
- **Separate purposes** - The game and Twitter bot are independent systems

**What you DO get by sharing Redis:**
- ✅ Cost savings (one Redis instance for multiple apps)
- ✅ Simplified infrastructure management
- ⚠️ But NO functional integration between the apps

**If you want bots to communicate:**
You would need to:
1. Design a shared data structure/protocol
2. Use common key names both bots can access
3. Implement pub/sub messaging between them
4. Add coordination logic to both applications

This is NOT currently implemented.

## How It Works

### Automatic Detection
```python
# The bot automatically detects Redis configuration on startup
if REDIS_HOST and REDIS_PASSWORD:
    # Attempts to connect to Redis
    # Falls back to file storage if connection fails
```

### State Management
All state operations use the same functions:
- `load_json_set(filename)` - Loads from Redis if available, falls back to file
- `save_json_set(data, filename)` - Saves to Redis if available, always saves to file as backup

### Benefits of Using Redis

1. **Persistence across deployments** - State survives container restarts
2. **Shared state** - Multiple instances can share the same state
3. **Performance** - Faster than disk I/O for frequently accessed data
4. **Reliability** - Managed Redis services handle backups and replication

## Testing Your Setup

After configuring Redis in Render:

1. Deploy your bot
2. Check the logs for:
   ```
   Redis connection established successfully
   ```
   
   Or if Redis is not available:
   ```
   Redis credentials not provided. Using file-based storage.
   ```

3. The bot will log Redis operations:
   ```
   Saved 5 items to Redis key: overseer:processed_mentions.json
   ```

## Troubleshooting

### "Redis connection failed" in logs
- **Cause**: Invalid credentials or Redis server unreachable
- **Solution**: The bot will automatically fall back to file storage
- **Fix**: Double-check your Redis credentials and network connectivity

### State not persisting
- **File storage**: Normal behavior on Render (ephemeral filesystem)
- **Solution**: Set up Redis using the steps above

### Sharing Redis with your game (atomicfizzcaps.xyz)
If you're using the same Redis instance for multiple applications:

1. **Monitor capacity usage:**
   ```bash
   # Check Redis memory usage (if you have redis-cli access)
   INFO memory
   ```
   - Redis Cloud free tier: 30MB total
   - Overseer Bot typically uses: < 1MB (stores only processed mention IDs)
   - Your game: (depends on your game's data)

2. **Check for key conflicts:**
   ```bash
   # List all keys (use with caution on production)
   KEYS overseer:*  # Shows only bot keys
   ```

3. **Signs you need a separate Redis:**
   - Memory usage approaching 30MB limit
   - Performance degradation in either app
   - Frequent connection errors
   - Need for independent scaling

### Testing locally
You can test Redis integration locally:
```bash
export REDIS_HOST=your-host
export REDIS_PORT=your-port
export REDIS_USERNAME=your-username
export REDIS_PASSWORD=your-password
python overseer_bot.py
```

## Security Note

⚠️ **Never commit Redis credentials to your repository!**
- Always use environment variables
- Keep credentials in Render's environment settings
- The `render.yaml` file only declares variable names, not values

## Cost Considerations

### Sharing Redis with Your Game
- **Redis Cloud Free Tier**: 30MB total (shared between all apps using it)
- **Overseer Bot usage**: Typically < 1MB (only stores processed mention IDs)
- **Your game**: May use more depending on game state/data
- **Combined**: Should fit in free tier unless game uses significant storage

### When to Get a Separate Redis
Consider a separate Redis instance when:
- Combined usage approaches 30MB
- Need independent scaling or performance
- Want isolated failure domains
- Production environment requires strict separation

### Cost Breakdown
- **Shared Redis**: $0/month (if within free tier)
- **Separate Redis**: $0/month each (if each within free tier) or upgrade to paid plan
- **Render Redis Add-on**: Check Render's pricing
- **File storage only**: $0/month (but less reliable on cloud platforms)

## Architecture

### Single Bot with Redis
```
┌─────────────────┐
│  Overseer Bot   │
│                 │
│  ┌───────────┐  │      ┌──────────────┐
│  │ save_data │──┼─────>│    Redis     │ (Primary if available)
│  └───────────┘  │      │overseer:*    │
│        │        │      └──────────────┘
│        └────────┼─────> processed_mentions.json (Backup/Fallback)
│                 │
│  ┌───────────┐  │      ┌──────────────┐
│  │ load_data │<─┼──────│    Redis     │ (If available)
│  └───────────┘  │      │overseer:*    │
│        ↑        │      └──────────────┘
│        └────────┼────── processed_mentions.json (If Redis unavailable)
└─────────────────┘
```

### Shared Redis with Game (atomicfizzcaps.xyz)
```
┌─────────────────┐
│  Overseer Bot   │
│                 │       ┌──────────────────────┐
│  ┌───────────┐  │       │   Shared Redis       │
│  │save/load  │──┼──────>│                      │
│  └───────────┘  │       │ overseer:*           │<──┐
└─────────────────┘       │ game:*               │   │
                          │ (separate namespaces)│   │
┌─────────────────┐       └──────────────────────┘   │
│ Your Game       │                                   │
│(atomicfizzcaps) │       No conflict because         │
│                 │       different key prefixes      │
│  ┌───────────┐  │                                   │
│  │save/load  │──┼───────────────────────────────────┘
│  └───────────┘  │
└─────────────────┘

✓ Safe: Different key namespaces prevent conflicts
⚠️ Shared: Same Redis capacity and performance pool
```

## Summary

**Do you need the code?**  
✅ **Yes!** Just setting environment variables in Render is **not enough**.

The application code needs to:
1. Initialize the Redis client using the environment variables
2. Implement the logic to read/write data to Redis
3. Handle connection errors and fall back to file storage when needed

This has all been implemented for you. Just set up the Redis credentials in Render, and the bot will automatically start using Redis for state persistence! 🚀
