import aiohttp
from bs4 import BeautifulSoup

BASE_SEARCH_URL = "https://www.futwiz.com/en/fc26/players/search?name="
BASE_PLAYER_URL = "https://www.futwiz.com/en/fc26/player/"

async def search_player(name: str):
    url = BASE_SEARCH_URL + name.replace(" ", "+")
    print(f"[DEBUG] URL Recherche : {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                print("[DEBUG] Mauvais status")
                return None

            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # 🔥 NOUVEAU SELECTEUR Futwiz FC26
            card = soup.select_one("div.player-card a")
            print(f"[DEBUG] Résultat trouvé : {card}")

            if not card:
                return None

            href = card.get("href")
            print(f"[DEBUG] href = {href}")

            if "/player/" not in href:
                return None

            slug = href.split("/player/")[1]
            print(f"[DEBUG] SLUG FINAL = {slug}")

            return slug


async def get_player_price(slug: str):
    url = BASE_PLAYER_URL + slug

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None

            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # 🔥 Futwiz FC26 : nouveau bloc prix
            box = soup.select_one("div.playerprices span.price-num")
            if not box:
                return None

            return box.text.strip()
