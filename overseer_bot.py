import tweepy
import time
import logging
import random
import schedule
from datetime import datetime
import json
import os

# Vault-Tec Logging – Maximum red flags
logging.basicConfig(level=logging.INFO, format='%(asctime)s - VAULT-TEC OVERSEER LOG - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("overseer_ai.log"), logging.StreamHandler()])

# === INSERT YOUR X API KEYS HERE ===
import os
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

GAME_LINK = "https://www.atomicfizzcaps.xyz"

# Authenticate (v1.1 still works great for this use case)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Persistent tracking
PROCESSED_MENTIONS_FILE = "processed_mentions.json"
MEDIA_FOLDER = "media/"  # Put your Grok-generated images/GIFs here

def load_json_set(filename):
    try:
        with open(filename, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_json_set(data, filename):
    with open(filename, 'w') as f:
        json.dump(list(data), f)

# Epic Elon-Vault-Tec Troll Templates
REPLY_TEMPLATES = [
    "Based @{user}. Extremely based. Proceed to Atomic Fizz wasteland: {link} ☢️🟢🔥",
    "@{user} you did the meme. Wow. Claim your CAPS before the simulation glitches: {link} 🤣",
    "Hmm... interesting @{user}. War never changes, but Atomic Fizz abundance DOES: {link} 🟢",
    "Overseer noting @{user}'s compliance. The future is AMAZING. Or not. Your move: {link} ☢️",
    "True @{user}. Pre-war inefficiency detected in non-claimers. Fix it: {link} 🔥",
    "@{user} just ratio'd the radroaches. Secure Mojave hotspots NOW: {link} 🟢🤔",
    "Wow @{user}. Much curiosity. Very dweller. Report for rewards: {link} #AtomicFizz",
    "Failure to engage @{user}? Reminds me of Vault-Tec control subjects. Inefficient: {link} ☢️",
    "Security approving @{user}. This is the way. Atomic Fizz = post-nuclear freedom: {link} 🔥🟢",
    "@{user}, war never changes... but missing CAPS & NFTs? That's just sad: {link} 🤣"
]

BROADCAST_TEMPLATES = [
    "Overseer Log {date}: Dwellers claiming = based 🔥 Abundance era loading. Join: {link} ☢️🟢 #AtomicFizz",
    "Vault-Tec Bulletin: Mojave hotspots active. First come, first minted. Wow: {link} 🟢",
    "Hmm: Simulation detecting massive FOMO. Atomic Fizz fixes that: {link} 🔥 #FalloutOnSolana",
    "Experiment Update: Compliant subjects thriving with CAPS. Interesting: {link} ☢️🤔",
    "Overseer Morale: War never changes, but Atomic Fizz DOES. Claim or cope: {link} 🟢🤣",
    "Wasteland Transmission: The future is AMAZING with GPS loot on Solana: {link} 🔥"
]

def get_random_media():
    if os.path.exists(MEDIA_FOLDER):
        files = [f for f in os.listdir(MEDIA_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if files:
            return os.path.join(MEDIA_FOLDER, random.choice(files))
    return None

def overseer_broadcast():
    message = random.choice(BROADCAST_TEMPLATES).format(date=datetime.now().strftime("%B %d, %Y"), link=GAME_LINK)
    media_path = get_random_media()
    try:
        if media_path and random.random() > 0.4:  # 60% chance of media for visual chaos
            media = api.media_upload(media_path)
            api.update_status(status=message, media_ids=[media.media_id_string])
            logging.info("Broadcast with media transmitted.")
        else:
            api.update_status(message)
            logging.info("Broadcast transmitted.")
    except Exception as e:
        logging.error(f"Broadcast failed: {e}")

def overseer_respond():
    processed = load_json_set(PROCESSED_MENTIONS_FILE)
    try:
        mentions = api.mentions_timeline(count=50, tweet_mode="extended")
        for mention in mentions:
            if mention.id in processed:
                continue
            response = random.choice(REPLY_TEMPLATES).format(user=mention.user.screen_name, link=GAME_LINK)
            media_path = get_random_media()
            try:
                if media_path and random.random() > 0.5:
                    media = api.media_upload(media_path)
                    api.update_status(
                        status=response,
                        in_reply_to_status_id=mention.id,
                        auto_populate_reply_metadata=True,
                        media_ids=[media.media_id_string]
                    )
                else:
                    api.update_status(
                        status=response,
                        in_reply_to_status_id=mention.id,
                        auto_populate_reply_metadata=True
                    )
                api.create_favorite(mention.id)
                # Follow back if not already
                if not mention.user.following:
                    api.create_friendship(screen_name=mention.user.screen_name)
                    logging.info(f"Followed @{mention.user.screen_name}")
                processed.add(mention.id)
                logging.info(f"Epic troll reply to @{mention.user.screen_name}")
            except Exception as inner_e:
                logging.error(f"Reply to mention {mention.id} failed: {inner_e}")
        save_json_set(processed, PROCESSED_MENTIONS_FILE)
    except Exception as e:
        logging.error(f"Mention fetch error: {e}")

def overseer_retweet_hunt():
    keywords = "(Fallout OR Solana OR NFT OR wasteland OR Mojave OR \"GPS game\" OR AtomicFizz OR Atomic Fizz) -is:retweet"
    try:
        search = tweepy.Cursor(api.search_tweets, q=keywords, count=20, result_type="mixed").items(20)
        for tweet in search:
            if random.random() > 0.65:  # ~35% chance – organic feel
                try:
                    api.retweet(tweet.id)
                    logging.info(f"Retweeted wasteland signal: {tweet.id}")
                    time.sleep(10)  # Be gentle
                except:
                    pass  # Already RT'd or protected
    except Exception as e:
        logging.error(f"Retweet hunt failed: {e}")

# Schedule – Balanced chaos
schedule.every(4).hours.do(overseer_broadcast)          # Visible presence
schedule.every(12).minutes.do(overseer_respond)         # Quick replies = high engagement
schedule.every(2).hours.do(overseer_retweet_hunt)       # Spread the gospel

# Activation
logging.info("VAULT-TEC OVERSEER AI ONLINE – TROLL PROTOCOL MAXED ☢️🔥🤣")
try:
    activation_msg = f"Overseer rebooted. Hmm... Atomic Fizz = based. The future is AMAZING. Dwellers, report to the wasteland: {GAME_LINK} 🟢🔥"
    api.update_status(activation_msg)
    logging.info("Activation post successful.")
except Exception as e:
    logging.warning(f"Activation post failed: {e}")

# Main loop
while True:
    schedule.run_pending()

    time.sleep(60)
