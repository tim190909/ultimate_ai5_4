import os
import asyncio
import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from views.main_menu import MainMenu
from db.models import init_db
from tasks.scheduler import start_tasks

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, description="ULTIMATE AI 5.4 MODERNE")

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")
    await init_db()
    await bot.tree.sync()
    start_tasks(bot)
    # Envoie automatique du menu dans le premier salon disponible
    for guild in bot.guilds:
        channel = guild.text_channels[0]
        if channel:
            await channel.send("🚀 **Bienvenue dans ULTIMATE AI 5.4 !**", view=MainMenu())
    print("📊 Menu envoyé automatiquement")

@bot.tree.command(name="menu", description="Ouvre le menu principal")
async def menu(interaction: discord.Interaction):
    await interaction.response.send_message("📋 **Menu Principal :**", view=MainMenu())

# ---------------- Auto-reconnexion ----------------
while True:
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"⚠️ Bot déconnecté, tentative de reconnexion : {e}")
        asyncio.run(asyncio.sleep(5))
