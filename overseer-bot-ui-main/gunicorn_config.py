"""
Gunicorn configuration for Overseer Bot.

This configuration ensures that the bot's scheduler and background tasks
start properly when run with gunicorn.

CRITICAL: This application MUST use workers=1. The app contains schedulers,
background tasks, and state that should not be duplicated across workers.
Multiple workers would cause duplicate tweets, multiple schedulers, and
race conditions. Do not increase the worker count.
"""
import logging
import os

# Bind to the PORT environment variable, or default to 5000
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# Use only 1 worker because the app has schedulers and background tasks
# Multiple workers would duplicate these tasks
workers = 1

# Worker class - use sync for compatibility with threading
worker_class = "sync"

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"

# Timeout for worker silence (seconds)
timeout = 120


def on_starting(server):
    """Called just before the master process is initialized."""
    logging.info("Gunicorn server is starting")


def when_ready(server):
    """Called just after the server is started."""
    logging.info("Gunicorn server is ready. Receiving requests.")


def post_worker_init(worker):
    """
    Called just after a worker has been initialized.
    This is where we initialize the bot's scheduler and background tasks.
    """
    logging.info(f"Worker {worker.pid} initialized, starting bot services")
    
    try:
        # Import here to avoid issues with module loading order
        from overseer_bot import initialize_bot
        
        # Initialize the bot (scheduler, API polling, activation tweet)
        initialize_bot()
        
        logging.info(f"Worker {worker.pid} bot services started successfully")
    except Exception as e:
        # Log the error but don't crash the worker
        # The Flask app can still serve the UI even if bot initialization fails
        logging.error(f"Worker {worker.pid} bot initialization failed: {e}", exc_info=True)
        logging.warning(
            "Flask UI will be available, but bot features will be limited. "
            "Scheduler jobs, API polling, Twitter bot, and activation tweets will not function."
        )
