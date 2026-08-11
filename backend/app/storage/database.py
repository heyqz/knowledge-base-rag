import sqlite3

from app.core.config import settings


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(settings.SQLITE_PATH)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query: str, params=()):
        cursor = self.conn.execute(query, params)
        self.conn.commit()
        return cursor
    
    def init_db(self):
        self.execute(
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

db = Database()
db.init_db()
