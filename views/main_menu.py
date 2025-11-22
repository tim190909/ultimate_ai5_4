import discord
from discord.ui import View, Button
from cogs.market import Market
from cogs.watchlist import Watchlist
from cogs.alerts import Alerts
from cogs.forecast_ai import ForecastAI

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    # Bouton Prix
    @discord.ui.button(label="📊 Prix", style=discord.ButtonStyle.green, custom_id="menu_price")
    async def price_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            "💰 Utilise la commande : `/price player_id:`",
            ephemeral=True
        )

    # Bouton Watchlist
    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.blurple, custom_id="menu_watchlist")
    async def watchlist_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            "⭐ Utilise la commande : `/watchlist`",
            ephemeral=True
        )

    # Bouton Prédictions
    @discord.ui.button(label="📈 Prédictions", style=discord.ButtonStyle.grey, custom_id="menu_predict")
    async def predict_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            "📈 Fonction complète bientôt",
            ephemeral=True
        )

    # Bouton Alertes
    @discord.ui.button(label="🔔 Alertes", style=discord.ButtonStyle.red, custom_id="menu_alert")
    async def alert_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            "🔔 Fonction complète bientôt",
            ephemeral=True
        )
