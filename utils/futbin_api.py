import aiohttp

# utils/futbin_api.py
import aiohttp

# URL Futbin non officielle (FIFA 24)
API_URL = "https://www.futbin.com/24/playerPrices?player={}"

async def get_player_price(player_id: int, platform: str = "ps") -> int | None:
    """
    Récupère le prix moyen d'un joueur sur FUTBIN pour la plateforme spécifiée.
    
    :param player_id: ID Futbin du joueur
    :param platform: 'ps', 'xbox' ou 'pc'
    :return: Prix en crédits, ou None si impossible de récupérer
    """
    platform = platform.lower()
    if platform not in ("ps", "xbox", "pc"):
        platform = "ps"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL.format(player_id)) as response:
                if response.status != 200:
                    print(f"Futbin API error: Status {response.status}")
                    return None

                data = await response.json()
                player_data = data.get(str(player_id))
                if not player_data:
                    print(f"Futbin API error: Joueur {player_id} non trouvé")
                    return None

                prices = player_data.get("prices", {})
                platform_info = prices.get(platform, {})
                lc_price = platform_info.get("LCPrice")

                if not lc_price:
                    print(f"Futbin API error: Prix LC non disponible pour {player_id} sur {platform}")
                    return None

                # Convertit "100,000" → 100000
                return int(lc_price.replace(",", ""))
    except Exception as e:
        print(f"Exception get_player_price({player_id}): {e}")
        return None
