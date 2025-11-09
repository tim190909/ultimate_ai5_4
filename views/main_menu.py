import discord
from discord.ui import View, Button, Modal, TextInput
from sbc.optimizer import get_sbc_solution
from futbin.scraper import fetch_popular_players, fetch_player_image, is_future_upgrade
from analysis.scorer import compute_score
from db import models

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📈 Recommandations", style=discord.ButtonStyle.green, custom_id="btn_recommend")
    async def recommend_button(self, button: Button, interaction: discord.Interaction):
        await interaction.response.defer()
        players = await fetch_popular_players("ps")
        embeds = []
        for p in players[:5]:
            hist = await models.get_price_history(p["id"], p["platform"], limit=7)
            prices = [v for v,_ in hist]
            future_upgrade = await is_future_upgrade(p["id"])
            score_data = compute_score(prices, future_upgrade=future_upgrade)
            img_url = await fetch_player_image(p["id"])
            if score_data and img_url:
                embed = discord.Embed(
                    title=f"{p['name']} ({p['platform']})",
                    description=f"Score: {score_data['score']:.2f}\n"
                                f"Risque: {score_data['risk']}\n"
                                f"Prix net: {int(score_data['net_price'])}\n"
                                f"{'🚀 Future upgrade!' if score_data['future_upgrade'] else ''}",
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
        await interaction.response.defer()
        user_id = str(interaction.user.id)
        rows = await models.get_user_watchlist(user_id)
        if not rows:
            await interaction.followup.send("Ta watchlist est vide.")
            return
        for player_id, platform in rows:
            hist = await models.get_price_history(player_id, platform, limit=7)
            prices = [v for v,_ in hist]
            future_upgrade = await is_future_upgrade(player_id)
            score_data = compute_score(prices, future_upgrade=future_upgrade)
            img_url = await fetch_player_image(player_id)
            if score_data and img_url:
                embed = discord.Embed(
                    title=f"{player_id} ({platform})",
                    description=f"Score: {score_data['score']:.2f}\n"
                                f"Risque: {score_data['risk']}\n"
                                f"Prix net: {int(score_data['net_price'])}\n"
                                f"{'🚀 Future upgrade!' if score_data['future_upgrade'] else ''}",
                    color=discord.Color.orange()
                )
                embed.set_image(url=img_url)
                await interaction.followup.send(embed=embed)

    @discord.ui.button(label="📊 Top Variations", style=discord.ButtonStyle.blurple, custom_id="btn_top_variations")
    async def top_variations_button(self, button: Button, interaction: discord.Interaction):
        await interaction.response.defer()
        players = await fetch_popular_players("ps")
        stats = []
        for p in players[:10]:
            hist = await models.get_price_history(p["id"], p["platform"], limit=7)
            prices = [v for v,_ in hist]
            if prices:
                variation = (prices[-1]-prices[0])/prices[0]*100
                stats.append({"name":p["name"], "platform":p["platform"], "variation":variation})
        stats.sort(key=lambda x: x["variation"], reverse=True)
        description = "\n".join([f"{s['name']} ({s['platform']}): {s['variation']:+.2f}%" for s in stats])
        embed = discord.Embed(title="Top 10 Variations", description=description, color=discord.Color.blue())
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="💡 SBC Optimale", style=discord.ButtonStyle.red, custom_id="btn_sbc")
    async def sbc_button(self, button: Button, interaction: discord.Interaction):
        await interaction.response.send_modal(SBCModal())

class SBCModal(Modal, title="Optimisation SBC"):
    sbc_name = TextInput(label="Nom du SBC", placeholder="Ex: League SBC", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        solution = await get_sbc_solution(self.sbc_name.value)
        if solution:
            description = "\n".join([f"{player['name']} ({player['price']} coins)" for player in solution["players"]])
            embed = discord.Embed(
                title=f"Solution SBC: {self.sbc_name.value}",
                description=f"Coût total: {solution['total_cost']} coins\n\n{description}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("SBC introuvable ou erreur.", ephemeral=True)
