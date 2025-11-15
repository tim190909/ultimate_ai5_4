import discord
from discord.ext import commands
from utils.ai_predictor import predict_player_price

class ForecastAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="predict",
        description="Prédiction IA du prix d’un joueur"
    )
    async def predict(self, interaction, futbin_id: int):
        price = await predict_player_price(futbin_id)

        if price is None:
            await interaction.response.send_message(
                "❌ Pas de données disponibles pour prédire.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"Prédiction IA – Joueur {futbin_id}",
            description=f"📈 Prévision : **{price} crédits**",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ForecastAI(bot))
