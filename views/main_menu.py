import discord
from discord.ui import View, Button
from futbin.scraper import fetch_popular_players, fetch_player_image
from db.models import get_price_history
from analysis.scorer import compute_score
from sbc.optimizer import optimize_sbc

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📈 Recommandations", style=discord.ButtonStyle.green, custom_id="btn_recommend")
    async def recommend_button(self, button: Button, interaction: discord.Interaction):
        players = await fetch_popular_players()
        embeds = []
        for p in players[:5]:
            hist = await get_price_history(p["id"], p["platform"], limit=7)
            prices = [v for v,_ in hist]
            score_data = compute_score(prices)
            img_url = await fetch_player_image(p["id"])
            if score_data and img_url:
                embed = discord.Embed(
                    title=f"{p['name']} ({p['platform']})",
                    description=f"Score: {score_data['score']:.2f}\n"
                                f"Risque: {score_data['risk']}\n"
                                f"Prix net: {int(score_data['net_price'])}",
                    color=discord.Color.green()
                )
                embed.set_image(url=img_url)
                embeds.append(embed)
        if embeds:
            for e in embeds:
                await interaction.followup.send(embed=e)
        else:
            await interaction.followup.send("Pas de recommandations disponibles.")

    @discord.ui.button(label="⭐ Watchlist", style=discord.ButtonStyle.gray, custom_id="btn_watchlist")
    async def watchlist_button(self, button: Button, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        rows = await models.get_user_watchlist(user_id)
        if not rows:
            await interaction.response.send_message("Ta watchlist est vide.", ephemeral=True)
            return
        for player_id, platform in rows:
            hist = await get_price_history(player_id, platform, limit=7)
            prices = [v for v,_ in hist]
            score_data = compute_score(prices)
            img_url = await fetch_player_image(player_id)
            if score_data and img_url:
                embed = discord.Embed(
                    title=f"{player_id} ({platform})",
                    description=f"Score: {score_data['score']:.2f}\n"
                                f"Risque: {score_data['risk']}\n"
                                f"Prix net: {int(score_data['net_price'])}",
                    color=discord.Color.orange()
                )
                embed.set_image(url=img_url)
                await interaction.followup.send(embed=embed)

    @discord.ui.button(label="📊 Top Variations", style=discord.ButtonStyle.blurple, custom_id="btn_top_variations")
    async def top_variations_button(self, button: Button, interaction: discord.Interaction):
        players = await fetch_popular_players()
        stats = []
        for p in players[:10]:
            hist = await get_price_history(p["id"], p["platform"], limit=7)
            prices = [v for v,_ in hist]
            if prices:
                variation = (prices[-1]-prices[0])/prices[0]*100
                stats.append({"name":p["name"], "platform":p["platform"], "variation":variation})
        stats.sort(key=lambda x: x["variation"], reverse=True)
        description = "\n".join([f"{s['name']} ({s['platform']}): {s['variation']:+.2f}%" for s in stats])
        embed = discord.Embed(title="Top 10 Variations", description=description, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="💡 SBC Optimizer", style=discord.ButtonStyle.red, custom_id="btn_sbc")
    async def sbc_button(self, button: Button, interaction: discord.Interaction):
        # Demander le nom du SBC
        await interaction.response.send_modal(optimize_sbc())
