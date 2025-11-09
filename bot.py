# bot.py
import discord
from discord.ext import commands
from views.main_menu import MainMenu
from db import models
from tasks.scheduler import start_tasks
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, description="ULTIMATE AI 5.4")

# ---------------- Event on_ready ----------------
@bot.event
async def on_ready():
    # Initialiser la DB
    await models.init_db()
    
    # Synchroniser les commandes slash
    await bot.tree.sync()
    
    # Démarrer les tâches automatiques (ex: vérification prix)
    start_tasks(bot)
    
    print(f"Bot connecté : {bot.user}")

# ---------------- Commande slash pour le menu principal ----------------
@bot.tree.command(name="menu", description="Ouvre le menu principal")
async def menu(interaction: discord.Interaction):
    await interaction.response.send_message("Menu principal :", view=MainMenu())

# ---------------- Run ----------------
bot.run(DISCORD_TOKEN)