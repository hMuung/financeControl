# src/services/expense_service.py
import sqlite3
from datetime import datetime
from models.expense import Expense

class ExpenseService:
    def __init__(self, db_name="expenses_app.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    origin TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            """)

    def save(self, expense: Expense) -> bool:
        expense.date = datetime.now().strftime("%Y-%m-%d")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (category, amount, origin, date) VALUES (?, ?, ?, ?)",
                (expense.category, expense.amount, expense.origin, expense.date)
            )
            conn.commit()
            return True

    def get_all(self) -> list[Expense]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, category, amount, origin, date FROM expenses ORDER BY id DESC")
            rows = cursor.fetchall()
            return [
                Expense(id=r[0], category=r[1], amount=r[2], origin=r[3], date=r[4]) 
                for r in rows
            ]