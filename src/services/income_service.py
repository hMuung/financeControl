# src/services/income_service.py
import sqlite3
from datetime import datetime, timedelta
from models.models import Income
from config import DB_NAME
from services.seeds import seed_incomes


class IncomeService:

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
        #self._seed_if_empty()

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
        cls._totals: dict = {
            "today": {"total": 0.0, "by_category": {}},
            "yesterday": {"total": 0.0, "by_category": {}},
            "week": {"total": 0.0, "by_category": {}},
            "last_week": {"total": 0.0, "by_category": {}},
            "month": {"total": 0.0, "by_category": {}},
            "year": {"total": 0.0, "by_category": {}},
            "all_time": {"total": 0.0, "by_category": {}},
        }

    @classmethod
    def get_totals(cls, db_name=DB_NAME) -> dict:
        now = datetime.now().date()

        today_str = now.strftime("%Y-%m-%d")
        yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")

        start_week = now - timedelta(days=now.weekday())
        start_week_str = start_week.strftime("%Y-%m-%d")

        start_last_week_str = (start_week - timedelta(days=7)).strftime("%Y-%m-%d")
        end_last_week_str = (start_week - timedelta(days=1)).strftime("%Y-%m-%d")

        start_month_str = now.replace(day=1).strftime("%Y-%m-%d")
        start_year_str = now.replace(month=1, day=1).strftime("%Y-%m-%d")

        periods_query = {
            "today": "WHERE date = ?",
            "yesterday": "WHERE date = ?",
            "week": "WHERE date >= ?",
            "last_week": "WHERE date BETWEEN ? AND ?",
            "month": "WHERE date >= ?",
            "year": "WHERE date >= ?",
            "all_time": "",
        }

        params_map = {
            "today": (today_str,),
            "yesterday": (yesterday_str,),
            "week": (start_week_str,),
            "last_week": (start_last_week_str, end_last_week_str),
            "month": (start_month_str,),
            "year": (start_year_str,),
            "all_time": (),
        }

        totals = {
            p: {"total": 0.0, "by_category": {}}
            for p in ["today", "yesterday", "week", "last_week", "month", "year", "all_time"]
        }

        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            for period, where_clause in periods_query.items():
                query = f"""
                    SELECT category_id, SUM(amount)
                    FROM incomes
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

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_incomes_date_cat 
                ON incomes(date, category_id)
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
            cursor.execute("SELECT category_id, amount, date FROM incomes WHERE id = ?", (income.id,))
            old_row = cursor.fetchone()
            if not old_row:
                return False

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
            if cursor.rowcount > 0:
                return True
            return False

    def delete(self, income_id: int) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_id, amount, date FROM incomes WHERE id = ?", (income_id,))
            old_row = cursor.fetchone()
            if not old_row:
                return False

            cursor.execute("DELETE FROM incomes WHERE id = ?", (income_id,))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            return False