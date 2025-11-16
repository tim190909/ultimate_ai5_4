import discord
from discord.ext import commands
import threading
from flask import Flask
import os
import asyncio

from config import DISCORD_TOKEN
from db.database import init_db
from tasks.scheduler import start_scheduled_tasks

# ----------------------
# Discord Bot
# ----------------------
INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=INTENTS,
    help_command=None,
    description="FUT Trading Bot – Version 41.0 Market Vision AI + Flask keepalive"
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
    print(f"🤖 Bot connecté : {bot.user}")
    await init_db()

    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✔️ Cog chargé : {cog}")
        except Exception as e:
            print(f"❌ Erreur chargement {cog} : {e}")

    await bot.tree.sync()
    print("✨ Slash commands synchronisées !")
    start_scheduled_tasks(bot)
    print("🚀 Bot prêt et tâches programmées lancées !")

# ----------------------
# Flask Keep-Alive
# ----------------------
app = Flask("")

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Lancer Flask dans un thread séparé
threading.Thread(target=run_flask).start()

# ----------------------
# Run Discord Bot
# ----------------------
bot.run(DISCORD_TOKEN)
