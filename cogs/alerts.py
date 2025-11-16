import discord
from discord.ext import commands
from db.models import execute

class Alerts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="alert", description="Créer une alerte de prix")
    async def alert(self, interaction: discord.Interaction, player_id: int, target_price: int, direction: str):
        if direction.lower() not in ("up", "down"):
            await interaction.response.send_message("❌ Direction invalide. Choisis `up` ou `down`.", ephemeral=True)
            return
        await execute(
            "INSERT INTO alerts (user_id, player_id, target_price, direction) VALUES (?, ?, ?, ?)",
            (str(interaction.user.id), player_id, target_price, direction)
        )
        await interaction.response.send_message(f"🔔 Alerte pour {player_id} à {target_price} ({direction})", ephemeral=True)

    async def manage_alerts(self, interaction: discord.Interaction):
        await interaction.response.send_message("🔔 Gestion des alertes – Fonction complète bientôt", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Alerts(bot))

