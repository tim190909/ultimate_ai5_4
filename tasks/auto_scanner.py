from discord.ext import tasks
from utils.futbin_api import get_player_price
from db.models import fetch_all
from config import ALERT_CHANNEL
import discord

@tasks.loop(seconds=1800) # 30 minutes par défaut
async def auto_price_check(bot):
    """
    Tâche automatique qui scanne les prix des joueurs de la watchlist
    et envoie les alertes dans le channel dédié.
    """
    print("🔎 Scan automatique des prix en cours...")

    watchlist = await fetch_all("SELECT DISTINCT player_id FROM watchlist")

    for row in watchlist:
        player_id = row["player_id"]
        price = await get_player_price(player_id)

        if price is None:
            continue

        channel = discord.utils.get(bot.get_all_channels(), name=ALERT_CHANNEL)
        if channel:
            try:
                await channel.send(f"📊 Nouveau prix pour ID **{player_id}** : `{price}` crédits")
            except Exception as e:
                print(f"❌ Erreur envoi message auto_price_check: {e}")
