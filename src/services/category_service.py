# src/services/category_service.py
import sqlite3
from models.models import Category
from config import DB_NAME
from services.seeds import seed_categories


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
                    name TEXT NOT NULL,
                    color TEXT,
                    bg_color TEXT,
                    icon TEXT,
                    type TEXT NOT NULL DEFAULT 'EXPENSE',
                    UNIQUE(name, type)
                )
            """)
            conn.commit()

    def _seed_if_empty(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM categories")
            if cursor.fetchone()[0] == 0:
                sample_categories = seed_categories
                # sample_categories debe contener tuplas con 5 elementos: (name, color, bg_color, icon, type)
                cursor.executemany(
                    "INSERT OR IGNORE INTO categories (name, color, bg_color, icon, type) VALUES (?, ?, ?, ?, ?)",
                    sample_categories
                )
                conn.commit()

    def get_all(self, category_type: str | None = None) -> list[Category]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            if category_type:
                cursor.execute(
                    "SELECT id, name, color, bg_color, icon, type FROM categories WHERE type = ?",
                    (category_type,)
                )
            else:
                cursor.execute("SELECT id, name, color, bg_color, icon, type FROM categories")
                
            return [
                Category(
                    id=r[0], 
                    name=r[1], 
                    color=r[2], 
                    bg_color=r[3], 
                    icon=r[4], 
                    type=r[5]
                ) 
                for r in cursor.fetchall()
            ]