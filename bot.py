import discord
from discord.ext import commands
import os
import asyncio

from config import DISCORD_TOKEN
from db.database import init_db
from cogs.menu import Menu # Pour charger /menu

INTENTS = discord.Intents.default()
INTENTS.message_content = True

class FutBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=INTENTS,
            description="FUT Trading Bot – Version 41.0"
        )

    async def setup_hook(self):
        # 🔌 Initialisation base de données
        await init_db()
        print("✅ Base de données initialisée.")

        # 📚 Chargement automatique des COGS
        COGS = [
            "cogs.menu",
            "cogs.market",
            "cogs.watchlist",
            "cogs.alerts",
            "cogs.forecast_ai"
        ]
        for cog in COGS:
            try:
                await self.load_extension(cog)
                print(f"✔️ Cog chargé : {cog}")
            except Exception as e:
                print(f"❌ Erreur chargement {cog} : {e}")

        # 🔁 Synchronisation slash commands
        try:
            await self.tree.sync()
            print("✨ Commandes slash synchronisées !")
        except Exception as e:
            print("❌ Erreur synchronisation slash:", e)

        # ⚡ Affichage du menu principal automatiquement
        self.add_view(Menu()) # Permet que MainMenu soit actif sans interaction préalable

# ---------------- RUN BOT ----------------
bot = FutBot()

@bot.event
async def on_ready():
    print(f"🤖 Bot connecté : {bot.user}")
    print("🚀 Version 41.0 démarrée avec succès !")

bot.run(DISCORD_TOKEN)
