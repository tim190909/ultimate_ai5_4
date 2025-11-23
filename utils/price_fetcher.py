import aiohttp
from bs4 import BeautifulSoup

BASE_SEARCH_URL = "https://www.futwiz.com/en/fc26/players/search?name="
BASE_PLAYER_URL = "https://www.futwiz.com/en/fc26/player/"

async def search_player(name: str):
    import aiohttp
    from bs4 import BeautifulSoup

    url = BASE_SEARCH_URL + name.replace(" ", "+")
    print(f"[DEBUG] Recherche URL : {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"[DEBUG] Status : {response.status}")

            html = await response.text()

            # On affiche les 2000 premiers caractères pour analyse
            print("\n\n===== DEBUG FUTWIZ HTML (DÉBUT) =====")
            print(html[:2000])
            print("===== DEBUG FUTWIZ HTML (FIN) =====\n\n")

            if response.status != 200:
                print("[DEBUG] Mauvais HTTP status")
                return None

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
