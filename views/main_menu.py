import discord
from discord.ext import commands
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
        await interaction.response.defer(ephemeral=True)

        rows = await fetch_all(
            "SELECT player_id FROM watchlist WHERE user_id = ?",
            (str(interaction.user.id),)
        )

        if not rows:
            await interaction.followup.send("❌ Ta watchlist est vide.")
            return

        messages = []
        for r in rows:
            price = await get_player_price(r["player_id"])
            if price:
                messages.append(f"ID {r['player_id']}: 💰 {price} crédits")
            else:
                messages.append(f"ID {r['player_id']}: ❌ Impossible de récupérer le prix")

        await interaction.followup.send("📘 **Ta watchlist :**\n" + "\n".join(messages))


    # Bouton Prédictions IA
    @discord.ui.button(label="📈 Prédictions", style=discord.ButtonStyle.grey, custom_id="menu_predict")
    async def predict_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("📈 *Fonction prédiction IA à venir*", ephemeral=True)

    # Bouton Alertes
    @discord.ui.button(label="🔔 Alertes", style=discord.ButtonStyle.red, custom_id="menu_alert")
    async def alert_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔔 *Gestion des alertes à venir*", ephemeral=True)


class PlayerIdModal(Modal, title="Récupérer le prix d'un joueur"):
    player_name = TextInput(label="Nom du joueur Futwiz", placeholder="Ex: Harry Kane")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        name = self.player_name.value
        slug = await search_player(name)

        if not slug:
            await interaction.followup.send(f"❌ Joueur {name} introuvable.")
            return

        price = await get_player_price(slug)

        if price:
            await interaction.followup.send(f"💰 Prix du joueur {name}: {price} crédits")
        else:
            await interaction.followup.send(f"❌ Impossible de récupérer le prix pour {name}")


class MenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="menu", description="Affiche le menu principal")
    async def menu(self, interaction: discord.Interaction):
        await interaction.response.send_message("📌 **Menu Principal**", view=MainMenu(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(MenuCog(bot))
