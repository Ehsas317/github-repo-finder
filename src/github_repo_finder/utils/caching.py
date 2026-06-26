import sqlite3
import json
import pickle
from datetime import datetime, timedelta
from typing import Any, Optional
from pathlib import Path

class CacheManager:
    def __init__(self, db_path: str = "~/.github_repo_finder/cache.db", ttl_hours: int = 24):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl_hours
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value BLOB,
                    timestamp DATETIME
                )
            """)

    def get(self, key: str) -> Optional[Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT value, timestamp FROM cache WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row:
                value, timestamp = row
                if datetime.fromisoformat(timestamp) + timedelta(hours=self.ttl) > datetime.now():
                    return pickle.loads(value)
                else:
                    self.delete(key)
        return None

    def set(self, key: str, value: Any):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?)",
                (key, pickle.dumps(value), datetime.now().isoformat())
            )

    def delete(self, key: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache WHERE key = ?", (key,))

    def clear(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache")
