from .auto_scanner import auto_price_check
from config import CHECK_INTERVAL

def start_scheduled_tasks(bot):
    """
    Démarre toutes les tâches programmées du bot.
    """
    auto_price_check.change_interval(seconds=CHECK_INTERVAL)
    auto_price_check.start(bot)
    print("⏱️ Tâches automatiques démarrées.")
