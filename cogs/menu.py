# cogs/menu.py
import discord
from discord.ext import commands
from views.main_menu import MainMenu # ton MainMenu avec les 4 boutons

class Menu(commands.Cog):
    """Cog pour la commande /menu qui ouvre le menu principal"""

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="menu", description="Ouvre le menu principal")
    async def menu(self, interaction: discord.Interaction):
        """Commande slash /menu"""
        await interaction.response.send_message(
            "📌 **Menu principal :**",
            view=MainMenu(),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Menu(bot))
