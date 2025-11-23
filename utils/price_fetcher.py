import aiohttp
from bs4 import BeautifulSoup

BASE_SEARCH_URL = "https://www.futwiz.com/en/fc26/players/search?name="
BASE_PLAYER_URL = "https://www.futwiz.com/en/fc26/player/"


async def search_player(name: str):
    """Recherche un joueur par son nom sur Futwiz FC26 et retourne son slug/id."""
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_SEARCH_URL + name.replace(" ", "+")) as response:
            if response.status != 200:
                return None

            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Futwiz met les résultats dans un tableau .searchTable
            table = soup.find("table", class_="searchTable")
            if not table:
                return None

            # Le premier résultat suffit
            first = table.find("a")
            if not first:
                return None

            # Lien exemple :
            # /en/fc26/player/harry-kane/20266
            href = first.get("href")

            if "/player/" not in href:
                return None

            # On récupère juste le slug complet : harry-kane/20266
            slug = href.split("/player/")[1]
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
