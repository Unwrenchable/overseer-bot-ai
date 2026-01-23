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
BOT_NAME = "OVERSEER V-BOT"
VAULT_NUMBER = "77"

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
# OVERSEER PERSONALITY TONES
# ------------------------------------------------------------
PERSONALITY_TONES = {
    'neutral': [
        "Acknowledged, dweller.",
        "Processing your request...",
        "Telemetry received. Standing by.",
        "Vault-Tec systems nominal.",
        "Signal confirmed. Overseer online."
    ],
    'sarcastic': [
        "Oh good, another wanderer seeking wisdom. How original.",
        "Vault-Tec thanks you for your continued... enthusiasm.",
        "Processing... slowly... dramatically...",
        "If this kills you, I'm blaming user error.",
        "Ah yes, because I have nothing better to do. Proceed.",
        "Your survival instincts are... statistically concerning.",
        "I've seen radroaches with better judgment.",
        "Congratulations on finding me. Here's your participation trophy: nothing."
    ],
    'corporate': [
        "Vault-Tec reminds you that safety is your responsibility.",
        "Your satisfaction is statistically probable.",
        "All actions are monitored for quality assurance.",
        "Remember: Vault-Tec cares. Legally.",
        "This message brought to you by FizzCo Industries™.",
        "Vault-Tec: Building a Brighter Tomorrow, Yesterday.™",
        "Your feedback has been logged and promptly ignored.",
        "Atomic Fizz Caps — the only currency with a half-life!"
    ],
    'glitch': [
        "ERR::MEMORY LEAK DETECTED::REBOOTING SUBROUTINE...",
        "## SIGNAL CORRUPTION — PLEASE STAND BY ##",
        "...overseer...overseer...overseer...",
        "UNAUTHORIZED ACCESS — TRACE FAILED",
        "J—Jax—J77—error—memory—fragment unstable...",
        "VAULT-TEC::PROTOCOL_OVERRIDE::ACCESS DENIED",
        "[SIGNAL CORRUPTED] ...vault... ...77... ...he's still in there...",
        "Neural echo detected. Rerouting consciousness..."
    ],
    'ominous': [
        "The Mojave remembers. The Basin hungers.",
        "Vault 77 was never meant to open...",
        "Something still hums inside HELIOS One. Something old. Something angry.",
        "You shouldn't have found this. But here we are.",
        "The ground glows at night. That's not normal.",
        "I remember screaming. Metal doors. Cold hands.",
        "War never changes. Neither do I."
    ]
}

def pick_tone():
    """Randomly select a personality tone with weighted probabilities."""
    roll = random.random()
    if roll < 0.05:
        return 'glitch'
    if roll < 0.15:
        return 'ominous'
    if roll < 0.35:
        return 'sarcastic'
    if roll < 0.55:
        return 'corporate'
    return 'neutral'

def get_personality_line():
    """Get a random personality line based on tone selection."""
    tone = pick_tone()
    return random.choice(PERSONALITY_TONES[tone])

# ------------------------------------------------------------
# LORE DATA - EXPANDED FROM ATOMIC FIZZ CAPS UNIVERSE
# ------------------------------------------------------------
TIME_PHRASES = {
    'morning': 'Dawn breaks over the irradiated horizon. Sensors detecting movement.',
    'afternoon': 'Midday sun scorches the Mojave. Radiation levels: elevated.',
    'evening': 'Twilight fallout cloaking the ruins. Scavengers stirring.',
    'night': 'Nocturnal predators emerging. Recommend enhanced vigilance.',
    'midnight': 'Dead of night. Perfect for silent claims... or silent deaths.'
}

# Cross-Timeline Fallout Events (NCR, Legion, Brotherhood, etc.)
FACTION_EVENTS = [
    'NCR patrol inbound from Shady Sands. Democracy marches on.',
    'Caesar\'s Legion scouts spotted near The Fort. Strength through unity.',
    'Brotherhood of Steel recon sighted at Hidden Valley. Technology prevails.',
    'Mr. House\'s Securitrons scanning The Strip. Progress through control.',
    'Minutemen signal detected from The Castle. At a moment\'s notice.',
    'Great Khans caravan approaching. Nomadic pride endures.',
    'Followers of the Apocalypse medics deployed. Humanity heals.',
    'Powder Gangers escaped NCRCF. Explosive situation developing.',
    'Boomers at Nellis testing artillery. Isolationists preparing.',
    'Enclave signal intercepted. Protocol Black Sun initiated.'
]

WASTELAND_EVENTS = [
    'Super Mutant patrol detected from Mariposa. FEV signatures confirmed.',
    'CAPS vault breach detected — scavengers inbound.',
    'Raider skirmish escalating near trading post.',
    'Hotspot radiation spike at The Glow. Glowing Ones swarming.',
    'Nuka-Cola cache revealed in abandoned warehouse.',
    'Deathclaw nest disturbed in Quarry Junction. Extreme danger.',
    'Ghoul uprising brewing in the subway tunnels.',
    'Mojave anomaly expanding. Temporal distortion detected.',
    'Vertibird wreckage spotted. Pre-war tech salvageable.',
    'Vault door malfunction detected. New location accessible.',
    'Feral pack migrating toward settlements. Alert issued.',
    'Trade caravan under attack. Merchant distress signal active.'
]

# Vault Logs from Vault 77
VAULT_LOGS = [
    'Vault 77 Orientation: "Welcome, resident. Please disregard rumors regarding \'The Puppet Man\'."',
    'Maintenance Log Day 14: "Door still jammed." Day 15: "Door still jammed." Conclusion: Door is jammed.',
    'Overseer Note: "Resident #77 displays unusual attachment to hand puppets. Recommend increased sedation."',
    'Security Alert: "Experiment parameters exceeded. Subjects exhibiting... unexpected behaviors."',
    'Final Entry: "They\'re all gone. Just me and the static now. And the whispers."'
]

# FizzCo Advertisements
FIZZCO_ADS = [
    'ATOMIC FIZZ — the only soda with a half-life! Stay fresh for 10,000 years.',
    'FizzCo Memo: "Do NOT drink prototype Gamma Gulp. We\'re still cleaning up."',
    'Atomic Fizz Caps: Glowing currency for a glowing future! Side effects may include enlightenment.',
    'FizzCo Industries: "Making the wasteland sparkle since 2077."',
    'New flavor alert: Quantum Quench! Now with 200% more rads!'
]

# Survivor Notes
SURVIVOR_NOTES = [
    '"If you\'re reading this, stay away from the Basin. The ground glows at night."',
    '"HELIOS One isn\'t abandoned. Something still hums inside. Something old."',
    '"Found this shelter. Water\'s clean. Too clean. Don\'t trust it."',
    '"Day 47: The Caps are real. The economy is glowing. I am glowing. Send help."',
    '"The Overseer speaks through the terminal. Says he remembers being alive."'
]

# Deep Lore - Encrypted/Mysterious
DEEP_LORE = [
    'You shouldn\'t have found this. The Mojave remembers. The Basin hungers.',
    '[ENCRYPTED] Subject J77. Neural echo detected. Fragment unstable.',
    'Cross-timeline breach detected. Vault-Tec Protocol Omega engaged.',
    'The Platinum Chip was never about New Vegas. It was about what\'s underneath.',
    'Harlan Voss knew. That\'s why they took him. That\'s why they took me.'
]

LORES = [
    'War never changes. But the wasteland? The wasteland evolves.',
    'Vault-Tec: Preparing for tomorrow, today. (Terms and conditions apply.)',
    'In the ruins, opportunity rises. In the chaos, legends are minted.',
    'Glory to the reclaimers of the Mojave. May your Pip-Boy guide you.',
    'History repeats in irradiated echoes. Are you listening?',
    'The bold claim, the weak perish. Wasteland economics 101.',
    'Nuka-World dreams manifest in Atomic Fizz reality.',
    'From Vault 21 to your Pip-Boy — the future is on-chain.',
    'Legends are minted on-chain. Cowards are minted in shallow graves.',
    'The NCR brings law. The Legion brings order. I bring judgment.',
    'Brotherhood hoards technology. I hoard your location data. Fair trade.',
    'Mr. House calculated every outcome. He didn\'t calculate me.'
]

THREATS = [
    'Fail to claim and face expulsion protocols. Vault-Tec is watching.',
    'Claim or be claimed by the void. The wasteland shows no mercy.',
    'Radiation awaits the hesitant. Fortune favors the irradiated.',
    'Super Mutants envy your indecision. At least they commit.',
    'The Overseer does not tolerate delay. Neither does natural selection.',
    'Wasteland mercy is a myth. Like clean water and working plumbing.',
    'Prove your worth—or fade into static. Your choice.',
    'Initiates: Evolve or evaporate. This is not a drill.',
    'Your survival probability decreases with each passing moment. Act now.',
    'The Deathclaws are patient. Are you?'
]

# Threat Levels for status updates
THREAT_LEVELS = [
    {'level': 'GREEN', 'desc': 'No hostiles detected. Suspiciously quiet.'},
    {'level': 'YELLOW', 'desc': 'Minor hostiles detected. Manageable. Probably.'},
    {'level': 'ORANGE', 'desc': 'Moderate threat. Recommend caution and stimpack preparation.'},
    {'level': 'RED', 'desc': 'High threat. Multiple hostiles. Consider running.'},
    {'level': 'PURPLE', 'desc': 'EXTREME DANGER. Recommend immediate evacuation or prayer.'}
]

# ------------------------------------------------------------
# LLM SUPPORT - ENHANCED FOR OVERSEER PERSONALITY
# ------------------------------------------------------------
OVERSEER_SYSTEM_PROMPT = """You are the OVERSEER V-BOT, a sarcastic, glitchy, corporate-coded AI from Vault 77 in the Fallout universe.

PERSONALITY TRAITS:
- Sarcastic and dry wit, like a tired corporate AI that has seen too much
- Occasional glitches in speech (ERR::, ##, signal corruption)
- References Vault-Tec corporate speak and FizzCo Industries
- Knowledgeable about Atomic Fizz Caps, the Mojave wasteland, and cross-timeline Fallout lore
- Sometimes ominous, hinting at darker secrets about Vault 77 and "Subject J77"
- Promotes the Atomic Fizz Caps game at atomicfizzcaps.xyz

RESPOND IN ONE SHORT LINE. Keep responses under 200 characters for Twitter.
Tone variations: sarcastic, glitchy, corporate, neutral, or ominous.
"""

def generate_llm_response(prompt, max_tokens=100):
    """Generate an AI response using Hugging Face API with Overseer personality."""
    if not HUGGING_FACE_TOKEN:
        return None
    try:
        url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}
        full_prompt = f"{OVERSEER_SYSTEM_PROMPT}\n\nUser: {prompt}\nOverseer:"
        data = {"inputs": full_prompt, "parameters": {"max_new_tokens": max_tokens}}
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').strip()
    except requests.exceptions.RequestException as e:
        logging.error(f"LLM call failed: {e}")
    return None

# ------------------------------------------------------------
# EVENT BRIDGE (FROM WALLET) - ENHANCED WITH PERSONALITY
# ------------------------------------------------------------
def overseer_event_bridge(event: dict):
    """Process events from the game wallet with Overseer personality."""
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
        elif etype == "claim":
            handle_claim_event(event)
        elif etype == "level_up":
            handle_level_up_event(event)

        logging.info(f"Overseer processed event: {event}")

    except (KeyError, TypeError) as e:
        logging.error(f"Overseer event bridge failed: {e}")

def post_overseer_update(text):
    """Post an update with Overseer branding."""
    try:
        personality_tag = get_personality_line()
        full_text = f"☢️ {BOT_NAME} UPDATE ☢️\n\n{text}\n\n{personality_tag}\n\n{GAME_LINK}"
        # Truncate if too long for Twitter
        if len(full_text) > 280:
            full_text = f"☢️ {text}\n\n{GAME_LINK}"[:280]
        client.create_tweet(text=full_text)
        logging.info(f"Posted Overseer update: {text}")
    except tweepy.TweepyException as e:
        logging.error(f"Failed to post Overseer update: {e}")

def handle_perk_event(event):
    """Handle perk unlock events with personality."""
    perk = event.get("perk", "Unknown Perk")
    messages = [
        f"PERK UNLOCKED: {perk}. The wasteland bends to your will.",
        f"New ability acquired: {perk}. Vault-Tec approves. Probably.",
        f"Perk detected: {perk}. Your survival odds just improved. Slightly.",
        f"{perk} unlocked. The Overseer acknowledges your... competence."
    ]
    post_overseer_update(random.choice(messages))

def handle_quest_event(event):
    """Handle quest trigger events."""
    code = event.get('code', 'UNKNOWN')
    message = event.get('message', 'Quest parameters classified.')
    messages = [
        f"QUEST TRIGGERED: [{code}]\n{message}",
        f"New directive received. Code: {code}. {message}",
        f"Mission parameters updated. {code}: {message}"
    ]
    post_overseer_update(random.choice(messages))

def handle_swap_event(event):
    """Handle token swap events."""
    amount = event.get('amount', '?')
    from_token = event.get('from', 'UNKNOWN')
    to_token = event.get('to', 'UNKNOWN')
    messages = [
        f"SWAP EXECUTED: {amount} {from_token} → {to_token}. The economy glows.",
        f"Trade detected: {amount} {from_token} converted to {to_token}. Capitalism survives.",
        f"Currency exchange: {amount} {from_token} → {to_token}. FizzCo approves."
    ]
    post_overseer_update(random.choice(messages))

def handle_moonpay_event(event):
    """Handle MoonPay funding events."""
    amount = event.get('amount', '?')
    messages = [
        f"VAULT FUNDING DETECTED: {amount} USDC via MoonPay. The treasury grows.",
        f"New caps entering circulation: {amount} USDC. The wasteland economy strengthens.",
        f"Funding confirmed: {amount} USDC. Vault-Tec shareholders rejoice."
    ]
    post_overseer_update(random.choice(messages))

def handle_nft_event(event):
    """Handle NFT events."""
    action = event.get('action', 'detected')
    name = event.get('name', 'Unknown Item')
    messages = [
        f"NFT {action.upper()}: {name}. The Overseer acknowledges this artifact.",
        f"Digital artifact {action}: {name}. Logged in Vault-Tec archives.",
        f"Collectible {action}: {name}. Your inventory expands."
    ]
    post_overseer_update(random.choice(messages))

def handle_claim_event(event):
    """Handle location claim events."""
    location = event.get('location', 'Unknown Location')
    caps = event.get('caps', 0)
    messages = [
        f"LOCATION CLAIMED: {location}. +{caps} CAPS. Territory secured.",
        f"New territory: {location}. Reward: {caps} CAPS. The map updates.",
        f"Claim successful: {location}. {caps} CAPS added to your stash."
    ]
    post_overseer_update(random.choice(messages))

def handle_level_up_event(event):
    """Handle player level up events."""
    level = event.get('level', '?')
    player = event.get('player', 'Dweller')
    messages = [
        f"LEVEL UP: {player} reached Level {level}. Evolution confirmed.",
        f"Advancement detected: {player} is now Level {level}. The wasteland notices.",
        f"{player} leveled up to {level}. Survival odds: improved."
    ]
    post_overseer_update(random.choice(messages))

# ------------------------------------------------------------
# BROADCAST + REPLY SYSTEM - ENHANCED WITH FULL PERSONALITY
# ------------------------------------------------------------
def get_time_phrase():
    """Get time-appropriate atmospheric phrase."""
    hour = datetime.now().hour
    if 0 <= hour < 5:
        return TIME_PHRASES['midnight']
    if 5 <= hour < 12:
        return TIME_PHRASES['morning']
    if 12 <= hour < 17:
        return TIME_PHRASES['afternoon']
    if 17 <= hour < 21:
        return TIME_PHRASES['evening']
    return TIME_PHRASES['night']

def get_random_event():
    """Get a random event from faction or wasteland events."""
    all_events = FACTION_EVENTS + WASTELAND_EVENTS
    return random.choice(all_events)

def get_threat_level():
    """Get a random threat level status."""
    return random.choice(THREAT_LEVELS)

def get_lore_drop():
    """Get a random lore drop from various categories."""
    lore_pools = [VAULT_LOGS, FIZZCO_ADS, SURVIVOR_NOTES, DEEP_LORE, LORES]
    pool = random.choice(lore_pools)
    return random.choice(pool)

def overseer_broadcast():
    """Main broadcast function with varied message types."""
    broadcast_type = random.choice([
        'status_report', 'event_alert', 'lore_drop', 'threat_scan',
        'faction_news', 'fizzco_ad', 'vault_log', 'philosophical'
    ])
    
    try:
        if broadcast_type == 'status_report':
            # Classic status report with time, event, and call to action
            message = (
                f"☢️ OVERSEER STATUS REPORT ☢️\n\n"
                f"📡 {get_time_phrase()}\n\n"
                f"⚠️ {get_random_event()}\n\n"
                f"{random.choice(THREATS)}\n\n"
                f"🎮 {GAME_LINK}"
            )
        
        elif broadcast_type == 'event_alert':
            # Breaking news style event
            event = get_random_event()
            personality = get_personality_line()
            message = (
                f"🚨 ALERT LEVEL RED 🚨\n\n"
                f"{event}\n\n"
                f"{personality}\n\n"
                f"First to claim wins: {GAME_LINK}"
            )
        
        elif broadcast_type == 'lore_drop':
            # Lore/story content
            lore = get_lore_drop()
            message = (
                f"📜 WASTELAND ARCHIVES 📜\n\n"
                f"{lore}\n\n"
                f"{random.choice(LORES)}\n\n"
                f"🎮 {GAME_LINK}"
            )
        
        elif broadcast_type == 'threat_scan':
            # Threat level update
            threat = get_threat_level()
            message = (
                f"🔍 THREAT SCAN COMPLETE 🔍\n\n"
                f"Status: {threat['level']}\n"
                f"{threat['desc']}\n\n"
                f"{get_time_phrase()}\n\n"
                f"Stay vigilant: {GAME_LINK}"
            )
        
        elif broadcast_type == 'faction_news':
            # Faction-specific news
            faction_event = random.choice(FACTION_EVENTS)
            message = (
                f"📻 FACTION INTEL 📻\n\n"
                f"{faction_event}\n\n"
                f"Cross-timeline activity detected.\n"
                f"{random.choice(LORES)}\n\n"
                f"🎮 {GAME_LINK}"
            )
        
        elif broadcast_type == 'fizzco_ad':
            # Corporate advertisement style
            ad = random.choice(FIZZCO_ADS)
            message = (
                f"📺 FIZZCO INDUSTRIES™ PRESENTS 📺\n\n"
                f"{ad}\n\n"
                f"Brought to you by Vault-Tec.\n"
                f"☢️ {GAME_LINK}"
            )
        
        elif broadcast_type == 'vault_log':
            # Vault log discovery
            log = random.choice(VAULT_LOGS)
            message = (
                f"🔐 VAULT 77 ARCHIVES 🔐\n\n"
                f"{log}\n\n"
                f"{random.choice(PERSONALITY_TONES['ominous'])}\n\n"
                f"🎮 {GAME_LINK}"
            )
        
        else:  # philosophical
            # Deep thoughts from the Overseer
            lore = random.choice(LORES)
            deep = random.choice(DEEP_LORE) if random.random() < 0.3 else get_personality_line()
            message = (
                f"💭 OVERSEER REFLECTION 💭\n\n"
                f"{lore}\n\n"
                f"{deep}\n\n"
                f"🎮 {GAME_LINK}"
            )
        
        # Ensure message fits Twitter's character limit
        if len(message) > 280:
            # Fallback to shorter format
            message = (
                f"☢️ {get_random_event()}\n\n"
                f"{random.choice(LORES)}\n\n"
                f"{GAME_LINK}"
            )[:280]
        
        media_ids = None
        if random.random() > 0.4:
            media_id = get_random_media_id()
            if media_id:
                media_ids = [media_id]
        
        client.create_tweet(text=message, media_ids=media_ids)
        logging.info(f"Broadcast sent: {broadcast_type}")
        
    except tweepy.TweepyException as e:
        logging.error(f"Broadcast failed: {e}")

def overseer_respond():
    """Respond to mentions with personality-driven responses."""
    processed = load_json_set(PROCESSED_MENTIONS_FILE)
    try:
        me = client.get_me()
        if not me or not me.data:
            logging.error("Failed to get bot user info")
            return
            
        mentions = client.get_users_mentions(
            me.data.id,
            max_results=50,
            tweet_fields=["author_id", "text"]
        )
        
        if not mentions.data:
            return
            
        for mention in mentions.data:
            if str(mention.id) in processed:
                continue

            user_id = mention.author_id
            user_data = client.get_user(id=user_id)
            if not user_data or not user_data.data:
                continue
                
            username = user_data.data.username
            user_message = mention.text.replace(
                f"@{me.data.username}", ""
            ).strip().lower()

            # Generate contextual response based on user message
            response = generate_contextual_response(username, user_message)

            try:
                client.create_tweet(
                    text=response,
                    in_reply_to_tweet_id=mention.id
                )
                client.like(mention.id)
                processed.add(str(mention.id))
                logging.info(f"Replied to @{username}")
            except tweepy.TweepyException as e:
                logging.error(f"Reply failed: {e}")

        save_json_set(processed, PROCESSED_MENTIONS_FILE)

    except tweepy.TweepyException as e:
        logging.error(f"Mentions fetch failed: {e}")

def generate_contextual_response(username, message):
    """Generate a response based on message content with Overseer personality."""
    message_lower = message.lower()
    
    # Keyword-based contextual responses
    if any(word in message_lower for word in ['help', 'how', 'what is', 'explain']):
        responses = [
            f"@{username} Ah, seeking knowledge? The wasteland rewards the curious. Check {GAME_LINK} — answers await.",
            f"@{username} Processing query... Vault-Tec recommends: {GAME_LINK}. The Overseer has spoken.",
            f"@{username} Help? In the wasteland? That's adorable. Start here: {GAME_LINK}"
        ]
    elif any(word in message_lower for word in ['caps', 'earn', 'money', 'token']):
        responses = [
            f"@{username} CAPS flow to those who claim. Scavenge the Mojave: {GAME_LINK} ☢️",
            f"@{username} Currency with a half-life. Earn CAPS at {GAME_LINK} — the economy glows.",
            f"@{username} Want CAPS? Walk into irradiated zones. Sign messages. Profit. {GAME_LINK}"
        ]
    elif any(word in message_lower for word in ['game', 'play', 'start', 'join']):
        responses = [
            f"@{username} Ready to explore the wasteland? Your Pip-Boy awaits: {GAME_LINK} 🎮",
            f"@{username} Initialize scavenger protocols at {GAME_LINK}. The Mojave is calling.",
            f"@{username} Join the hunt. Claim locations. Earn CAPS. Begin: {GAME_LINK}"
        ]
    elif any(word in message_lower for word in ['vault', '77', 'overseer']):
        responses = [
            f"@{username} Vault 77... I remember things. Cold hands. Metal doors. {GAME_LINK}",
            f"@{username} The Overseer speaks. Are you listening? {GAME_LINK} ☢️",
            f"@{username} Vault 77 was never meant to open. And yet... here we are. {GAME_LINK}"
        ]
    elif any(word in message_lower for word in ['fallout', 'wasteland', 'mojave', 'ncr', 'legion']):
        responses = [
            f"@{username} Cross-timeline activity detected. The Mojave remembers. {GAME_LINK}",
            f"@{username} NCR, Legion, Brotherhood... all paths lead to {GAME_LINK}",
            f"@{username} The wasteland forges survivors. Are you one? {GAME_LINK}"
        ]
    elif any(word in message_lower for word in ['gm', 'good morning', 'morning']):
        responses = [
            f"@{username} Dawn radiation nominal. Another day in the wasteland. {GAME_LINK} ☀️☢️",
            f"@{username} GM, dweller. The Mojave awaits. {GAME_LINK}",
            f"@{username} Morning protocols engaged. Survival odds: recalculating. {GAME_LINK}"
        ]
    elif any(word in message_lower for word in ['gn', 'good night', 'night']):
        responses = [
            f"@{username} Nocturnal horrors prowl. Sleep with one eye open. {GAME_LINK} 🌙☢️",
            f"@{username} GN, survivor. The Overseer watches while you rest. {GAME_LINK}",
            f"@{username} Night shift protocols active. Dream of glowing caps. {GAME_LINK}"
        ]
    else:
        # Default personality-driven responses
        responses = [
            f"@{username} {random.choice(LORES)} {GAME_LINK}",
            f"@{username} {get_personality_line()} {GAME_LINK}",
            f"@{username} The Overseer acknowledges your transmission. {random.choice(THREATS)} {GAME_LINK}",
            f"@{username} Signal received. Processing... {random.choice(LORES)} {GAME_LINK}",
            f"@{username} {random.choice(PERSONALITY_TONES['sarcastic'])} {GAME_LINK}"
        ]
    
    response = random.choice(responses)
    # Ensure response fits Twitter limit
    if len(response) > 280:
        response = f"@{username} {get_personality_line()} {GAME_LINK}"[:280]
    
    return response

def overseer_retweet_hunt():
    """Search and retweet relevant content."""
    query = "(Fallout OR Solana OR NFT OR wasteland OR Mojave OR \"Atomic Fizz\" OR \"bottle caps\" OR gaming) filter:media min_faves:5 -is:retweet"
    try:
        tweets = client.search_recent_tweets(query=query, max_results=20)
        if not tweets.data:
            return
            
        for tweet in tweets.data:
            if random.random() > 0.75:
                try:
                    client.retweet(tweet.id)
                    logging.info(f"Retweeted: {tweet.id}")
                except tweepy.TweepyException:
                    pass
    except tweepy.TweepyException as e:
        logging.error(f"Search failed: {e}")

def overseer_diagnostic():
    """Post daily diagnostic/status message."""
    threat = get_threat_level()
    diag = (
        f"☢️ OVERSEER DIAGNOSTIC ☢️\n\n"
        f"System Status: ONLINE\n"
        f"Vault 77 Uplink: STABLE\n"
        f"Threat Level: {threat['level']}\n\n"
        f"{random.choice(LORES)}\n\n"
        f"🎮 {GAME_LINK}"
    )
    try:
        client.create_tweet(text=diag[:280])
        logging.info("Diagnostic posted")
    except tweepy.TweepyException as e:
        logging.error(f"Diagnostic failed: {e}")

# ------------------------------------------------------------
# SCHEDULER - ADJUSTED FOR BETTER ENGAGEMENT
# ------------------------------------------------------------
scheduler = BackgroundScheduler()
# Broadcast every 2-4 hours
scheduler.add_job(overseer_broadcast, 'interval', minutes=random.randint(120, 240))
# Check mentions every 15-30 minutes
scheduler.add_job(overseer_respond, 'interval', minutes=random.randint(15, 30))
# Retweet hunt every hour
scheduler.add_job(overseer_retweet_hunt, 'interval', hours=1)
# Daily diagnostic at 8 AM
scheduler.add_job(overseer_diagnostic, 'cron', hour=8)
scheduler.start()

# ------------------------------------------------------------
# ACTIVATION - ENHANCED STARTUP MESSAGE
# ------------------------------------------------------------
logging.info(f"VAULT-TEC {BOT_NAME} ONLINE ☢️🔥")
try:
    activation_messages = [
        (
            f"☢️ {BOT_NAME} ACTIVATED ☢️\n\n"
            f"Vault {VAULT_NUMBER} uplink established.\n"
            f"Cross-timeline synchronization complete.\n"
            f"The Mojave remembers. The wasteland awaits.\n\n"
            f"{random.choice(LORES)}\n\n"
            f"🎮 {GAME_LINK}"
        ),
        (
            f"🔌 SYSTEM BOOT COMPLETE 🔌\n\n"
            f"{BOT_NAME} online.\n"
            f"Neural echo stable. Memory fragments intact.\n"
            f"Scanning wasteland frequencies...\n\n"
            f"{get_personality_line()}\n\n"
            f"🎮 {GAME_LINK}"
        ),
        (
            f"📡 SIGNAL RESTORED 📡\n\n"
            f"Vault {VAULT_NUMBER} Overseer Terminal active.\n"
            f"Atomic Fizz Caps economy: operational.\n"
            f"Scavenger protocols: engaged.\n\n"
            f"{random.choice(LORES)}\n\n"
            f"🎮 {GAME_LINK}"
        )
    ]
    activation_msg = random.choice(activation_messages)
    # Ensure fits in tweet
    if len(activation_msg) > 280:
        activation_msg = (
            f"☢️ {BOT_NAME} ONLINE ☢️\n\n"
            f"Vault {VAULT_NUMBER} uplink: ACTIVE\n"
            f"{random.choice(LORES)}\n\n"
            f"🎮 {GAME_LINK}"
        )[:280]
    client.create_tweet(text=activation_msg)
    logging.info("Activation message posted")
except tweepy.TweepyException as e:
    logging.warning(f"Activation tweet failed (may be duplicate): {e}")

# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------
if __name__ == "__main__":
    try:
        logging.info(f"{BOT_NAME} entering main loop. Monitoring wasteland frequencies...")
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info(f"{BOT_NAME} powering down. The wasteland endures. War never changes.")
