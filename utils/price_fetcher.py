# utils/price_fetcher.py
import aiohttp
from bs4 import BeautifulSoup
import re

BASE_SEARCH_URL = "https://www.futwiz.com/en/fc26/players/search?name="
BASE_PLAYER_URL = "https://www.futwiz.com/en/fc26/player/"

async def search_player(name: str) -> str | None:
    """Cherche le joueur par nom et renvoie le slug Futwiz."""
    url = BASE_SEARCH_URL + name.replace(" ", "+")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Les résultats de recherche FC26 sont maintenant dans des liens <a> avec href "/en/fc26/player/slug"
            player_link = soup.find("a", href=re.compile(r"/en/fc26/player/"))
            if not player_link:
                return None

            href = player_link.get("href")
            slug = href.split("/player/")[1].rstrip("/")
            return slug

async def get_player_price(slug: str) -> str | None:
    """Récupère le prix du joueur depuis Futwiz FC26."""
    url = BASE_PLAYER_URL + slug
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Prix FC26 : dans <div class="playerprices">, span class="price-num"
            price_box = soup.find("div", class_="playerprices")
            if not price_box:
                return None
            price = price_box.find("span", class_="price-num")
            if not price:
                return None
            # Nettoyage du prix : "100,000" → "100000"
            return price.text.strip().replace(",", "")
