import os, json, aiohttp
from bs4 import BeautifulSoup
from datetime import datetime as dt, timedelta
from config import CACHE_FILE, CACHE_TTL_HOURS

async def fetch_popular_players(platform="ps", max_pages=2):
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE,"r",encoding="utf-8") as f:
                data=json.load(f)
            cache_time=dt.fromisoformat(data.get("timestamp"))
            if dt.utcnow()-cache_time<timedelta(hours=CACHE_TTL_HOURS):
                return [p for p in data.get("players",[]) if p["platform"]==platform]
        except: pass
    players=[]
    base_url="https://www.futbin.com/popular"
    async with aiohttp.ClientSession(headers={"User-Agent":"Mozilla/5.0"}) as session:
        for page in range(1,max_pages+1):
            try:
                async with session.get(f"{base_url}?page={page}",timeout=15) as resp:
                    html=await resp.text()
                soup=BeautifulSoup(html,"html.parser")
                rows=soup.select("tr.player_tr_1, tr.player_tr_2")
                for row in rows:
                    link=row.find("a",href=True)
                    if not link: continue
                    href=link["href"]
                    parts=href.split("/")
                    if len(parts)>=5 and parts[2]=="player": player_id=parts[3]
                    else: continue
                    name=link.text.strip()
                    players.append({"id":player_id,"name":name,"platform":platform})
            except: continue
    with open(CACHE_FILE,"w",encoding="utf-8") as f:
        json.dump({"timestamp":dt.utcnow().isoformat(),"players":players},f,ensure_ascii=False)
    return [p for p in players if p["platform"]==platform]

async def fetch_player_image(player_id):
    url=f"https://www.futbin.com/22/player/{player_id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as resp:
                html=await resp.text()
        except: return None
    soup=BeautifulSoup(html,"html.parser")
    img_tag=soup.find("img",{"id":"player_card_img"})
    if img_tag: return img_tag.get("src")
    return None

async def is_future_upgrade(player_id):
    url = f"https://www.futbin.com/22/player/{player_id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as resp:
                html = await resp.text()
        except:
            return False
    return "Future Upgrade" in html or "In-Form" in html or "TOTW" in html