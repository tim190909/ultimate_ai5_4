import discord
from discord.ext import commands
import os
import asyncio

from db.database import init_db
from tasks.scheduler import start_scheduled_tasks

TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.getenv("PORT", 10000)) # Render Free fournit un PORT

INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=INTENTS,
    help_command=None,
    description="FUT Trading Bot – Version 41.0"
)

# Liste des Cogs
COGS = [
    "cogs.menu",
    "cogs.market",]
import discord
from discord.ext import commands
import os
import asyncio
from config import DISCORD_TOKEN, CHECK_INTERVAL
from db.database import init_db
from tasks.scheduler import start_scheduled_tasks

INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=INTENTS,
    help_command=None,
    description="FUT Trading Bot – Version 42 Render Free"
)

COGS = [
    "cogs.menu",
    "cogs.market",
    "cogs.watchlist",
    "cogs.alerts",
    "cogs.forecast_ai"
]

@bot.event
async def on_ready():
    print(f"✅ Bot connecté : {bot.user}")
    
    # Base de données
    await init_db()

    # Charger les cogs
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✔️ Cog chargé : {cog}")
        except Exception as e:
            print(f"❌ Erreur chargement {cog} : {e}")

    # Synchroniser les slash commands
    await bot.tree.sync()
    print("✔️ Commandes slash synchronisées")

    # Lancer les tâches automatiques
    start_scheduled_tasks(bot)
    print("🚀 Version 42 démarrée avec succès !")

bot.run(DISCORD_TOKEN)
