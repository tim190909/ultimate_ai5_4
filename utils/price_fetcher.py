import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.futwiz.com/fc26/player/"

async def search_player(name: str) -> str | None:
    """
    Recherche un joueur sur Futwiz par nom et retourne le slug.
    Exemple : "Harry Kane" → "harry-kane"
    """
    name_slug = name.lower().replace(" ", "-")
    url = BASE_URL + name_slug + "/"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return name_slug
                return None
    except Exception as e:
        print(f"Erreur search_player({name}): {e}")
        return None

async def get_player_price(player_slug: str, platform: str = "ps") -> int | None:
    """
    Récupère le prix du joueur depuis Futwiz.
    :param player_slug: slug du joueur (ex: "harry-kane")
    :param platform: "ps", "xbox", "pc"
    :return: prix en crédits ou None
    """
    url = BASE_URL + f"{player_slug}/"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Exemple : récupérer prix PS depuis la page
                price_tag = soup.select_one(".price-box .ps .price") # À adapter si HTML change
                if not price_tag:
                    return None
                price_text = price_tag.text.strip().replace(",", "").replace("€", "")
                return int(price_text)
    except Exception as e:
        print(f"Erreur get_player_price({player_slug}): {e}")
        return None
