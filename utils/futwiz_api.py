# utils/futwiz_api.py
import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.futwiz.com/en/fc24/player/{}"


async def get_player_prices(player_id: int):
    """
    Récupère les prix PS / Xbox / PC pour un joueur via Futwiz.
    :return: dict { "ps": prix, "xbox": prix, "pc": prix } ou None
    """
    url = BASE_URL.format(player_id)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"[FUTWIZ] Status {response.status}")
                return None

            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            try:
                prices = {
                    "ps": soup.select_one(".ps-price").text.strip(),
                    "xbox": soup.select_one(".xbox-price").text.strip(),
                    "pc": soup.select_one(".pc-price").text.strip(),
                }
                return prices

            except Exception:
                print("[FUTWIZ] Impossible d'extraire les prix")
                return None
