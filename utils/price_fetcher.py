# utils/price_fetcher.py
import aiohttp
from bs4 import BeautifulSoup
import os

BASE_SEARCH_URL = "https://www.futwiz.com/en/fc26/players/search?name="
BASE_PLAYER_URL = "https://www.futwiz.com/en/fc26/player/"

async def search_player(name: str):
    url = BASE_SEARCH_URL + name.replace(" ", "+")
    print(f"[DEBUG] Recherche URL : {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"[DEBUG] Status : {response.status}")

            if response.status != 200:
                print("[DEBUG] Mauvais status")
                return None

            html = await response.text()

            # Crée le dossier logs s'il n'existe pas
            os.makedirs("logs", exist_ok=True)

            # Sauvegarde du HTML pour debug
            debug_path = os.path.join("logs", "debug_futwiz.html")
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"[DEBUG] HTML sauvegardé dans {debug_path}")

            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", class_="searchTable")
            print(f"[DEBUG] searchTable trouvée ? {table is not None}")

            if not table:
                return None

            first = table.find("a")
            print(f"[DEBUG] Premier lien trouvé : {first}")

            if not first:
                return None

            href = first.get("href")
            print(f"[DEBUG] href = {href}")

            if "/player/" not in href:
                return None

            slug = href.split("/player/")[1]
            print(f"[DEBUG] SLUG FINAL = {slug}")

            return slug

async def get_player_price(slug: str):
    """Scrape Futwiz FC26 pour récupérer un prix."""
    url = BASE_PLAYER_URL + slug

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None

            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Futwiz FC26 affiche le prix dans un bloc ".playerprices"
            price_box = soup.find("div", class_="playerprices")
            if not price_box:
                return None

            price = price_box.find("span", class_="price-num")
            if not price:
                return None

            return price.text.strip()
