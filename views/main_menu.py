# views/main_menu.py
import discord
from discord.ui import View, Button, Modal, TextInput
from utils.price_fetcher import get_player_price, search_player
from db.models import fetch_all

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    # Bouton Prix
    @discord.ui.button(label="📊 Prix", style=discord.ButtonStyle.green, custom_id="menu_price")
    async def price_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(PlayerIdModal())

    # Bouton Watchlist
    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.blurple, custom_id="menu_watchlist")
    async def watchlist_button(self, interaction: discord.Interaction, button: Button):
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
        await interaction.response.send_message("📈 *Fonction prédiction IA à venir*", ephemeral=True)

    # Bouton Alertes
    @discord.ui.button(label="🔔 Alertes", style=discord.ButtonStyle.red, custom_id="menu_alert")
    async def alert_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔔 *Gestion des alertes à venir*", ephemeral=True)


class PlayerIdModal(Modal, title="Récupérer le prix d'un joueur"):
    player_id = TextInput(label="Nom du joueur Futwiz", placeholder="Ex: Harry Kane")

    async def on_submit(self, interaction: discord.Interaction):
        name = self.player_id.value.strip()
        slug = await search_player(name) # recherche le joueur sur Futwiz FC26
        if not slug:
            await interaction.response.send_message(f"❌ Joueur '{name}' introuvable.", ephemeral=True)
            return

        price = await get_player_price(slug)
        if price is not None:
            await interaction.response.send_message(f"💰 Prix du joueur '{name}': {price} crédits", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Impossible de récupérer le prix pour '{name}'", ephemeral=True)
