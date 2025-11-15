import discord

def error_embed(message: str):
    return discord.Embed(
        title="❌ Erreur",
        description=message,
        color=discord.Color.red()
    )

def success_embed(message: str):
    return discord.Embed(
        title="✅ Succès",
        description=message,
        color=discord.Color.green()
    )
