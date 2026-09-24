# src/services/expense_service.py
import sqlite3
from datetime import datetime
from models.models import Expense
from config import DB_NAME

class ExpenseService:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
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
            cursor.execute("SELECT COUNT(*) FROM expenses")
            if cursor.fetchone()[0] == 0:
                sample_expenses = [
                    (1, 1, 150.50, "Almuerzo de trabajo", datetime.now().strftime("%Y-%m-%d")),
                    (2, 2, 45.00, "Pasaje de transporte", datetime.now().strftime("%Y-%m-%d")),
                    (3, 3, 1200.00, "Servicio de Internet", datetime.now().strftime("%Y-%m-%d")),
                ]
                cursor.executemany(
                    "INSERT INTO expenses (category_id, origin_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
                    sample_expenses
                )
                conn.commit()

    def save(self, expense: Expense) -> bool:
        expense.date = datetime.now().strftime("%Y-%m-%d")
        desc = expense.description.strip() if expense.description and expense.description.strip() else "Sin descripción"
        
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (category_id, origin_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
                (expense.category_id, expense.origin_id, expense.amount, desc, expense.date)
            )
            conn.commit()
            return True

    def get_all(self) -> list[Expense]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.category_id, e.origin_id, e.amount, e.description, e.date, c.name, o.name
                FROM expenses e
                LEFT JOIN categories c ON e.category_id = c.id
                LEFT JOIN origins o ON e.origin_id = o.id
                ORDER BY e.id DESC
            """)
            return [
                Expense(
                    id=r[0],
                    category_id=r[1],
                    origin_id=r[2],
                    amount=r[3],
                    description=r[4],
                    date=r[5],
                    category_name=r[6],
                    origin_name=r[7]
                ) 
                for r in cursor.fetchall()
            ]

    def update(self, expense: Expense) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE expenses
                SET category_id = ?, origin_id = ?, amount = ?, description = ?
                WHERE id = ? """,
                (
                    expense.category_id,
                    expense.origin_id,
                    expense.amount,
                    expense.description,
                    expense.id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, expense_id: int) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()
            return cursor.rowcount > 0