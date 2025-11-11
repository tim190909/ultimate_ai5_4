import discord
from discord.ui import View, Button

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📈 Recommandations", style=discord.ButtonStyle.green)
    async def recommend(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("📊 Fonction 'Recommandations' à venir...", ephemeral=True)

    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.gray)
    async def watchlist(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("👀 Fonction 'Watchlist' à venir...", ephemeral=True)

    @discord.ui.button(label="📊 Top Variations", style=discord.ButtonStyle.blurple)
    async def top_var(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("💹 Fonction 'Top Variations' à venir...", ephemeral=True)

    @discord.ui.button(label="💡 SBC Optimizer", style=discord.ButtonStyle.red)
    async def sbc(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("⚙️ Fonction 'SBC Optimizer' à venir...", ephemeral=True)
