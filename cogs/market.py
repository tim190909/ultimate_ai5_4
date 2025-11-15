import discord
from discord.ext import commands
from utils.futbin_api import get_player_price

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="price",
        description="Voir le prix FUTBIN d’un joueur (ID)"
    )
    async def price(self, interaction: discord.Interaction, futbin_id: int):
        price = await get_player_price(futbin_id)

        if price is None:
            await interaction.response.send_message(
                "❌ Impossible de récupérer le prix.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"Prix du joueur {futbin_id}",
            description=f"💰 **{price} crédits**",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Market(bot))
