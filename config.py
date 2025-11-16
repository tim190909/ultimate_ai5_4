import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DB_PATH = os.getenv("DB_PATH", "database.db")
FUTBIN_API_KEY = os.getenv("FUTBIN_API_KEY", None)
ALERT_CHANNEL = os.getenv("ALERT_CHANNEL", "trading-alerts")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 1800))
APPLICATION_ID = os.getenv("APPLICATION_ID") # Pour Render