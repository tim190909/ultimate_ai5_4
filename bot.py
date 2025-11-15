import discord
from discord.ext import commands
import os
import asyncio

from config import DISCORD_TOKEN, CHECK_INTERVAL
from tasks.auto_scanner import start_scheduled_tasks

INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=INTENTS,
    help_command=None,
    description="FUT Trading Bot – Version 41.0 Market Vision AI Adaptive"
)

# --------------------------
# LOAD COGS AUTOMATIQUEMENT
# --------------------------

COGS = [
    "cogs.menu",
    "cogs.market",
    "cogs.watchlist",
    "cogs.alerts",
    "cogs.forecast_ai"
]

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que : {bot.user}")

    # Charger les cogs
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✔️ Cog chargé : {cog}")
        except Exception as e:
            print(f"❌ Erreur chargement {cog} : {e}")

    # Synchronisation slash commands
    await bot.tree.sync()
    print("✔️ Commandes slash synchronisées.")

    # Lancer tâches automatiques
    start_scheduled_tasks(bot)

    print("🚀 Version 41.0 démarrée avec succès !")

bot.run(DISCORD_TOKEN)
