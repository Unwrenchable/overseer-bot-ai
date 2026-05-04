# Copilot Instructions

## Build, test, and run commands

- Install local dependencies: `pip install -r requirements.txt`
- Render-style dependency install: `pip install -r requirements-lock.txt`
- Generate a local `.env`: `python setup_env.py`
- Run in development: `python overseer_bot.py`
- Run in production style: `gunicorn --config gunicorn_config.py overseer_bot:app`
- Run the full test suite: `python test_twitter_bot.py`
- Run a single test: `python -m unittest test_twitter_bot.TestTweetDedup.test_mark_and_detect_duplicate`

## High-level architecture

- This service supports both the Atomic Fizz Caps product and its Twitter/X presence. The bot promotes the Atomic Fizz Caps game at `https://www.atomicfizzcaps.xyz`, posts themed social content as OVERSEER-77, and surfaces game- and market-related activity through the monitoring dashboard and webhook/API layer.
- This is a flat Python application centered on `overseer_bot.py`. That file owns the Flask app, the Basic Auth-protected dashboard and JSON API, APScheduler jobs, Twitter/X posting and media upload, LLM tweet generation, token price monitoring, wallet endpoints, token safety checks, and the Fallout-themed content pools.
- Startup is intentionally split. `gunicorn_config.py` must keep `workers = 1`, and its `post_worker_init()` hook calls `initialize_bot()`. Local development also calls `initialize_bot()` from the `if __name__ == "__main__"` path before starting the Flask dev server.
- `initialize_bot()` is the lifecycle hub. It registers all scheduled jobs, starts the delayed activation tweet thread, starts `api_client.start_polling()`, and schedules `warm_wiki_lore_cache()` so tweet generation can inject Fallout wiki snippets without blocking the hot path.
- `api_client.py` is the external-service bridge. It keeps thread-safe in-memory alert and health stores, polls the configured remote Overseer service on a daemon thread, and feeds `/api/alerts` and `/api/health`, which merge external data with local activity state from `overseer_bot.py`.
- The monitoring UI is embedded directly in `monitoring_dashboard()` with `render_template_string` plus inline JavaScript that calls the JSON endpoints. There is no `templates/` directory or separate frontend build.
- Runtime state is mostly process-local and partially file-backed. Recent activities, alert history, tweet dedup hashes, cooldowns, token safety cache, and lore cache live in memory; `price_cache.json` and `processed_mentions.json` are the durable local caches the app reads and writes directly.

## Key conventions

- Preserve the single-process assumption. Do not raise Gunicorn worker count or add behavior that depends on multi-worker coordination; duplicated workers would duplicate schedulers, background polling, and in-memory tweet/state tracking.
- Follow the repo's feature-gating pattern. Code checks module-level flags like `TWITTER_ENABLED`, `TWITTER_READ_ENABLED`, `LLM_ENABLED`, and `WALLET_ENABLED`, and posting/read paths also re-check concrete clients (`client`, `api_v1`) for defense in depth.
- Keep mutable shared state behind the existing locks and bounded caches. Important examples are `RECENT_ACTIVITIES_LOCK`, `RECENT_TWEET_HASHES_LOCK`, `ALERT_HISTORY_LOCK`, `HEALTH_STATUS_LOCK`, and the size-limited caches in both `overseer_bot.py` and `api_client.py`.
- Treat code as the source of truth when docs disagree. The current POST helper endpoints are `/api/wallet/check-token` and `/api/price/check`, even though parts of the README still show the older paths.
- Keep UI changes in `overseer_bot.py` unless you are deliberately introducing a new structure. Dashboard markup, CSS, and browser-side fetch logic all live inside `monitoring_dashboard()`.
- Keep auth and exposure patterns consistent: `/health` is public, `/api/*` and `/` use HTTP Basic Auth, `/overseer-event` uses the webhook API key path, and `/api/*` plus `/health` intentionally return permissive CORS headers.
- Tests follow the established lightweight style in `test_twitter_bot.py`: `unittest.TestCase` plus plain `assert`, with heavy optional modules stubbed before importing `overseer_bot`.
- This repo stays intentionally flat. Prefer extending the existing root-level modules and current patterns before introducing new packages, template folders, or extra framework layers.

## MCP servers

- Prefer a Playwright MCP server when validating the monitoring dashboard, Basic Auth flow, inline JavaScript behavior, and end-to-end calls from the browser UI to `/api/*` endpoints.
- Prefer a GitHub MCP server when investigating Actions runs, PR discussions, deployment history, or repo metadata tied to this bot's production behavior.
