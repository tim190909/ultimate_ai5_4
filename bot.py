import asyncio
from threading import Thread
from flask import Flask

import discord
from discord.ext import commands, tasks

from config import DISCORD_TOKEN, ALERT_CHANNEL_NAME, CHECK_INTERVAL
from views.main_menu import MainMenu
from db import models
from tasks.scheduler import start_tasks

# ---------------- Discord Bot ----------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, description="ULTIMATE AI 5.4")

@bot.event
async def on_ready():
    await models.init_db()
    await bot.tree.sync()
    start_tasks(bot)
    print(f"Bot connecté : {bot.user}")

@bot.tree.command(name="menu", description="Ouvre le menu principal")
async def menu(interaction: discord.Interaction):
    await interaction.response.send_message("Menu principal :", view=MainMenu())

# ---------------- Serveur web pour ping ----------------
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

# ---------------- Lancer le bot ----------------
bot.run(DISCORD_TOKEN)
