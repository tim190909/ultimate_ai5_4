# utils/futwiz_api.py
import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.futwiz.com/en/fifa24/player/{player_id}"

async def get_player_price(player_id: int) -> int | None:
    """
    Récupère le prix moyen d’un joueur depuis Futwiz.
    :param player_id: ID Futwiz du joueur
    :return: Prix moyen en crédits, ou None si erreur
    """
    url = BASE_URL.format(player_id=player_id)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"Futwiz API error: Status {resp.status}")
                    return None

                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")

                # Exemple : récupère le prix PS dans un span spécifique
                price_span = soup.find("span", class_="price")
                if not price_span:
                    print(f"Futwiz: prix non trouvé pour {player_id}")
                    return None

                price_text = price_span.text.strip().replace(",", "").replace("€", "")
                return int(price_text)
    except Exception as e:
        print(f"Exception get_player_price({player_id}): {e}")
        return None
