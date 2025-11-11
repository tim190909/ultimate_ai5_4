from discord.ext import tasks
from alerts.notifier import send_price_alert
from config import CHECK_INTERVAL

def start_tasks(bot):
    @tasks.loop(seconds=CHECK_INTERVAL)
    async def price_check():
        await send_price_alert(bot, "Vérification automatique terminée ✅")
    price_check.start()
