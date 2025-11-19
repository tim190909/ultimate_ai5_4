import discord
from discord.ext import commands
from utils.price_fetcher import get_player_price

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commande slash
    @discord.app_commands.command(name="price", description="Voir le prix FUTBIN d’un joueur")
    async def price(self, interaction: discord.Interaction, futbin_id: int):
        price = await get_player_price(futbin_id)
        if price is None:
            await interaction.response.send_message("❌ Impossible de récupérer le prix.", ephemeral=True)
            return
        await interaction.response.send_message(f"💰 Prix du joueur {futbin_id} : {price} crédits", ephemeral=True)

    # Méthode appelée par MainMenu
    async def get_price(self, interaction: discord.Interaction, futbin_id: int):
        price = await get_player_price(futbin_id)
        if price is None:
            await interaction.response.send_message("❌ Impossible de récupérer le prix.", ephemeral=True)
            return
        await interaction.response.send_message(f"💰 Prix du joueur {futbin_id} : {price} crédits", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Market(bot))
