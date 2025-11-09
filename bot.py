import discord
from discord.ext import commands
from views.main_menu import MainMenu
from db import models
from tasks.scheduler import start_tasks
from config import DISCORD_TOKEN
import asyncio
from aiohttp import web
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, description="ULTIMATE AI 5.4")

# ---------------- Webserver pour UptimeRobot ----------------
async def handle_ping(request):
    return web.Response(text="Bot actif !")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000)) # Render fournit une variable PORT
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"======== Webserver démarré sur le port {port} ========")

# ---------------- Événement on_ready ----------------
@bot.event
async def on_ready():
    await models.init_db()
    await bot.tree.sync()
    start_tasks(bot)
    asyncio.create_task(start_webserver()) # Démarre le serveur web
    print(f"Bot connecté : {bot.user}")

# ---------------- Commande slash /menu ----------------
@bot.tree.command(name="menu", description="Ouvre le menu principal")
async def menu(interaction: discord.Interaction):
    await interaction.response.send_message("Menu principal :", view=MainMenu())

# ---------------- Run ----------------
bot.run(DISCORD_TOKEN)