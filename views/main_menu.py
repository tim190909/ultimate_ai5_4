import discord
from discord.ui import View, Button
from utils.price_fetcher import get_player_price
from db.models import fetch_all

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    # Bouton Prix
    @discord.ui.button(label="📊 Prix", style=discord.ButtonStyle.green, custom_id="menu_price")
    async def price_button(self, interaction: discord.Interaction, button: Button):
        # Affiche un modal pour entrer l'ID du joueur
        await interaction.response.send_modal(PlayerIdModal())

    # Bouton Watchlist
    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.blurple, custom_id="menu_watchlist")
    async def watchlist_button(self, interaction: discord.Interaction, button: Button):
        # Récupère la watchlist de l'utilisateur
        rows = await fetch_all(
            "SELECT player_id FROM watchlist WHERE user_id = ?",
            (str(interaction.user.id),)
        )

        if not rows:
            await interaction.response.send_message("❌ Ta watchlist est vide.", ephemeral=True)
            return

        messages = []
        for r in rows:
            price = await get_player_price(r["player_id"])
            if price:
                messages.append(f"ID {r['player_id']}: 💰 {price} crédits")
            else:
                messages.append(f"ID {r['player_id']}: ❌ Impossible de récupérer le prix")

        await interaction.response.send_message("📘 **Ta watchlist :**\n" + "\n".join(messages), ephemeral=True)

    # Bouton Prédictions IA
    @discord.ui.button(label="📈 Prédictions", style=discord.ButtonStyle.grey, custom_id="menu_predict")
    async def predict_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("📈 *Fonction prédiction IA bientôt disponible*", ephemeral=True)

    # Bouton Alertes
    @discord.ui.button(label="🔔 Alertes", style=discord.ButtonStyle.red, custom_id="menu_alert")
    async def alert_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔔 *Gestion des alertes bientôt disponible*", ephemeral=True)


# Modal pour entrer l'ID du joueur
class PlayerIdModal(discord.ui.Modal, title="Récupérer le prix d'un joueur"):
    player_id = discord.ui.TextInput(label="ID Futwiz du joueur", placeholder="Ex: 123456")

    async def on_submit(self, interaction: discord.Interaction):
        try:
            player_id_int = int(self.player_id.value)
            price = await get_player_price(player_id_int)
            if price:
                await interaction.response.send_message(f"💰 Prix du joueur {player_id_int} : {price} crédits", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ Impossible de récupérer le prix pour {player_id_int}", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ ID invalide.", ephemeral=True)
