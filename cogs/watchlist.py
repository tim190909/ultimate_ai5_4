import discord
from discord.ext import commands
from db.models import execute, fetch_all

class Watchlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="watch_add", description="Ajouter un joueur à ta watchlist")
    async def watch_add(self, interaction, player_id: int):
        await execute(
            "INSERT OR IGNORE INTO watchlist (user_id, player_id) VALUES (?, ?)",
            (str(interaction.user.id), player_id)
        )
        await interaction.response.send_message(
            f"⭐ Joueur `{player_id}` ajouté à ta watchlist !",
            ephemeral=True
        )

    @discord.app_commands.command(name="watchlist", description="Voir ta watchlist")
    async def watchlist(self, interaction):
        rows = await fetch_all(
            "SELECT player_id FROM watchlist WHERE user_id = ?",
            (str(interaction.user.id),)
        )

        if not rows:
            await interaction.response.send_message("❌ Ta watchlist est vide.", ephemeral=True)
            return

        content = "\n".join([f"- `{r['player_id']}`" for r in rows])
        await interaction.response.send_message(
            f"📘 **Ta watchlist :**\n{content}",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Watchlist(bot))
