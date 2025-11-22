# utils/price_fetcher.py
import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.futwiz.com/fc26"

async def search_player(name: str) -> str | None:
    """
    Recherche le joueur sur Futwiz FC26 et retourne son slug pour l'URL.
    :param name: Nom du joueur (ex: "Harry Kane")
    :return: slug (ex: "harry-kane/20266") ou None si introuvable
    """
    try:
        async with aiohttp.ClientSession() as session:
            search_url = f"{BASE_URL}/search?term={name.replace(' ', '+')}"
            async with session.get(search_url) as resp:
                if resp.status != 200:
                    print(f"Futwiz search error: status {resp.status}")
                    return None

                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                link = soup.select_one("a[href*='/fc26/player/']")
                if link:
                    # extrait le slug après /fc26/player/
                    slug = link['href'].split("/fc26/player/")[1].rstrip("/")
                    return slug
                return None
    except Exception as e:
        print(f"search_player error: {e}")
        return None


async def get_player_price(slug: str, platform: str = "ps") -> int | None:
    """
    Récupère le prix du joueur sur Futwiz FC26.
    :param slug: slug du joueur (ex: harry-kane/20266)
    :param platform: "ps", "xbox" ou "pc"
    :return: prix en crédits ou None
    """
    platform = platform.lower()
    if platform not in ("ps", "xbox", "pc"):
        platform = "ps"

    url = f"{BASE_URL}/player/{slug}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"Futwiz player page error: status {resp.status}")
                    return None

                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")

                # Classe CSS spécifique pour le prix PS/Xbox/PC
                # PS = .pcprice, Xbox = .xboxprice, PC = .pcprice
                price_selector = {
                    "ps": ".pcprice",
                    "xbox": ".xboxprice",
                    "pc": ".pcprice"
                }

                price_tag = soup.select_one(price_selector[platform])
                if not price_tag:
                    print(f"Futwiz price not found for platform {platform}")
                    return None

                price_text = price_tag.text.replace(",", "").replace("€", "").strip()
                return int(price_text)
    except Exception as e:
        print(f"get_player_price error: {e}")
        return None
