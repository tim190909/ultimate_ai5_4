import discord
from discord.ui import View, Button

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    # Bouton 1 – Prix
    @discord.ui.button(label="📊 Prix", style=discord.ButtonStyle.green, custom_id="menu_price")
    async def price_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("💰 Fonction prix à venir", ephemeral=True)
        except Exception as e:
            print("Erreur bouton Prix:", e)

    # Bouton 2 – Watchlist
    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.blurple, custom_id="menu_watchlist")
    async def watchlist_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("⭐ Fonction watchlist à venir", ephemeral=True)
        except Exception as e:
            print("Erreur bouton Watchlist:", e)

    # Bouton 3 – Prédictions IA
    @discord.ui.button(label="📈 Prédictions", style=discord.ButtonStyle.gray, custom_id="menu_predict")
    async def predict_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("📈 Fonction prédiction IA à venir", ephemeral=True)
        except Exception as e:
            print("Erreur bouton Prédictions:", e)

    # Bouton 4 – Alertes
    @discord.ui.button(label="🔔 Alertes", style=discord.ButtonStyle.red, custom_id="menu_alert")
    async def alert_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("🔔 Fonction gestion des alertes à venir", ephemeral=True)
        except Exception as e:
            print("Erreur bouton Alertes:", e)

    # Bouton 5 – Top Variations
    @discord.ui.button(label="📊 Top Variations", style=discord.ButtonStyle.primary, custom_id="menu_top_variations")
    async def top_variations_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("📊 Fonction Top Variations à venir", ephemeral=True)
        except Exception as e:
            print("Erreur bouton Top Variations:", e)

    # Bouton 6 – SBC Optimizer
    @discord.ui.button(label="💡 SBC Optimizer", style=discord.ButtonStyle.orange, custom_id="menu_sbc")
    async def sbc_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("💡 Fonction SBC Optimizer à venir", ephemeral=True)
        except Exception as e:
            print("Erreur bouton SBC Optimizer:", e)
