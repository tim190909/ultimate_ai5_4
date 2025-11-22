import aiohttp

API_URL = "https://www.futwiz.com/en/fifa-26/playerPrices?player={}" # FC26

async def get_player_price(player_id: int) -> int | None:
    """
    Récupère le prix moyen d’un joueur depuis Futwiz FC26
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL.format(player_id)) as response:
                if response.status != 200:
                    print(f"Futwiz API error: Status {response.status}")
                    return None
                data = await response.json()
                price_info = data.get("prices", {})
                ps_price = price_info.get("ps", {}).get("LCPrice")
                if ps_price:
                    return int(ps_price.replace(",", ""))
                return None
    except Exception as e:
        print(f"Exception get_player_price({player_id}): {e}")
        return None


async def search_player(name: str) -> list[dict]:
    """
    Recherche un joueur par nom pour FC26
    Retourne une liste de dicts : [{"id":12345,"name":"Mbappé"}]
    """
    SEARCH_URL = f"https://www.futwiz.com/en/fifa-26/searchPlayers?name={name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(SEARCH_URL) as response:
                if response.status != 200:
                    print(f"Search API error: {response.status}")
                    return []
                data = await response.json()
                return [{"id":p["id"], "name":p["name"]} for p in data.get("players", [])]
    except Exception as e:
        print(f"Exception search_player({name}): {e}")
        return []
