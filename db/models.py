import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT,
            platform TEXT,
            created_at TEXT
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER,
            timestamp TEXT,
            price INTEGER,
            FOREIGN KEY(target_id) REFERENCES targets(id)
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS user_watchlist (
            user_id TEXT,
            target_id INTEGER,
            PRIMARY KEY(user_id,target_id),
            FOREIGN KEY(target_id) REFERENCES targets(id)
        )""")
        await db.commit()
