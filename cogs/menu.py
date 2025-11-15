import discord
from discord.ext import commands
from views.main_menu import MainMenu

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="menu", description="Ouvre le menu principal")
    async def menu(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "📌 **Menu principal :**",
            view=MainMenu(),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Menu(bot))
