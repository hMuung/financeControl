# src/services/origin_service.py
import sqlite3
from models.models import Origin
from config import DB_NAME
from services.seeds import seed_origin

class OriginService:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._init_db()
        self._seed_if_empty()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS origins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    color TEXT,
                    bg_color TEXT,
                    icon TEXT,
                    type TEXT NOT NULL DEFAULT 'EXPENSE'
                )
            """)
            conn.commit()

    def _seed_if_empty(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM origins")
            if cursor.fetchone()[0] == 0:
                sample_origins = seed_origin
                # seed_origin debe incluir 5 valores: (name, color, bg_color, icon, type)
                cursor.executemany(
                    "INSERT INTO origins (name, color, bg_color, icon, type) VALUES (?, ?, ?, ?, ?)",
                    sample_origins
                )
                conn.commit()

    def get_all(self, origin_type: str | None = None) -> list[Origin]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            if origin_type:
                cursor.execute(
                    "SELECT id, name, color, bg_color, icon, type FROM origins WHERE type = ?",
                    (origin_type,)
                )
            else:
                cursor.execute("SELECT id, name, color, bg_color, icon, type FROM origins")

            return [
                Origin(
                    id=r[0], 
                    name=r[1], 
                    color=r[2], 
                    bg_color=r[3], 
                    icon=r[4], 
                    type=r[5]
                ) 
                for r in cursor.fetchall()
            ]