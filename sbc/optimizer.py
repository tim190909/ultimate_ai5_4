import asyncio
from db import models
import aiosqlite
from datetime import datetime as dt

async def get_all_sbc_solutions(sbc_name: str, max_solutions=5):
    # Ici, on pourrait récupérer les prix réels depuis Futbin / DB
    solutions = [
        {"cartes": [("Carte A", 10000), ("Carte B", 15000), ("Carte C", 12000)], "total": 37000},
        {"cartes": [("Carte D", 9000), ("Carte E", 16000), ("Carte F", 11000)], "total": 36000},
        {"cartes": [("Carte G", 9500), ("Carte H", 15500), ("Carte I", 12500)], "total": 37500},
    ]
    solutions.sort(key=lambda x: x["total"])
    async with aiosqlite.connect(models.DB_PATH) as db:
        now = dt.utcnow().isoformat()
        for sol in solutions[:max_solutions]:
            await db.execute(
                "INSERT INTO sbc_history (sbc_name, total, timestamp) VALUES (?, ?, ?)",
                (sbc_name, sol["total"], now)
            )
        await db.commit()
    msg = f"Solutions SBC pour **{sbc_name}** :\n"
    for idx, sol in enumerate(solutions[:max_solutions], 1):
        msg += f"\n**Solution {idx}** - Total : {sol['total']} coins\n"
        for c, price in sol["cartes"]:
            msg += f"- {c} : {price}\n"
    return msg

async def optimize_sbc(sbc_name: str):
    return await get_all_sbc_solutions(sbc_name)