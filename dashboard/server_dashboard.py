from discord import Embed

async def server_dashboard(guild):
    embed = Embed(title=f"Dashboard du serveur {guild.name}")
    embed.add_field(name="Top Joueurs", value="Ex: Joueur A, Joueur B", inline=False)
    embed.add_field(name="Top SBC", value="Ex: TOTW Pack, Icon SBC", inline=False)
    embed.add_field(name="Alertes récentes", value="3 alertes cette semaine", inline=False)
    return embed