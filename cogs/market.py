import discord
from discord.ext import commands
from utils.price_fetcher import get_player_price, search_player

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="price",
        description="Voir le prix FUTWIZ d’un joueur (FC26)"
    )
    async def price(self, interaction: discord.Interaction, player_name: str):
        await interaction.response.defer()
        results = await search_player(player_name)

        if not results:
            await interaction.followup.send("❌ Joueur introuvable.", ephemeral=True)
            return

        # Si plusieurs résultats, on prend le premier pour simplifier
        player = results[0]
        price = await get_player_price(player["id"])

        if price is None:
            await interaction.followup.send("❌ Impossible de récupérer le prix.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Prix du joueur {player['name']}",
            description=f"💰 **{price} crédits** (FC26)",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Market(bot))
