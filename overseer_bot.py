import tweepy
import time
import logging
import random
import schedule
from datetime import datetime
import json
import os

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - VAULT-TEC OVERSEER LOG - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("overseer_ai.log"), logging.StreamHandler()])

# Keys from env
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')  # Optional but recommended for searches

GAME_LINK = "https://www.atomicfizzcaps.xyz"

# v2 Client for most actions (post, reply, like, follow, search)
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
    bearer_token=BEARER_TOKEN,  # Add if you have it
    wait_on_rate_limit=True
)

# v1.1 API only for media upload (still works in 2025)
auth_v1 = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api_v1 = tweepy.API(auth_v1)

# Folders/files same
PROCESSED_MENTIONS_FILE = "processed_mentions.json"
MEDIA_FOLDER = "media/"

# Load/save same functions...

# Templates same (epic as hell)

def get_random_media_id():
    media_path = get_random_media()  # Your existing function to pick file
    if media_path:
        try:
            media = api_v1.media_upload(media_path)
            return media.media_id_string
        except Exception as e:
            logging.error(f"Media upload failed: {e}")
    return None

def overseer_broadcast():
    message = random.choice(BROADCAST_TEMPLATES).format(date=datetime.now().strftime("%B %d, %Y"), link=GAME_LINK)
    media_ids = [get_random_media_id()] if random.random() > 0.4 else None
    try:
        client.create_tweet(text=message, media_ids=media_ids)
        logging.info("Broadcast transmitted.")
    except Exception as e:
        logging.error(f"Broadcast failed: {e}")

def overseer_respond():
    processed = load_json_set(PROCESSED_MENTIONS_FILE)
    try:
        # Get recent mentions via v2
        mentions = client.get_users_mentions(
            client.get_me().data.id,
            max_results=50,
            tweet_fields=["author_id"]
        )
        for mention in mentions.data:
            if mention.id in processed:
                continue
            user = client.get_user(id=mention.author_id).data.username
            response = random.choice(REPLY_TEMPLATES).format(user=user, link=GAME_LINK)
            media_ids = [get_random_media_id()] if random.random() > 0.5 else None
            try:
                client.create_tweet(text=response, in_reply_to_tweet_id=mention.id, media_ids=media_ids)
                client.like(mention.id)
                # Follow back
                client.follow_user(mention.author_id)
                processed.add(mention.id)
                logging.info(f"Replied to @{user}")
            except Exception as e:
                logging.error(f"Reply failed: {e}")
        save_json_set(processed, PROCESSED_MENTIONS_FILE)
    except Exception as e:
        logging.error(f"Mentions fetch failed: {e}")

def overseer_retweet_hunt():
    query = "(Fallout OR Solana OR NFT OR wasteland OR Mojave OR \"GPS game\" OR AtomicFizz OR \"Atomic Fizz\") -is:retweet"
    try:
        tweets = client.search_recent_tweets(query=query, max_results=20)
        for tweet in tweets.data or []:
            if random.random() > 0.65:
                try:
                    client.retweet(tweet.id)
                    logging.info(f"Retweeted {tweet.id}")
                    time.sleep(10)
                except:
                    pass
    except Exception as e:
        logging.error(f"Search failed: {e}")

# Schedule same intervals...

# Activation
logging.info("VAULT-TEC OVERSEER AI ONLINE ☢️🔥")
try:
    activation_msg = f"Static crackles... Overseer rebooted. Atomic Fizz wasteland active. Report, dwellers: {GAME_LINK} 🟢🔥"
    client.create_tweet(text=activation_msg)
except Exception as e:
    logging.warning(f"Activation failed: {e}")

# Main loop same
while True:
    schedule.run_pending()
    time.sleep(60)