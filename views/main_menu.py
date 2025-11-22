import discord
from discord.ui import View, Button
from cogs.watchlist import Watchlist
from cogs.alerts import Alerts
from cogs.forecast_ai import ForecastAI
from cogs.market import Market

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    # --- Prix ---
    @discord.ui.button(label="📊 Prix", style=discord.ButtonStyle.green, custom_id="menu_price")
    async def price_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(PlayerSearchModal())

    # --- Watchlist ---
    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.blurple, custom_id="menu_watchlist")
    async def watchlist_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(WatchlistModal())

    # --- Prédictions IA ---
    @discord.ui.button(label="📈 Prédictions", style=discord.ButtonStyle.grey, custom_id="menu_predict")
    async def predict_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(PredictModal())

    # --- Alertes ---
    @discord.ui.button(label="🔔 Alertes", style=discord.ButtonStyle.red, custom_id="menu_alert")
    async def alert_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(AlertModal())


# --- Modals ---

class PlayerSearchModal(discord.ui.Modal, title="Recherche Joueur"):
    player_name = discord.ui.TextInput(
        label="Nom du joueur",
        placeholder="Ex: Mbappé",
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        market_cog = interaction.client.get_cog("Market")
        if market_cog:
            await market_cog.price(interaction, self.player_name.value)
        else:
            await interaction.response.send_message("❌ Cog Market non trouvé.", ephemeral=True)


class WatchlistModal(discord.ui.Modal, title="Ajouter un joueur à la Watchlist"):
    player_name = discord.ui.TextInput(
        label="Nom du joueur",
        placeholder="Ex: Mbappé",
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        watchlist_cog = interaction.client.get_cog("Watchlist")
        if watchlist_cog:
            await watchlist_cog.watch_add(interaction, self.player_name.value)
        else:
            await interaction.response.send_message("❌ Cog Watchlist non trouvé.", ephemeral=True)


class PredictModal(discord.ui.Modal, title="Prédiction IA"):
    player_name = discord.ui.TextInput(
        label="Nom du joueur",
        placeholder="Ex: Mbappé",
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        ai_cog = interaction.client.get_cog("ForecastAI")
        if ai_cog:
            await ai_cog.predict(interaction, self.player_name.value)
        else:
            await interaction.response.send_message("❌ Cog ForecastAI non trouvé.", ephemeral=True)


class AlertModal(discord.ui.Modal, title="Créer une alerte"):
    player_name = discord.ui.TextInput(
        label="Nom du joueur",
        placeholder="Ex: Mbappé",
        max_length=50
    )
    target_price = discord.ui.TextInput(
        label="Prix cible",
        placeholder="Ex: 100000",
        max_length=20
    )
    direction = discord.ui.TextInput(
        label="Direction (up/down)",
        placeholder="up ou down",
        max_length=5
    )

    async def on_submit(self, interaction: discord.Interaction):
        alert_cog = interaction.client.get_cog("Alerts")
        if alert_cog:
            await alert_cog.alert(
                interaction,
                self.player_name.value,
                int(self.target_price.value),
                self.direction.value
            )
        else:
            await interaction.response.send_message("❌ Cog Alerts non trouvé.", ephemeral=True)
