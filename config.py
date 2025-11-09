import os
from dotenv import load_dotenv

load_dotenv()

# --- Discord ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ALERT_CHANNEL_NAME = os.getenv("DISCORD_ALERT_CHANNEL", "trading-alerts")

# --- Base de données ---
DB_PATH = os.getenv("DB_PATH", "ultimate_ai5_4.db")

# --- Futbin ---
CACHE_FILE = "popular_players_cache.json"
CACHE_TTL_HOURS = 12

# --- Bot & tâches ---
CHECK_INTERVAL = 900 # 15 minutes

# --- Finance ---
FUT_TAX_RATE = 0.05
	
