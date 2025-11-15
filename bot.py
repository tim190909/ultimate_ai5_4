import discord
from discord.ext import commands
import os
import asyncio

TOKEN = os.environ.get("DISCORD_TOKEN")

class FutBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True # nécessaire pour lire les messages

        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=os.environ.get("APPLICATION_ID") # pour Render
        )

    async def setup_hook(self):
        # Charge automatiquement tous les cogs
        for folder in ("cogs",):
            for file in os.listdir(folder):
                if file.endswith(".py"):
                    await self.load_extension(f"{folder}.{file[:-3]}")
        print("📦 Cogs chargés !")

        # Synchronisation slash commands
        try:
            await self.tree.sync()
            print("✨ Slash commands synchronisées !")
        except Exception as e:
            print("❌ Erreur sync :", e)

bot = FutBot()

@bot.event
async def on_ready():
    print(f"🤖 Bot connecté : {bot.user}")

def run():
    bot.run(TOKEN)
