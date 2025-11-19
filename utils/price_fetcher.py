# utils/price_fetcher.py
import aiohttp
import asyncio

# API endpoints
FUTAPI_URL = "https://futapi.io/api/players/{player_id}"
FUTDB_URL = "https://api.futdb.app/24/player/{player_id}"

# Tes clés d'API à mettre dans les variables d'environnement
import os
FUTAPI_KEY = os.getenv("FUTAPI_KEY") # FutAPI
FUTDB_KEY = os.getenv("FUTDB_KEY") # FutDB

async def fetch_futapi_price(player_id: int, platform: str = "ps") -> int | None:
    """Récupère le prix via FutAPI."""
    if not FUTAPI_KEY:
        return None

    headers = {"X-AUTH-TOKEN": FUTAPI_KEY}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FUTAPI_URL.format(player_id=player_id), headers=headers) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                price = data.get("prices", {}).get(platform, {}).get("LCPrice")
                if price:
                    return int(str(price).replace(",", ""))
    except Exception:
        return None
    return None

async def fetch_futdb_price(player_id: int, platform: str = "ps") -> int | None:
    """Récupère le prix via FutDB."""
    if not FUTDB_KEY:
        return None

    headers = {"X-API-KEY": FUTDB_KEY}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FUTDB_URL.format(player_id=player_id), headers=headers) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                price = data.get("prices", {}).get(platform, {}).get("LCPrice")
                if price:
                    return int(str(price).replace(",", ""))
    except Exception:
        return None
    return None

async def get_player_price(player_id: int, platform: str = "ps") -> int | None:
    """
    Récupère le prix le plus récent possible en combinant FutAPI et FutDB.
    Priorité à FutAPI.
    """
    price = await fetch_futapi_price(player_id, platform)
    if price is not None:
        return price

    # Si FutAPI échoue, fallback sur FutDB
    price = await fetch_futdb_price(player_id, platform)
    return price
