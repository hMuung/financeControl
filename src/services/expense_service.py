# src/services/expense_service.py
import sqlite3
from datetime import datetime
from models.expense_model import Expense

class ExpenseService:
    def __init__(self, db_name="expenses_app.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    origin TEXT NOT NULL,
                    description TEXT DEFAULT 'Sin descripción',
                    date TEXT NOT NULL
                )
            """)
            
            cursor.execute("PRAGMA table_info(expenses)")
            columns = [column[1] for column in cursor.fetchall()]
            if "description" not in columns:
                cursor.execute("ALTER TABLE expenses ADD COLUMN description TEXT DEFAULT 'Sin descripción'")
            conn.commit()

        # Insertar registros automáticamente si la tabla está vacía
        self._seed_if_empty()

    def _seed_if_empty(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM expenses")
            count = cursor.fetchone()[0]

            if count == 0:
                sample_expenses = [
                    ("Comida", 150.50, "Tarjeta Débito", "Supermercado semanal", "2026-03-01"),
                    ("Transporte", 45.00, "Efectivo", "Carga de gasolina", "2026-03-02"),
                    ("Servicios", 850.00, "Transferencia", "Pago de luz y agua", "2026-03-03"),
                    ("Entretenimiento", 220.00, "Tarjeta Crédito", "Suscripción streaming y cine", "2026-03-05"),
                    ("Comida", 85.00, "Efectivo", "Almuerzo de trabajo", "2026-03-06"),
                    ("Salud", 340.00, "Tarjeta Débito", "Medicamentos farmacia", "2026-03-08"),
                    ("Educación", 1200.00, "Tarjeta Crédito", "Curso en línea Python", "2026-03-10"),
                    ("Hogar", 450.00, "Tarjeta Débito", "Artículos de limpieza y hogar", "2026-03-11"),
                    ("Transporte", 35.00, "Efectivo", "Pasaje de autobús / metro", "2026-03-12"),
                    ("Comida", 65.00, "Efectivo", "Café y snacks", "2026-03-13")
                ]
                cursor.executemany("""
                    INSERT INTO expenses (category, amount, origin, description, date)
                    VALUES (?, ?, ?, ?, ?)
                """, sample_expenses)
                conn.commit()

    def save(self, expense: Expense) -> bool:
        expense.date = datetime.now().strftime("%Y-%m-%d")
        desc = expense.description.strip() if expense.description and expense.description.strip() else "Sin descripcion"
        
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (category, amount, origin, description, date) VALUES (?, ?, ?, ?, ?)",
                (expense.category, expense.amount, expense.origin, desc, expense.date)
            )
            conn.commit()
            return True

    def get_all(self) -> list[Expense]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, category, amount, origin, description, date FROM expenses ORDER BY id DESC")
            rows = cursor.fetchall()
            return [
                Expense(
                    id=r[0], 
                    category=r[1], 
                    amount=r[2], 
                    origin=r[3], 
                    description=r[4] if r[4] else "Sin descripcion", 
                    date=r[5]
                ) 
                for r in rows
            ]

    def delete(self, expense_id: int) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()
            return cursor.rowcount > 0