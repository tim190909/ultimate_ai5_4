# utils/price_fetcher.py
import aiohttp

# URL Futwiz FIFA 26 (non officielle)
API_URL = "https://www.futwiz.com/fc26/player/{player_id}"

async def get_player_price(player_id: int, platform: str = "ps") -> int | None:
    """
    Récupère le prix d'un joueur depuis Futwiz pour la plateforme choisie.
    
    :param player_id: ID Futwiz du joueur
    :param platform: 'ps', 'xbox' ou 'pc'
    :return: Prix en crédits ou None si impossible de récupérer
    """
    platform = platform.lower()
    if platform not in ("ps", "xbox", "pc"):
        platform = "ps"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL.format(player_id)) as response:
                if response.status != 200:
                    print(f"Futwiz API error: Status {response.status}")
                    return None

                data = await response.json()

                # Futwiz retourne un dict avec l'ID du joueur comme clé
                player_data = data.get(str(player_id))
                if not player_data:
                    print(f"Futwiz API error: Joueur {player_id} non trouvé")
                    return None

                prices = player_data.get("prices", {})
                platform_info = prices.get(platform, {})
                lc_price = platform_info.get("LCPrice")

                if not lc_price:
                    print(f"Futwiz API error: Prix LC non disponible pour {player_id} sur {platform}")
                    return None

                # Convertit "100,000" → 100000
                return int(lc_price.replace(",", ""))
    except Exception as e:
        print(f"Exception get_player_price({player_id}): {e}")
        return None

