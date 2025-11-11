import aiohttp

async def get_player_price(player_id, platform="ps"):
    url = f"https://www.futbin.com/24/playerPrices?player={player_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data.get(str(player_id), {}).get("prices", {}).get(platform, {}).get("LCPrice", "N/A")