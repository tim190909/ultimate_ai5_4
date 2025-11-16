import discord
from discord.ui import View, Button
from discord.ext import commands

class MainMenu(View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    # 📊 Prix
    @discord.ui.button(label="📊 Prix", style=discord.ButtonStyle.green, custom_id="menu_price")
    async def price_button(self, interaction: discord.Interaction, button: Button):
        market_cog = self.bot.get_cog("Market")
        if market_cog is None:
            await interaction.response.send_message("❌ Cog Market non chargé.", ephemeral=True)
            return
        futbin_id = 12345 # Tu peux le remplacer par une interaction pour demander l'ID
        price = await market_cog.get_price(futbin_id)
        await interaction.response.send_message(f"💰 Prix du joueur {futbin_id} : {price} crédits", ephemeral=True)

    # ⭐ Watchlist
    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.blurple, custom_id="menu_watchlist")
    async def watchlist_button(self, interaction: discord.Interaction, button: Button):
        watchlist_cog = self.bot.get_cog("Watchlist")
        if watchlist_cog is None:
            await interaction.response.send_message("❌ Cog Watchlist non chargé.", ephemeral=True)
            return
        await watchlist_cog.send_watchlist(interaction)

    # 📈 Prédictions IA
    @discord.ui.button(label="📈 Prédictions", style=discord.ButtonStyle.grey, custom_id="menu_predict")
    async def predict_button(self, interaction: discord.Interaction, button: Button):
        forecast_cog = self.bot.get_cog("ForecastAI")
        if forecast_cog is None:
            await interaction.response.send_message("❌ Cog ForecastAI non chargé.", ephemeral=True)
            return
        futbin_id = 12345 # Idem, à remplacer par la sélection de l'utilisateur
        prediction = await forecast_cog.predict_price(futbin_id)
        await interaction.response.send_message(f"📈 Prévision IA pour {futbin_id} : {prediction} crédits", ephemeral=True)

    # 🔔 Alertes
    @discord.ui.button(label="🔔 Alertes", style=discord.ButtonStyle.red, custom_id="menu_alert")
    async def alert_button(self, interaction: discord.Interaction, button: Button):
        alerts_cog = self.bot.get_cog("Alerts")
        if alerts_cog is None:
            await interaction.response.send_message("❌ Cog Alerts non chargé.", ephemeral=True)
            return
        await alerts_cog.manage_alerts(interaction)
