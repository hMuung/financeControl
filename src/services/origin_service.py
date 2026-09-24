# src/services/origin_service.py
import sqlite3
from models.models import Origin
from config import DB_NAME

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
                    icon TEXT
                )
            """)
            conn.commit()

    def _seed_if_empty(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM origins")
            if cursor.fetchone()[0] == 0:
                sample_origins = [
                    ("Efectivo", "#2E7D32", "#E8F5E9", "payments"),
                    ("Tarjeta de Débito", "#0277BD", "#E1F5FE", "credit_card"),
                    ("Tarjeta de Crédito", "#C2185B", "#FCE4EC", "credit_card"),
                ]
                cursor.executemany(
                    "INSERT INTO origins (name, color, bg_color, icon) VALUES (?, ?, ?, ?)",
                    sample_origins
                )
                conn.commit()

    def get_all(self) -> list[Origin]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, color, bg_color, icon FROM origins")
            return [Origin(id=r[0], name=r[1], color=r[2], bg_color=r[3], icon=r[4]) for r in cursor.fetchall()]