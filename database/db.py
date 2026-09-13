import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT UNIQUE,
    published TEXT,
    summary TEXT,
    category TEXT,
    collected_at TEXT
);
"""


def init_db(db_path):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(SCHEMA)
        conn.commit()


def save_items(db_path, items):
    if not items:
        return 0

    with sqlite3.connect(db_path) as conn:
        saved = 0
        for item in items:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO items
                (source, title, url, published, summary, category, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.get("source", ""),
                    item.get("title", ""),
                    item.get("url", ""),
                    item.get("published", ""),
                    item.get("summary", ""),
                    item.get("category", "general_ai"),
                    item.get("collected_at", ""),
                ),
            )
            saved += cursor.rowcount
        conn.commit()
    return saved
