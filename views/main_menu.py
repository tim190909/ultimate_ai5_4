import discord
from discord.ui import View, Button

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None) # Persistance totale des boutons

    # -------------------
    # Bouton 1 : Prix
    # -------------------
    @discord.ui.button(label="📊 Prix", style=discord.ButtonStyle.green, custom_id="menu_price")
    async def price_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("💰 *Fonction prix à venir*", ephemeral=True)

    # -------------------
    # Bouton 2 : Watchlist
    # -------------------
    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.blurple, custom_id="menu_watchlist")
    async def watchlist_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("⭐ *Fonction watchlist à venir*", ephemeral=True)

    # -------------------
    # Bouton 3 : Prédictions IA
    # -------------------
    @discord.ui.button(label="📈 Prédictions", style=discord.ButtonStyle.grey, custom_id="menu_predict")
    async def predict_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("📈 *Fonction prédiction IA à venir*", ephemeral=True)

    # -------------------
    # Bouton 4 : Alertes
    # -------------------
    @discord.ui.button(label="🔔 Alertes", style=discord.ButtonStyle.red, custom_id="menu_alert")
    async def alert_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("🔔 *Gestion des alertes à venir*", ephemeral=True)
