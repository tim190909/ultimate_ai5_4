# utils/price_fetcher.py
import aiohttp
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.futwiz.com/fc26"

async def get_player_price(player_id: int) -> int | None:
    url = f"{BASE_URL}/player/{player_id}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                if resp.status != 200:
                    print(f"Futwiz fetch error: Status {resp.status}")
                    return None
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                
                # Recherche du prix (exemple basé sur l'ancienne classe)
                price_div = soup.find("div", class_="player-prices")  
                if not price_div:
                    print("Futwiz fetch error: prix non trouvé")
                    return None
                price_text = re.sub(r"[^\d]", "", price_div.get_text())
                return int(price_text)
    except Exception as e:
        print(f"Exception get_player_price({player_id}): {e}")
        return None

async def search_player(name: str) -> int | None:
    """
    Recherche un joueur par nom et retourne son ID Futwiz
    """
    url = f"{BASE_URL}/search?query={name.replace(' ', '+')}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                if resp.status != 200:
                    print(f"Futwiz search error: Status {resp.status}")
                    return None
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                
                # Cherche le premier lien joueur
                player_link = soup.find("a", href=re.compile(r"/player/\d+"))
                if not player_link:
                    print("Futwiz search error: joueur non trouvé")
                    return None
                # Extrait l'ID du lien /player/12345
                player_id = int(player_link['href'].split('/')[-1])
                return player_id
    except Exception as e:
        print(f"Exception search_player({name}): {e}")
        return None
