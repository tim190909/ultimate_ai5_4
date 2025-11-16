import discord
from discord.ext import commands
from utils.ai_predictor import predict_player_price

class ForecastAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="predict", description="Prédiction IA du prix d’un joueur")
    async def predict(self, interaction: discord.Interaction, futbin_id: int):
        price = await predict_player_price(futbin_id)
        await interaction.response.send_message(f"📈 Prévision IA pour {futbin_id} : {price} crédits", ephemeral=True)

    # Méthode pour MainMenu
    async def predict_price(self, interaction: discord.Interaction):
        await interaction.response.send_message("📈 Prédiction IA – Fonction complète bientôt", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ForecastAI(bot))

