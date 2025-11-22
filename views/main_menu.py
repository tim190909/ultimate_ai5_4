import discord

class MainMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    # ---- BOUTON PRIX ----
    @discord.ui.button(label="💰 Prix", style=discord.ButtonStyle.primary, row=0)
    async def price_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Appelle la commande /price
        command = interaction.client.tree.get_command("price")
        if command is None:
            return await interaction.response.send_message(
                "❌ Commande prix introuvable.", ephemeral=True
            )

        await interaction.response.send_message(
            "🟦 Utilise la commande : `/price player_id:`",
            ephemeral=True
        )

    # ---- BOUTON WATCHLIST ----
    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.primary, row=0)
    async def watchlist_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        command = interaction.client.tree.get_command("watchlist")
        if command is None:
            return await interaction.response.send_message(
                "❌ Watchlist n'est pas encore configuré.",
                ephemeral=True
            )

        await interaction.response.send_message(
            "⭐ Utilise la commande : `/watchlist add` ou `/watchlist view`",
            ephemeral=True
        )

    # ---- BOUTON PRÉDICTIONS ----
    @discord.ui.button(label="📈 Prédictions", style=discord.ButtonStyle.success, row=1)
    async def predictions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "📉 Fonction Prédictions : bientôt disponible.",
            ephemeral=True
        )

    # ---- BOUTON ALERTS ----
    @discord.ui.button(label="🔔 Alerts", style=discord.ButtonStyle.danger, row=1)
    async def alerts_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "🔔 Alerts automatiques arrivent bientôt 🚀",
            ephemeral=True
        )
