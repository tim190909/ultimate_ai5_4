-- ========================================================
-- SCHEMA SQL pour FUT Trading Bot – Version 41.0
-- ========================================================

-- Table des joueurs
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    futbin_id INTEGER NOT NULL,
    name TEXT,
    platform TEXT,
    created_at TEXT DEFAULT (datetime('now','localtime'))
);

-- Historique des prix
CREATE TABLE IF NOT EXISTS price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    timestamp TEXT DEFAULT (datetime('now','localtime')),
    price INTEGER NOT NULL,
    FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Watchlist des utilisateurs
CREATE TABLE IF NOT EXISTS watchlist (
    user_id TEXT NOT NULL,
    player_id INTEGER NOT NULL,
    PRIMARY KEY(user_id, player_id),
    FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Alertes de prix
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    player_id INTEGER NOT NULL,
    target_price INTEGER NOT NULL,
    direction TEXT CHECK(direction IN ('up','down')),
    created_at TEXT DEFAULT (datetime('now','localtime')),
    FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Table pour sauvegarder les prédictions IA (optionnelle)
CREATE TABLE IF NOT EXISTS ai_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    predicted_price INTEGER NOT NULL,
    predicted_at TEXT DEFAULT (datetime('now','localtime')),
    FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Table pour les logs (optionnelle)
CREATE TABLE IF NOT EXISTS bot_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now','localtime'))
);
