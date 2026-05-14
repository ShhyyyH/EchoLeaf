import json
import sqlite3
import os
from datetime import datetime, timezone, date

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "echoleaf.db")

os.makedirs(DB_DIR, exist_ok=True)


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            feeling TEXT DEFAULT '',
            tags TEXT DEFAULT '[]',
            rating TEXT DEFAULT '',
            read_date TEXT DEFAULT '',
            fragment TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_reading(title: str, feeling: str, tags: list[str], rating: str,
                 read_date: date, fragment: str) -> str:
    rid = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    read_date_str = str(read_date) if read_date else ""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO readings (id, title, feeling, tags, rating, read_date, fragment, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (rid, title.strip(), feeling.strip(), json.dumps(tags, ensure_ascii=False),
         rating, read_date_str, fragment.strip(), _utcnow()),
    )
    conn.commit()
    conn.close()
    return rid


def load_readings() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, title, feeling, tags, rating, read_date, fragment, created_at "
        "FROM readings ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    records = []
    for row in rows:
        records.append({
            "id": row[0],
            "book": row[1],
            "feeling": row[2],
            "tags": json.loads(row[3]),
            "rating": row[4],
            "date": row[5],
            "fragment": row[6],
            "created_at": row[7],
        })
    return records


def delete_reading(rid: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM readings WHERE id = ?", (rid,))
    conn.commit()
    conn.close()
