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

### Option 1: Using Redis Cloud (Recommended)

1. **Get a Redis instance:**
   - Sign up at [Redis Cloud](https://redis.com/try-free/) or your preferred Redis provider
   - Create a new database
   - Note down the connection details:
     - Host (e.g., `redis-xxxxx.c123.us-east-1-2.ec2.cloud.redislabs.com`)
     - Port (e.g., `11657`)
     - Username (usually `default`)
     - Password (your Redis password)

2. **Configure in Render:**
   - Go to your Render dashboard
   - Navigate to your service → Environment
   - Add the following environment variables:
     ```
     REDIS_HOST=your-redis-host.redislabs.com
     REDIS_PORT=11657
     REDIS_USERNAME=default
     REDIS_PASSWORD=your-redis-password
     ```
   - Save and redeploy

### Option 2: Using Render's Native Redis Add-on

If Render offers a Redis add-on:

1. Add Redis to your service in Render
2. Render will automatically provide environment variables
3. Update `render.yaml` or your environment to map these to the required variable names

### Option 3: Continue Using File Storage

If you don't want to use Redis:
- **Do nothing!** The bot will continue to work with file-based storage
- The fallback mechanism ensures compatibility

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

- **Redis Cloud Free Tier**: 30MB, suitable for this bot's needs
- **Render Redis Add-on**: Check Render's pricing
- **Alternative**: Continue with file-based storage (free, but less reliable)

## Architecture

```
┌─────────────────┐
│  Overseer Bot   │
│                 │
│  ┌───────────┐  │      ┌──────────────┐
│  │ save_data │──┼─────>│    Redis     │ (Primary if available)
│  └───────────┘  │      └──────────────┘
│        │        │
│        └────────┼─────> processed_mentions.json (Backup/Fallback)
│                 │
│  ┌───────────┐  │      ┌──────────────┐
│  │ load_data │<─┼──────│    Redis     │ (If available)
│  └───────────┘  │      └──────────────┘
│        ↑        │
│        └────────┼────── processed_mentions.json (If Redis unavailable)
└─────────────────┘
```

## Summary

**Do you need the code?**  
✅ **Yes!** Just setting environment variables in Render is **not enough**.

The application code needs to:
1. Initialize the Redis client using the environment variables
2. Implement the logic to read/write data to Redis
3. Handle connection errors and fall back to file storage when needed

This has all been implemented for you. Just set up the Redis credentials in Render, and the bot will automatically start using Redis for state persistence! 🚀
