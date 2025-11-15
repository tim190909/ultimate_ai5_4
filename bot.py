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
    "cogs.market",
    "cogs.watchlist",
    "cogs.alerts",
    "cogs.forecast_ai"
]

@bot.event
async def on_ready():
    print(f"🤖 Bot connecté : {bot.user}")

    # Initialisation DB
    await init_db()

    # Charger les Cogs
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✔️ Cog chargé : {cog}")
        except Exception as e:
            print(f"❌ Erreur chargement {cog} : {e}")

    # Synchronisation slash commands
    try:
        await bot.tree.sync()
        print("✨ Commandes slash synchronisées !")
    except Exception as e:
        print(f"❌ Erreur sync : {e}")

    # Démarrage du scheduler
    start_scheduled_tasks(bot)

    print("🚀 Bot prêt et en ligne 24/7 !")

# Mini serveur web pour Render Free
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot en ligne ✅")

app = web.Application()
app.router.add_get("/", handle)

async def start_web():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🌐 Serveur web démarré sur le port {PORT}")

async def main():
    await start_web()
    await bot.start(TOKEN)

# Lancer le bot + serveur web
asyncio.run(main())
