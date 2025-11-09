import discord
from discord.ui import View, Button, Modal, TextInput
from futbin.scraper import fetch_popular_players, fetch_player_image
from analysis.scorer import compute_score
from sbc.optimizer import optimize_sbc
from gamification.mini_games import mini_game_guess_price

class MainMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📈 Recommandations", style=discord.ButtonStyle.green, custom_id="btn_recommend")
    async def recommend_button(self, button: Button, interaction: discord.Interaction):
        await interaction.response.defer()
        players = await fetch_popular_players("ps")
        for p in players[:5]:
            hist = [10000,10500,11000,10750,10800,11200,11500] # Remplacer par DB
            prices = hist
            future_upgrade = False
            score_data = compute_score(prices, future_upgrade=future_upgrade)
            img_url = await fetch_player_image(p["id"])
            if score_data and img_url:
                embed = discord.Embed(
                    title=f"{p['name']} ({p['platform']})",
                    description=f"Score: {score_data['score']:.2f}\nRisque: {score_data['risk']}\nPrix net: {int(score_data['net_price'])}\n"
                                f"{'🚀 Future upgrade prévue!' if score_data['future_upgrade'] else ''}",
                    color=discord.Color.green()
                )
                embed.set_image(url=img_url)
                await interaction.followup.send(embed=embed)

    @discord.ui.button(label="⭐ Mini-Jeu", style=discord.ButtonStyle.blurple, custom_id="btn_minigame")
    async def minigame_button(self, button: Button, interaction: discord.Interaction):
        await interaction.response.defer()
        result = await mini_game_guess_price(str(interaction.user.id), real_price=15000)
        await interaction.followup.send(result)

    @discord.ui.button(label="🧩 SBC Optimale", style=discord.ButtonStyle.primary, custom_id="btn_sbc")
    async def sbc_button(self, button: Button, interaction: discord.Interaction):
        await interaction.response.send_modal(SBCModal())

class SBCModal(Modal):
    sbc_name = TextInput(label="Nom du SBC", placeholder="Ex: TOTW Pack")

    async def on_submit(self, interaction: discord.Interaction):
        result = await optimize_sbc(self.sbc_name.value)
        await interaction.response.send_message(result)
	
