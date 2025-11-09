import aiosqlite
from datetime import datetime as dt
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT NOT NULL,
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
            server_id TEXT,
            target_id INTEGER,
            PRIMARY KEY(user_id,server_id,target_id),
            FOREIGN KEY(target_id) REFERENCES targets(id)
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS sbc_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sbc_name TEXT,
            total INTEGER,
            timestamp TEXT
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS user_badges (
            user_id TEXT,
            badge TEXT,
            points INTEGER DEFAULT 0,
            PRIMARY KEY(user_id,badge)
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            player_id TEXT,
            platform TEXT,
            price INTEGER,
            type TEXT,
            timestamp TEXT
        )""")
        await db.commit()