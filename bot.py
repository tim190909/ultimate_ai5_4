import discord
from discord.ext import commands
from views.main_menu import MainMenu
from db import models
from tasks.scheduler import start_tasks
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, description="ULTIMATE AI 5.4")

@bot.event
async def on_ready():
    await models.init_db()
    await bot.tree.sync()
    start_tasks(bot)
    print(f"Bot connecté : {bot.user}")

# Commande slash pour le menu principal
@bot.tree.command(name="menu", description="Ouvre le menu principal")
async def menu(interaction: discord.Interaction):
    await interaction.response.send_message("Menu principal :", view=MainMenu())

bot.run(DISCORD_TOKEN)