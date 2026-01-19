import os
import time
import logging
import random
from datetime import datetime
import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import tweepy
from flask import Flask, request

# ------------------------------------------------------------
# CONFIG & LOGGING
# ------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - VAULT-TEC OVERSEER LOG - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("overseer_ai.log"), logging.StreamHandler()]
)

GAME_LINK = "https://www.atomicfizzcaps.xyz"

# ------------------------------------------------------------
# TWITTER AUTH
# ------------------------------------------------------------
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')

client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True
)

auth_v1 = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
)
api_v1 = tweepy.API(auth_v1, wait_on_rate_limit=True)

# ------------------------------------------------------------
# FLASK APP FOR WALLET EVENTS
# ------------------------------------------------------------
app = Flask(__name__)

@app.post("/overseer-event")
def overseer_event():
    event = request.json
    overseer_event_bridge(event)
    return {"ok": True}

# ------------------------------------------------------------
# FILES & MEDIA
# ------------------------------------------------------------
PROCESSED_MENTIONS_FILE = "processed_mentions.json"
MEDIA_FOLDER = "media/"

def load_json_set(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return set(json.load(f))
    return set()

def save_json_set(data, filename):
    with open(filename, 'w') as f:
        json.dump(list(data), f)

def get_random_media_id():
    media_files = [
        f for f in os.listdir(MEDIA_FOLDER)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4'))
    ]
    if not media_files:
        return None
    media_path = os.path.join(MEDIA_FOLDER, random.choice(media_files))
    try:
        media = api_v1.media_upload(media_path)
        return media.media_id_string
    except Exception as e:
        logging.error(f"Media upload failed: {e}")
        return None

# ------------------------------------------------------------
# LORE DATA
# ------------------------------------------------------------
TIME_PHRASES = {
    'morning': 'Dawn radiation nominal, dwellers stirring',
    'afternoon': 'Midday heat blistering the sands',
    'evening': 'Twilight fallout cloaking the ruins',
    'night': 'Nocturnal horrors prowling the wastes',
    'midnight': 'Dead of night—perfect for silent claims'
}

EVENTS = [
    'Super Mutant patrol inbound', 'CAPS vault breach detected', 'Raider skirmish escalating',
    'Hotspot radiation spike', 'Nuka-Cola cache revealed', 'Deathclaw nest disturbed',
    'Brotherhood recon sighted', 'Enclave signal intercepted', 'Ghoul uprising brewing',
    'Mojave anomaly expanding'
]

LORES = [
    'War never changes.', 'The wasteland forges survivors.', 'Vault-Tec: Preparing for tomorrow.',
    'In the ruins, opportunity rises.', 'Glory to the reclaimers of the Mojave.',
    'History repeats in irradiated echoes.', 'The bold claim, the weak perish.',
    'Nuka-World dreams in Atomic Fizz reality.', 'From Vault 21 to your Pip-Boy.',
    'Legends are minted on-chain.'
]

THREATS = [
    'Fail and face expulsion protocols.', 'Claim or be claimed by the void.',
    'Radiation awaits the hesitant.', 'Super Mutants envy your indecision.',
    'The Overseer does not tolerate delay.', 'Wasteland mercy is a myth.',
    'Prove your worth—or fade into static.', 'Initiates: Evolve or evaporate.'
]

# ------------------------------------------------------------
# LLM SUPPORT
# ------------------------------------------------------------
def generate_llm_response(prompt, max_tokens=100):
    if not HUGGING_FACE_TOKEN:
        return None
    try:
        url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}
        data = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()[0]['generated_text'].strip()
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
    return None

# ------------------------------------------------------------
# EVENT BRIDGE (FROM WALLET)
# ------------------------------------------------------------
def overseer_event_bridge(event: dict):
    try:
        etype = event.get("type")

        if etype == "perk":
            handle_perk_event(event)
        elif etype == "quest":
            handle_quest_event(event)
        elif etype == "swap":
            handle_swap_event(event)
        elif etype == "moonpay":
            handle_moonpay_event(event)
        elif etype == "nft":
            handle_nft_event(event)

        logging.info(f"Overseer processed event: {event}")

    except Exception as e:
        logging.error(f"Overseer event bridge failed: {e}")

def post_overseer_update(text):
    try:
        client.create_tweet(text=f"Overseer update: {text} {GAME_LINK}")
        logging.info(f"Posted Overseer update: {text}")
    except Exception as e:
        logging.error(f"Failed to post Overseer update: {e}")

def handle_perk_event(event):
    perk = event.get("perk")
    post_overseer_update(f"Perk unlocked: {perk}. The wasteland shifts.")

def handle_quest_event(event):
    post_overseer_update(f"Quest triggered: {event.get('code')}. {event.get('message')}")

def handle_swap_event(event):
    post_overseer_update(
        f"Swap executed: {event.get('amount')} {event.get('from')} → {event.get('to')}."
    )

def handle_moonpay_event(event):
    post_overseer_update(
        f"Vault funding detected: {event.get('amount')} USDC purchased via MoonPay."
    )

def handle_nft_event(event):
    post_overseer_update(
        f"NFT {event.get('action')}: {event.get('name')}. Overseer acknowledges."
    )

# ------------------------------------------------------------
# BROADCAST + REPLY SYSTEM
# ------------------------------------------------------------
def get_time_phrase():
    hour = datetime.now().hour
    if 0 <= hour < 5: return TIME_PHRASES['midnight']
    if 5 <= hour < 12: return TIME_PHRASES['morning']
    if 12 <= hour < 17: return TIME_PHRASES['afternoon']
    if 17 <= hour < 21: return TIME_PHRASES['evening']
    return TIME_PHRASES['night']

def overseer_broadcast():
    message = random.choice([
        f"Static crackles... {get_time_phrase()}. {random.choice(EVENTS)} Dwellers, heed the call: {GAME_LINK} {random.choice(THREATS)}",
        f"Overseer directive - {datetime.now().strftime('%B %d, %Y')}: {random.choice(EVENTS)} {random.choice(LORES)} Mobilize: {GAME_LINK}",
        f"Alert level red: {random.choice(EVENTS)} First to claim wins: {GAME_LINK} {random.choice(THREATS)}"
    ])
    media_ids = [get_random_media_id()] if random.random() > 0.4 else None
    try:
        client.create_tweet(text=message, media_ids=media_ids)
    except Exception as e:
        logging.error(f"Broadcast failed: {e}")

def overseer_respond():
    processed = load_json_set(PROCESSED_MENTIONS_FILE)
    try:
        mentions = client.get_users_mentions(
            client.get_me().data.id,
            max_results=50,
            tweet_fields=["author_id", "text"]
        )
        for mention in mentions.data or []:
            if mention.id in processed:
                continue

            user_id = mention.author_id
            user = client.get_user(id=user_id).data.username
            user_message = mention.text.replace(
                f"@{client.get_me().data.username}", ""
            ).strip()

            response = f"@{user} {random.choice(LORES)} {GAME_LINK}"

            try:
                client.create_tweet(
                    text=response,
                    in_reply_to_tweet_id=mention.id
                )
                client.like(mention.id)
                processed.add(mention.id)
            except Exception as e:
                logging.error(f"Reply failed: {e}")

        save_json_set(processed, PROCESSED_MENTIONS_FILE)

    except Exception as e:
        logging.error(f"Mentions fetch failed: {e}")

def overseer_retweet_hunt():
    query = "(Fallout OR Solana OR NFT OR wasteland OR Mojave OR \"Atomic Fizz\") filter:media min_faves:5 -is:retweet"
    try:
        tweets = client.search_recent_tweets(query=query, max_results=20)
        for tweet in tweets.data or []:
            if random.random() > 0.75:
                try:
                    client.retweet(tweet.id)
                except Exception:
                    pass
    except Exception as e:
        logging.error(f"Search failed: {e}")

def overseer_diagnostic():
    diag = f"Static crackles... Overseer diagnostic: ONLINE. {random.choice(LORES)} {GAME_LINK} ☢️🔥"
    try:
        client.create_tweet(text=diag)
    except Exception as e:
        logging.error(f"Diagnostic failed: {e}")

# ------------------------------------------------------------
# SCHEDULER
# ------------------------------------------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(overseer_broadcast, 'interval', minutes=random.randint(120, 240))
scheduler.add_job(overseer_respond, 'interval', minutes=random.randint(15, 30))
scheduler.add_job(overseer_retweet_hunt, 'interval', hours=1)
scheduler.add_job(overseer_diagnostic, 'cron', hour=8)
scheduler.start()

# ------------------------------------------------------------
# ACTIVATION
# ------------------------------------------------------------
logging.info("VAULT-TEC OVERSEER AI ONLINE ☢️🔥")
try:
    activation_msg = (
        f"Static crackles... Overseer fully awakened. "
        f"Atomic Fizz wasteland pulses with life. {GAME_LINK} 🟢🔥 {random.choice(LORES)}"
    )
    client.create_tweet(text=activation_msg)
except Exception:
    pass

# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------
if __name__ == "__main__":
    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Overseer powering down. The wasteland endures.")
