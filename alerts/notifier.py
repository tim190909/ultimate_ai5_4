import discord
from config import ALERT_CHANNEL_NAME

async def send_price_alert(bot, message: str):
    channel = discord.utils.get(bot.get_all_channels(), name=ALERT_CHANNEL_NAME)
    if channel:
        await channel.send(f"⚠️ **Alerte de prix :** {message}")
