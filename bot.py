import discord
from discord.ext import commands
import threading
from flask import Flask
import asyncio
import os

from config import DISCORD_TOKEN, ALERT_CHANNEL, CHECK_INTERVAL
from db.database import init_db
from tasks.scheduler import start_scheduled_tasks

# ------------------------
# BOT DISCORD
# ------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    description="FUT Trading Bot – Version 41.0 Render Ready"
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

async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✔️ Cog chargé : {cog}")
        except Exception as e:
            print(f"❌ Erreur chargement {cog} : {e}")

# ------------------------
# MINI SERVEUR FLASK POUR RENDER
# ------------------------
app = Flask("")

@app.route("/")
def home():
    return "Bot Discord est actif ✅"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()

# ------------------------
# LANCER BOT
# ------------------------
async def main():
    await init_db()
    await load_cogs()
    start_scheduled_tasks(bot)
    await bot.start(DISCORD_TOKEN)

asyncio.run(main())
