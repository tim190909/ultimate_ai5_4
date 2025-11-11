import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ALERT_CHANNEL_NAME = os.getenv("DISCORD_ALERT_CHANNEL", "trading-alerts")
DB_PATH = os.getenv("DB_PATH", "ultimate_ai5_4.db")
CHECK_INTERVAL = 1800 # 30 minutes
FUT_TAX_RATE = 0.05
CACHE_TTL_HOURS = 12
DEFAULT_PLATFORM = "ps"
