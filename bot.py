# bot.py
import discord
from discord.ext import commands
from views.main_menu import MainMenu, SBCModal
from db import models
from tasks.scheduler import start_tasks
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, description="ULTIMATE AI 5.4")

@bot.event
async def on_ready():
    await models.init_db() # Initialisation base de données
    await bot.tree.sync() # Synchronisation des slash commands
    start_tasks(bot) # Démarre les tasks (price check, alert, etc.)
    print(f"Bot connecté : {bot.user}")

# Slash command pour ouvrir le menu principal
@bot.tree.command(name="menu", description="Ouvre le menu principal")
async def menu(interaction: discord.Interaction):
    await interaction.response.send_message("Bienvenue dans le menu principal :", view=MainMenu())

bot.run(DISCORD_TOKEN)
