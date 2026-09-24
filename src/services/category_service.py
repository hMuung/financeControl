# src/services/category_service.py
import sqlite3
from models.models import Category
from config import DB_NAME

class CategoryService:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._init_db()
        self._seed_if_empty()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
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
            cursor.execute("SELECT COUNT(*) FROM categories")
            if cursor.fetchone()[0] == 0:
                sample_categories = [
                    ("Comida", "#388E3C", "#E8F5E9", "category"),
                    ("Transporte", "#F57C00", "#FFF3E0", "directions_car"),
                    ("Servicios", "#D32F2F", "#FFEBEE", "receipt"),
                    ("Entretenimiento", "#7B1FA2", "#F3E5F5", "movie"),
                ]
                cursor.executemany(
                    "INSERT INTO categories (name, color, bg_color, icon) VALUES (?, ?, ?, ?)",
                    sample_categories
                )
                conn.commit()

    def get_all(self) -> list[Category]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, color, bg_color, icon FROM categories")
            return [Category(id=r[0], name=r[1], color=r[2], bg_color=r[3], icon=r[4]) for r in cursor.fetchall()]