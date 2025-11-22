# utils/price_fetcher.py
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import quote

BASE_URL = "https://www.futwiz.com/fc26"

async def search_player(name: str) -> str | None:
    """
    Transforme le nom du joueur en slug Futwiz FC26.
    Ex: 'Harry Kane' -> 'harry-kane/20266'
    """
    try:
        search_url = f"{BASE_URL}/search?term={quote(name)}"
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                if response.status != 200:
                    print(f"Erreur recherche Futwiz: {response.status}")
                    return None

                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                
                # Futwiz retourne une liste de joueurs dans les liens <a href="/fc26/player/...">
                player_link = soup.find("a", href=lambda x: x and "/fc26/player/" in x)
                if not player_link:
                    return None

                slug = player_link["href"].replace("/fc26/player/", "")
                return slug
    except Exception as e:
        print(f"Exception search_player({name}): {e}")
        return None

async def get_player_price(slug: str) -> int | None:
    """
    Récupère le prix du joueur sur Futwiz FC26 à partir du slug.
    Ex: 'harry-kane/20266'
    """
    try:
        url = f"{BASE_URL}/player/{slug}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Erreur récupération prix: {response.status}")
                    return None

                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")

                # Exemple: le prix est dans un span avec id="price"
                price_span = soup.find("span", {"id": "price"})
                if not price_span:
                    print("Prix non trouvé sur la page")
                    return None

                price_text = price_span.text.strip().replace(",", "").replace("€", "")
                return int(price_text)
    except Exception as e:
        print(f"Exception get_player_price({slug}): {e}")
        return None
