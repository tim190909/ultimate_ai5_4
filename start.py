import os
import asyncio
from aiohttp import web
from bot import bot # ton bot existant

# ------------------------------
# Fonction pour démarrer le bot
# ------------------------------
async def start_bot():
    await bot.start(os.getenv("DISCORD_TOKEN"))

# ------------------------------
# Petit serveur web pour Render
# ------------------------------
async def handle(request):
    return web.Response(text="🤖 Bot en ligne !")

async def main():
    # Crée l'application web
    app = web.Application()
    app.add_routes([web.get("/", handle)])

    # Setup du runner
    runner = web.AppRunner(app)
    await runner.setup()

    # Port fourni par Render
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Serveur web lancé sur le port {port}")

    # Lancer le bot Discord en parallèle
    await start_bot()

# Run le main asyncio
asyncio.run(main())

