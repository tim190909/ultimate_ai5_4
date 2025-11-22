# utils/price_fetcher.py
import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.futwiz.com/fc26/player/"

async def search_player(player_name: str) -> int | None:
    """
    Recherche un joueur sur Futwiz FC26 et retourne son ID.
    :param player_name: Nom complet du joueur
    :return: ID Futwiz ou None si non trouvé
    """
    try:
        async with aiohttp.ClientSession() as session:
            # On remplace les espaces par des tirets et tout en minuscule pour l'URL
            search_name = player_name.lower().replace(" ", "-")
            url = f"{BASE_URL}{search_name}/"
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"Erreur recherche joueur {player_name}: Status {resp.status}")
                    return None
                text = await resp.text()
                soup = BeautifulSoup(text, "html.parser")
                
                # Futwiz met l'ID dans un script JSON sur la page
                scripts = soup.find_all("script")
                for script in scripts:
                    if "window.playerData" in script.text:
                        text = script.text
                        start = text.find('"id":') + 5
                        end = text.find(',', start)
                        player_id = int(text[start:end])
                        return player_id
        return None
    except Exception as e:
        print(f"Exception search_player({player_name}): {e}")
        return None

async def get_player_price(player_id: int) -> int | None:
    """
    Récupère le prix du joueur via son ID sur Futwiz FC26.
    :param player_id: ID Futwiz du joueur
    :return: Prix en crédits ou None si erreur
    """
    try:
        async with aiohttp.ClientSession() as session:
            # Futwiz fournit les prix via une page JSON
            url = f"https://www.futwiz.com/fc26/playerprices?id={player_id}"
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"Erreur récupération prix ID {player_id}: Status {resp.status}")
                    return None
                data = await resp.json()
                # Exemple simplifié: prix PS
                price = data.get("prices", {}).get("ps", {}).get("LCPrice")
                if price:
                    return int(price.replace(",", ""))
        return None
    except Exception as e:
        print(f"Exception get_player_price({player_id}): {e}")
        return None
