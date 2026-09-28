# src/services/expense_service.py
import sqlite3
from datetime import datetime, timedelta
from models.models import Expense
from config import DB_NAME
from services.seeds import seed_expenses


class ExpenseService:

    _totals: dict = {
        "today": {"total": 0.0, "by_category": {}},
        "week": {"total": 0.0, "by_category": {}},
        "month": {"total": 0.0, "by_category": {}},
        "year": {"total": 0.0, "by_category": {}},
        "all_time": {"total": 0.0, "by_category": {}},
    }
    _totals_initialized: bool = False

    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._init_db()
        self._seed_if_empty()

    @staticmethod
    def _get_active_periods(date_str: str) -> list[str]:
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return ["all_time"]

        now = datetime.now().date()
        periods = ["all_time"]

        if d.year == now.year:
            periods.append("year")
            if d.month == now.month:
                periods.append("month")

        if d.isocalendar()[:2] == now.isocalendar()[:2]:
            periods.append("week")

        if d == now:
            periods.append("today")

        return periods

    @classmethod
    def _reset_totals(cls):
        cls._totals = {
            "today": {"total": 0.0, "by_category": {}},
            "week": {"total": 0.0, "by_category": {}},
            "month": {"total": 0.0, "by_category": {}},
            "year": {"total": 0.0, "by_category": {}},
            "all_time": {"total": 0.0, "by_category": {}},
        }

    @classmethod
    def get_totals(cls, db_name=DB_NAME) -> dict:
        """Calcula dinamicamente los acumulados mediante consultas SQL agrupadas e indexadas."""
        now = datetime.now().date()

        today_str = now.strftime("%Y-%m-%d")
        start_week_str = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
        start_month_str = now.replace(day=1).strftime("%Y-%m-%d")
        start_year_str = now.replace(month=1, day=1).strftime("%Y-%m-%d")

        periods_query = {
            "today": "WHERE date = ?",
            "week": "WHERE date >= ?",
            "month": "WHERE date >= ?",
            "year": "WHERE date >= ?",
            "all_time": "",
        }

        params_map = {
            "today": (today_str,),
            "week": (start_week_str,),
            "month": (start_month_str,),
            "year": (start_year_str,),
            "all_time": (),
        }

        totals = {
            p: {"total": 0.0, "by_category": {}}
            for p in ["today", "week", "month", "year", "all_time"]
        }

        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            for period, where_clause in periods_query.items():
                query = f"""
                    SELECT category_id, SUM(amount)
                    FROM expenses
                    {where_clause}
                    GROUP BY category_id
                """
                cursor.execute(query, params_map[period])

                period_total = 0.0
                by_cat = {}
                for cat_id, cat_sum in cursor.fetchall():
                    if cat_sum is not None:
                        rounded_sum = round(cat_sum, 2)
                        by_cat[cat_id] = rounded_sum
                        period_total += rounded_sum

                totals[period]["total"] = round(period_total, 2)
                totals[period]["by_category"] = by_cat

        return totals

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

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_expenses_date_cat 
                ON expenses(date, category_id)
            """)
            conn.commit()

    def _seed_if_empty(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM expenses")
            if cursor.fetchone()[0] == 0:
                sample_expenses = seed_expenses
                cursor.executemany(
                    "INSERT INTO expenses (category_id, origin_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
                    sample_expenses,
                )
                conn.commit()

    def save(self, expense: Expense) -> bool:
        expense.date = datetime.now().strftime("%Y-%m-%d")
        desc = (
            expense.description.strip()
            if expense.description and expense.description.strip()
            else "Sin descripción"
        )

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (category_id, origin_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
                (expense.category_id, expense.origin_id, expense.amount, desc, expense.date),
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
                    origin_name=r[7],
                )
                for r in cursor.fetchall()
            ]

    def update(self, expense: Expense) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_id, amount, date FROM expenses WHERE id = ?", (expense.id,))
            old_row = cursor.fetchone()
            if not old_row:
                return False

            cursor.execute(
                """
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
            if cursor.rowcount > 0:
                return True
            return False

    def delete(self, expense_id: int) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_id, amount, date FROM expenses WHERE id = ?", (expense_id,))
            old_row = cursor.fetchone()
            if not old_row:
                return False

            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            return False