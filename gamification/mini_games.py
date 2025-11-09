import random
from db import models
import aiosqlite

BADGES = ["Trader Expert", "SBC Master", "Visionnaire", "Market Guru"]

async def award_badge(user_id):
    badge = random.choice(BADGES)
    async with aiosqlite.connect(models.DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO user_badges (user_id, badge, points) VALUES (?, ?, ?)",
            (user_id, badge, 100)
        )
        await db.commit()
    return badge

async def mini_game_guess_price(user_id, real_price):
    guess = random.randint(int(real_price*0.5), int(real_price*1.5))
    if abs(guess-real_price)/real_price < 0.1:
        badge = await award_badge(user_id)
        return f"Bravo ! Tu as gagné le badge {badge} 🎉"
    return f"Essaie encore ! Le prix réel était {real_price}."
	
