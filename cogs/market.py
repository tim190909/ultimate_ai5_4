# cogs/market.py
import discord
from discord.ext import commands
from utils.futwiz_api import get_player_price

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="price",
        description="Voir le prix Futwiz d’un joueur (ID)"
    )
    async def price(self, interaction: discord.Interaction, futwiz_id: int):
        # Appelle la fonction Futwiz
        price = await get_player_price(futwiz_id)

        if price is None:
            await interaction.response.send_message(
                "❌ Impossible de récupérer le prix sur Futwiz.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"Prix du joueur {futwiz_id}",
            description=f"💰 **{price} crédits**",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Market(bot))
