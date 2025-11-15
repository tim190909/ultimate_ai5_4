import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            futbin_id INTEGER,
            name TEXT,
            platform TEXT,
            created_at TEXT
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            timestamp TEXT,
            price INTEGER,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            user_id TEXT,
            player_id INTEGER,
            PRIMARY KEY(user_id, player_id)
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            player_id INTEGER,
            target_price INTEGER,
            direction TEXT,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS ai_training (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            predicted_price INTEGER,
            actual_price INTEGER,
            timestamp TEXT
        )""")
        await db.commit()
