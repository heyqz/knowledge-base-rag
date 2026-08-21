import sqlite3
from pathlib import Path

from app.core.config import settings


class Database:
    def __init__(self):
        self.db_path = Path(settings.SQLITE_PATH)
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def execute(self, query: str, params=()):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            cursor = conn.execute(query, params)
            conn.commit()

            return cursor.fetchall()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    uploaded_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

db = Database()
db.init_db()
