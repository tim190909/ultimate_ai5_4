import discord
from discord.ext import commands
from db.models import execute, fetch_all
from utils.price_fetcher import search_player, get_player_price

class Watchlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="watch_add", description="Ajouter un joueur à ta watchlist")
    async def watch_add(self, interaction: discord.Interaction, player_name: str):
        await interaction.response.defer()
        results = await search_player(player_name)

        if not results:
            await interaction.followup.send("❌ Joueur introuvable.", ephemeral=True)
            return

        player = results[0]
        await execute(
            "INSERT OR IGNORE INTO watchlist (user_id, player_id) VALUES (?, ?)",
            (str(interaction.user.id), player["id"])
        )
        await interaction.followup.send(f"⭐ Joueur `{player['name']}` ajouté à ta watchlist !", ephemeral=True)

    @discord.app_commands.command(name="watchlist", description="Voir ta watchlist")
    async def watchlist(self, interaction: discord.Interaction):
        await interaction.response.defer()
        rows = await fetch_all(
            "SELECT player_id FROM watchlist WHERE user_id = ?",
            (str(interaction.user.id),)
        )

        if not rows:
            await interaction.followup.send("❌ Ta watchlist est vide.", ephemeral=True)
            return

        content = []
        for r in rows:
            price = await get_player_price(r["player_id"])
            content.append(f"- ID {r['player_id']} : {'N/A' if price is None else f'{price} crédits'}")

        await interaction.followup.send(f"📘 **Ta watchlist :**\n" + "\n".join(content), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Watchlist(bot))
