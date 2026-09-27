# src/services/income_service.py
import sqlite3
from datetime import datetime
from models.models import Income
from config import DB_NAME
from services.seeds import seed_incomes


class IncomeService:

    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._init_db()
        self._seed_if_empty()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS incomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    origin_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT DEFAULT 'Sin descripción',
                    date TEXT NOT NULL,
                    FOREIGN KEY(category_id) REFERENCES categories(id),
                    FOREIGN KEY(origin_id) REFERENCES origins(id)
                )
            """)
            conn.commit()

    def _seed_if_empty(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM incomes")
            if cursor.fetchone()[0] == 0 and seed_incomes:
                cursor.executemany(
                    "INSERT INTO incomes (category_id, origin_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
                    seed_incomes,
                )
                conn.commit()

    def save(self, income: Income) -> bool:
        income.date = datetime.now().strftime("%Y-%m-%d")
        desc = (
            income.description.strip()
            if income.description and income.description.strip()
            else "Sin descripción"
        )

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO incomes (category_id, origin_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
                (
                    income.category_id,
                    income.origin_id,
                    income.amount,
                    desc,
                    income.date,
                ),
            )
            conn.commit()
            return True

    def get_all(self) -> list[Income]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, i.category_id, i.origin_id, i.amount, i.description, i.date, c.name, o.name
                FROM incomes i
                LEFT JOIN categories c ON i.category_id = c.id
                LEFT JOIN origins o ON i.origin_id = o.id
                ORDER BY i.id DESC
            """)
            return [
                Income(
                    id=r[0],
                    category_id=r[1],
                    origin_id=r[2],
                    amount=r[3],
                    description=r[4],
                    date=r[5],
                    category_name=r[6],
                    origin_name=r[7],
                )
                for r in cursor.fetchall()
            ]

    def update(self, income: Income) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE incomes
                SET category_id = ?, origin_id = ?, amount = ?, description = ?
                WHERE id = ? """,
                (
                    income.category_id,
                    income.origin_id,
                    income.amount,
                    income.description,
                    income.id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, income_id: int) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM incomes WHERE id = ?", (income_id,))
            conn.commit()
            return cursor.rowcount > 0