import aiohttp

API_URL = "https://www.futbin.com/24/playerPrices?player={}"

async def get_player_price(player_id: int):
    """
    Récupère le prix moyen d’un joueur sur FUTBIN.
    Retourne None si erreur.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL.format(player_id)) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                info = data.get(str(player_id))

                if not info:
                    return None

                # Prix PS
                price = info["prices"]["ps"]["LCPrice"]
                return int(price.replace(",", ""))
    except Exception as e:
        print(f"❌ Erreur get_player_price: {e}")
        return None
