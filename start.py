import os
import asyncio
from aiohttp import web
from bot import bot # ton bot.py principal

# -------------------------
# Serveur web minimal pour Render
# -------------------------
async def handle(request):
    return web.Response(text="Bot en ligne !")

async def init_web_server():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    port = int(os.environ.get("PORT", 10000)) # Render fournit le port via env
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Web server lancé sur le port {port}")

# -------------------------
# Démarrage principal
# -------------------------
async def main():
    await init_web_server() # keep-alive
    bot.run(os.environ["DISCORD_TOKEN"]) # lance le bot Discord

if __name__ == "__main__":
    asyncio.run(main())
