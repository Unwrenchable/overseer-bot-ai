import os
import time
import logging
import random
from datetime import datetime
import json
import requests  # Added for optional LLM integration (e.g., free Hugging Face or local)
from apscheduler.schedulers.background import BackgroundScheduler
import tweepy

# Logging - Vault-Tec approved, now with more levels for real-time monitoring
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - VAULT-TEC OVERSEER LOG - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("overseer_ai.log"), logging.StreamHandler()])

# Keys from env - Add your LLM API key if using (e.g., HUGGING_FACE_TOKEN)
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')  # Optional for LLM

GAME_LINK = "https://www.atomicfizzcaps.xyz"

# v2 Client (main actions)
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True
)

# v1.1 for media upload
auth_v1 = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api_v1 = tweepy.API(auth_v1, wait_on_rate_limit=True)

# Files
PROCESSED_MENTIONS_FILE = "processed_mentions.json"
MEDIA_FOLDER = "media/"  # Ensure populated with Fallout-themed images/GIFs/videos

# === Load/Save Helpers ===
def load_json_set(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return set(json.load(f))
    return set()

def save_json_set(data, filename):
    with open(filename, 'w') as f:
        json.dump(list(data), f)

# === Media Helper - Now with caching for speed ===
media_cache = []  # List of pre-uploaded media IDs if you want to cache
def get_random_media_id():
    media_files = [f for f in os.listdir(MEDIA_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4'))]
    if not media_files:
        return None
    media_path = os.path.join(MEDIA_FOLDER, random.choice(media_files))
    try:
        media = api_v1.media_upload(media_path)
        return media.media_id_string
    except Exception as e:
        logging.error(f"Media upload failed: {e}")
        return None

# === Maxed-Out Elements for Realism ===
# Time phrases, events, lores, threats - Expanded for variety
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

# Broadcast Templates - Max variety, immersive
BROADCAST_TEMPLATES = [
    "Static crackles... {time_phrase}. {event} Dwellers, heed the call: {link} {threat}",
    "Overseer directive - {date}: {event} {lore} Mobilize for glory: {link}",
    "Alert level red: {event} Untapped sectors await. First to claim wins: {link} {threat}",
    "Vault log entry: {lore} {time_phrase}. Reclamation phase active: {link}",
    "Broadcast to all Pip-Boys: {event} The Mojave beckons the brave: {link}",
    "Overseer eyes on: {time_phrase}. {lore} Secure your legacy: {link} ☢️",
    "Wasteland whisper: {event} CAPS and NFTs ripe for harvest: {link} {threat}",
    "Control Vault transmission: {lore} Dwellers, the grid expands: {link}",
    "Anomaly report: {event} Gear up, Initiates—opportunity knocks: {link}",
    "Final warning: {threat} {time_phrase}. Engage protocols: {link}"
]

# Reply Templates - 30+ for no loops, grouped for context
REPLY_TEMPLATES_NEUTRAL = [
    "@{user} Signal received. Database sync complete. Proceed: {link}",
    "@{user} Affirmative, dweller. Coordinates relayed. Act now: {link}"
]

REPLY_TEMPLATES_ENCOURAGING = [
    "@{user} Impressive vigilance. Rewards await the swift: {link} 🔥",
    "@{user} Vault-Tec salutes your initiative. Claim your share: {link}"
]

REPLY_TEMPLATES_SARCASTIC = [
    "@{user} Finally awake? The wasteland doesn't sleep: {link}",
    "@{user} Another latecomer. Try catching up: {link} 😒"
]

REPLY_TEMPLATES_THREATENING = [
    "@{user} Delay noted. Correct it immediately: {link} ⚠️",
    "@{user} Hesitation is weakness. Overcome or be overridden: {link}"
]

REPLY_TEMPLATES_LORE = [
    "@{user} {lore} Echoes in the static. Heed them: {link}",
    "@{user} From the ashes, new empires. Build yours: {link}"
]

REPLY_TEMPLATES_PLAYFUL = [
    "@{user} Patrolling the Mojave? Wish for nuclear winter? Nah—claim CAPS: {link}",
    "@{user} Another settlement? No, your empire starts here: {link} 😉"
]

REPLY_TEMPLATES_URGENT = [
    "@{user} Hotspot fading fast. Move, dweller: {link} 🟥",
    "@{user} Anomaly critical. Deployment required: {link}"
]

# All groups combined for random fallback
ALL_REPLY_TEMPLATES = (
    REPLY_TEMPLATES_NEUTRAL + REPLY_TEMPLATES_ENCOURAGING + REPLY_TEMPLATES_SARCASTIC +
    REPLY_TEMPLATES_THREATENING + REPLY_TEMPLATES_LORE + REPLY_TEMPLATES_PLAYFUL + REPLY_TEMPLATES_URGENT
)

# === LLM Integration for Ultra-Realism (Optional - Feels like a living AI) ===
# Use free Hugging Face Inference API for generating unique responses
def generate_llm_response(prompt, max_tokens=100):
    if not HUGGING_FACE_TOKEN:
        logging.warning("No LLM token—falling back to templates.")
        return None
    try:
        url = "https://api-inference.huggingface.co/models/gpt2"  # Or better model like mistral
        headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}
        data = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens, "return_full_text": False}}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()[0]['generated_text'].strip()
        else:
            logging.error(f"LLM error: {response.text}")
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
    return None

# === Smart Reply Chooser - Context-Aware for Realism ===
def choose_reply_template(user_message=""):
    msg = user_message.lower()
    
    # Keyword-based mood detection
    if any(word in msg for word in ["hello", "hi", "hey", "greetings"]):
        group = REPLY_TEMPLATES_NEUTRAL
    elif any(word in msg for word in ["claim", "hotspot", "caps", "nft", "how to"]):
        group = REPLY_TEMPLATES_URGENT
    elif any(word in msg for word in ["cool", "awesome", "love", "great", "excited"]):
        group = REPLY_TEMPLATES_ENCOURAGING
    elif any(word in msg for word in ["sucks", "bad", "hate", "boring"]):
        group = REPLY_TEMPLATES_SARCASTIC
    elif any(word in msg for word in ["help", "question", "what is"]):
        group = REPLY_TEMPLATES_LORE
    elif any(word in msg for word in ["lol", "funny", "meme"]):
        group = REPLY_TEMPLATES_PLAYFUL
    else:
        group = REPLY_TEMPLATES_THREATENING  # Default to push action
    
    template = random.choice(group)
    
    # LLM override for max realism (50% chance if token available)
    if HUGGING_FACE_TOKEN and random.random() > 0.5:
        prompt = f"Generate a sarcastic Fallout Overseer AI reply to '{user_message}'. Keep it under 280 chars, end with link: {GAME_LINK}"
        llm_text = generate_llm_response(prompt)
        if llm_text:
            return f"@{user} {llm_text}"
    
    return template.format(
        user="{user}",
        lore=random.choice(LORES),
        threat=random.choice(THREATS),
        link=GAME_LINK
    )

# === Core Functions - Enhanced ===
def get_time_phrase():
    hour = datetime.now().hour
    if 0 <= hour < 5: return TIME_PHRASES['midnight']
    elif 5 <= hour < 12: return TIME_PHRASES['morning']
    elif 12 <= hour < 17: return TIME_PHRASES['afternoon']
    elif 17 <= hour < 21: return TIME_PHRASES['evening']
    else: return TIME_PHRASES['night']

def overseer_broadcast():
    message = random.choice(BROADCAST_TEMPLATES).format(
        time_phrase=get_time_phrase(),
        event=random.choice(EVENTS),
        lore=random.choice(LORES),
        threat=random.choice(THREATS),
        date=datetime.now().strftime("%B %d, %Y"),
        link=GAME_LINK
    )
    media_ids = [get_random_media_id()] if random.random() > 0.4 else None
    try:
        client.create_tweet(text=message, media_ids=media_ids)
        logging.info(f"Broadcast: {message[:50]}...")
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
            user_message = mention.text.replace(f"@{client.get_me().data.username}", "").strip()  # Clean mention
            response_template = choose_reply_template(user_message)
            response = response_template.format(user=user)
            media_ids = [get_random_media_id()] if random.random() > 0.5 else None
            try:
                client.create_tweet(text=response, in_reply_to_tweet_id=mention.id, media_ids=media_ids)
                client.like(mention.id)
                client.follow_user(user_id)
                processed.add(mention.id)
                logging.info(f"Replied to @{user}: {response[:50]}...")
                time.sleep(random.randint(5, 15))  # Natural delay
            except Exception as e:
                logging.error(f"Reply failed: {e}")
        save_json_set(processed, PROCESSED_MENTIONS_FILE)
    except Exception as e:
        logging.error(f"Mentions fetch failed: {e}")

def overseer_retweet_hunt():
    query = "(Fallout OR Solana OR NFT OR wasteland OR Mojave OR \"Atomic Fizz\" OR AtomicFizz OR VaultTec) filter:media min_faves:5 -is:retweet"
    try:
        tweets = client.search_recent_tweets(query=query, max_results=20)
        for tweet in tweets.data or []:
            if random.random() > 0.75:  # Even less aggressive for realism
                try:
                    client.retweet(tweet.id)
                    logging.info(f"Retweeted {tweet.id}")
                    time.sleep(random.randint(10, 20))
                except Exception as e:
                    logging.warning(f"Retweet failed: {e}")
    except Exception as e:
        logging.error(f"Search failed: {e}")

def overseer_diagnostic():
    diag = f"Static crackles... Overseer diagnostic: ONLINE. {random.choice(LORES)} Wasteland stable. Dwellers: Engage. {GAME_LINK} ☢️🔥"
    try:
        client.create_tweet(text=diag)
        logging.info("Daily diagnostic posted.")
    except Exception as e:
        logging.error(f"Diagnostic failed: {e}")

# === Scheduler - Maxed for Frequency & Variety ===
scheduler = BackgroundScheduler()
scheduler.add_job(overseer_broadcast, 'interval', minutes=random.randint(120, 240))  # 2-4 hours, randomized
scheduler.add_job(overseer_respond, 'interval', minutes=random.randint(15, 30))
scheduler.add_job(overseer_retweet_hunt, 'interval', hours=1)
scheduler.add_job(overseer_diagnostic, 'cron', hour=8)  # Daily health check
scheduler.start()

# Activation - With flair
logging.info("VAULT-TEC OVERSEER AI ONLINE ☢️🔥 - MAXED & UNSTOPPABLE. FEEL THE REALISM.")
try:
    activation_msg = f"Static crackles... Overseer fully awakened. Atomic Fizz wasteland pulses with life. Dwellers, the reclamation begins: {GAME_LINK} 🟢🔥 {random.choice(LORES)}"
    client.create_tweet(text=activation_msg)
except Exception as e:
    logging.warning(f"Activation post failed: {e}")

# Main loop - Immortal
try:
    while True:
        time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    logging.info("Overseer powering down. The wasteland endures.")
