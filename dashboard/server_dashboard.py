def get_server_stats(guild):
    return {
        "Nom": guild.name,
        "Membres": guild.member_count,
        "Salons": len(guild.text_channels),
        "ID": guild.id
    }