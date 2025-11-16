import discord
from discord.ui import View, Button

class MainMenu(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="📊 Prix", style=discord.ButtonStyle.green, custom_id="menu_price")
    async def price_button(self, interaction: discord.Interaction, button: Button):
        market_cog = self.bot.get_cog("Market")
        if market_cog:
            await market_cog.get_price(interaction, futbin_id=12345) # Exemple ID fixe
        else:
            await interaction.response.send_message("❌ Cog Market non chargé.", ephemeral=True)

    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.blurple, custom_id="menu_watchlist")
    async def watchlist_button(self, interaction: discord.Interaction, button: Button):
        watchlist_cog = self.bot.get_cog("Watchlist")
        if watchlist_cog:
            await watchlist_cog.send_watchlist(interaction)
        else:
            await interaction.response.send_message("❌ Cog Watchlist non chargé.", ephemeral=True)

    @discord.ui.button(label="📈 Prédictions", style=discord.ButtonStyle.gray, custom_id="menu_predict")
    async def predict_button(self, interaction: discord.Interaction, button: Button):
        ai_cog = self.bot.get_cog("ForecastAI")
        if ai_cog:
            await ai_cog.predict_price(interaction)
        else:
            await interaction.response.send_message("❌ Cog ForecastAI non chargé.", ephemeral=True)

    @discord.ui.button(label="🔔 Alertes", style=discord.ButtonStyle.red, custom_id="menu_alert")
    async def alert_button(self, interaction: discord.Interaction, button: Button):
        alerts_cog = self.bot.get_cog("Alerts")
        if alerts_cog:
            await alerts_cog.manage_alerts(interaction)
        else:
            await interaction.response.send_message("❌ Cog Alerts non chargé.", ephemeral=True)
