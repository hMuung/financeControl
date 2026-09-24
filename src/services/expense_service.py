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
                    #  COMIDA (category_id = 1)
                    (1, 1, 150.50, "Almuerzo de trabajo", "2026-08-01"),
                    (1, 2, 85.00, "Café y pan dulce", "2026-08-02"),
                    (1, 3, 450.00, "Cena en restaurante", "2026-08-03"),
                    (1, 1, 350.00, "Despensa semanal", "2026-08-04"),
                    (1, 2, 120.00, "Tacos de la esquina", "2026-08-05"),
                    (1, 3, 280.00, "Comida rápida", "2026-08-06"),
                    (1, 1, 65.00, "Botanas y refrescos", "2026-08-07"),
                    (1, 2, 520.00, "Supermercado quincenal", "2026-08-08"),
                    (1, 3, 195.00, "Pizza para llevar", "2026-08-09"),
                    (1, 1, 110.00, "Desayuno ejecutivo", "2026-08-10"),
                    (1, 2, 45.00, "Agua embotellada y snack", "2026-08-11"),
                    (1, 3, 850.00, "Supermercado mensual", "2026-08-12"),
                    (1, 1, 75.00, "Helado y postre", "2026-08-13"),
                    (1, 2, 210.00, "Comida buffet", "2026-08-14"),
                    (1, 3, 340.00, "Cena de mariscos", "2026-08-15"),
                    (1, 1, 90.00, "Torta y jugo", "2026-08-16"),
                    (1, 2, 160.00, "Comida corrida", "2026-08-17"),
                    (1, 3, 620.00, "Compra en carnicería", "2026-08-18"),
                    (1, 1, 130.00, "Frutas y verduras en mercado", "2026-08-19"),
                    (1, 2, 250.00, "Sushi express", "2026-08-20"),
                    (1, 3, 180.00, "Hamburguesa con papas", "2026-08-21"),
                    (1, 1, 55.00, "Café por la mañana", "2026-08-22"),
                    (1, 2, 410.00, "Despensa de verduras y frutas", "2026-08-23"),
                    (1, 3, 310.00, "Comida en plaza comercial", "2026-08-24"),
                    (1, 1, 95.00, "Panadería tradicional", "2026-08-25"),
                    (1, 2, 175.00, "Ensaladas preparadas", "2026-08-26"),
                    (1, 3, 530.00, "Cena familiar fin de semana", "2026-08-27"),
                    (1, 1, 40.00, "Galletas y café", "2026-08-28"),
                    (1, 2, 290.00, "Alitas y bebidas", "2026-08-29"),
                    (1, 3, 780.00, "Súper de productos orgánicos", "2026-08-30"),

                    # TRANSPORTE (category_id = 2)
                    (2, 2, 45.00, "Pasaje de transporte", "2026-08-01"),
                    (2, 3, 650.00, "Gasolina para el auto", "2026-08-02"),
                    (2, 1, 180.00, "Viaje en Uber / Taxi", "2026-08-03"),
                    (2, 2, 25.00, "Peaje de autopista", "2026-08-04"),
                    (2, 3, 700.00, "Tanque lleno de gasolina", "2026-08-05"),
                    (2, 1, 50.00, "Estacionamiento centro", "2026-08-06"),
                    (2, 2, 220.00, "Lavado de auto", "2026-08-07"),
                    (2, 3, 140.00, "Viaje de regreso en Uber", "2026-08-08"),
                    (2, 1, 30.00, "Recarga tarjeta transporte", "2026-08-09"),
                    (2, 3, 600.00, "Gasolina semana 2", "2026-08-10"),
                    (2, 1, 120.00, "Taxi nocturno", "2026-08-11"),
                    (2, 2, 350.00, "Cambio de aceite auto", "2026-08-12"),
                    (2, 3, 680.00, "Gasolina premium", "2026-08-13"),
                    (2, 1, 40.00, "Propinas y viene-viene", "2026-08-14"),
                    (2, 2, 90.00, "Peaje regreso caseta", "2026-08-15"),
                    (2, 3, 210.00, "Uber al aeropuerto", "2026-08-16"),
                    (2, 1, 250.00, "Taxi del aeropuerto", "2026-08-17"),
                    (2, 2, 60.00, "Estacionamiento plaza", "2026-08-18"),
                    (2, 3, 720.00, "Gasolina semana 3", "2026-08-19"),
                    (2, 1, 50.00, "Boleto de autobús interurbano", "2026-08-20"),
                    (2, 2, 130.00, "Reparación de pinchazo llanta", "2026-08-21"),
                    (2, 3, 640.00, "Gasolina semana 4", "2026-08-22"),
                    (2, 1, 80.00, "Viaje en DiDi", "2026-08-23"),
                    (2, 2, 100.00, "Recarga tarjeta colectivo", "2026-08-24"),
                    (2, 3, 310.00, "Alineación y balanceo", "2026-08-25"),

                    # SERVICIOS (category_id = 3)
                    (3, 3, 1200.00, "Servicio de Internet", "2026-08-01"),
                    (3, 2, 450.00, "Factura de Luz", "2026-08-02"),
                    (3, 2, 280.00, "Recibo de Agua", "2026-08-03"),
                    (3, 3, 350.00, "Plan de Telefonía Móvil", "2026-08-04"),
                    (3, 2, 850.00, "Mantenimiento del condominio", "2026-08-05"),
                    (3, 3, 500.00, "Carga de Gas L.P.", "2026-08-06"),
                    (3, 2, 199.00, "Suscripción almacenamiento en nube", "2026-08-07"),
                    (3, 3, 1100.00, "Seguro de auto mensual", "2026-08-08"),
                    (3, 1, 150.00, "Pago de mantenimiento extra", "2026-08-09"),
                    (3, 2, 320.00, "Recarga móvil adicional", "2026-08-10"),
                    (3, 3, 400.00, "Servicio de limpieza dominguero", "2026-08-11"),
                    (3, 2, 250.00, "Pago de impuesto predial", "2026-08-12"),
                    (3, 3, 600.00, "Seguro médico deducible", "2026-08-13"),
                    (3, 1, 200.00, "Reparación de fuga de agua", "2026-08-14"),
                    (3, 2, 180.00, "Servicio de fumigación", "2026-08-15"),
                    (3, 3, 1250.00, "Internet de alta velocidad oficina", "2026-08-16"),
                    (3, 1, 300.00, "Mantenimiento aire acondicionado", "2026-08-17"),
                    (3, 2, 480.00, "Luz segundo periodo", "2026-08-18"),
                    (3, 3, 380.00, "Plan móvil adicional", "2026-08-19"),
                    (3, 2, 550.00, "Gas estufa y calentador", "2026-08-20"),
                    (3, 3, 1500.00, "Seguro de gastos médicos", "2026-08-21"),
                    (3, 1, 100.00, "Copia de llaves casa", "2026-08-22"),
                    (3, 2, 220.00, "Lavandería y tintorería", "2026-08-23"),
                    (3, 3, 90.00, "Dominio y hosting web", "2026-08-24"),
                    (3, 1, 180.00, "Jardinería quincenal", "2026-08-25"),

                    # ENTRETENIMIENTO (category_id = 4)
                    (4, 3, 240.00, "Boletos de cine", "2026-08-01"),
                    (4, 2, 180.00, "Suscripción Netflix", "2026-08-02"),
                    (4, 3, 129.00, "Suscripción Spotify Premium", "2026-08-03"),
                    (4, 1, 350.00, "Entradas a evento local", "2026-08-04"),
                    (4, 3, 899.00, "Videojuego digital", "2026-08-05"),
                    (4, 2, 150.00, "Compra de libro digital", "2026-08-06"),
                    (4, 3, 400.00, "Salida a boliche con amigos", "2026-08-07"),
                    (4, 1, 200.00, "Juegos mecánicos y feria", "2026-08-08"),
                    (4, 2, 299.00, "Membresía de gimnasio", "2026-08-09"),
                    (4, 3, 150.00, "Renta de película streaming", "2026-08-10"),
                    (4, 1, 80.00, "Dulces y dulcería del cine", "2026-08-11"),
                    (4, 3, 1200.00, "Boletos para concierto", "2026-08-12"),
                    (4, 2, 220.00, "Suscripción Disney+", "2026-08-13"),
                    (4, 3, 310.00, "Entradas a museo y guía", "2026-08-14"),
                    (4, 1, 160.00, "Juegos de mesa en cafetería", "2026-08-15"),
                    (4, 2, 450.00, "Pase de temporada teatro", "2026-08-16"),
                    (4, 3, 99.00, "Suscripción Amazon Prime", "2026-08-17"),
                    (4, 1, 280.00, "Cervezas y botanas en bar", "2026-08-18"),
                    (4, 2, 600.00, "Inscripción a carrera 10K", "2026-08-19"),
                    (4, 3, 350.00, "Escape room experiencia", "2026-08-20"),
                    (4, 1, 120.00, "Renta de bicicletas parque", "2026-08-21"),
                    (4, 2, 250.00, "Suscripción a revista/podcast", "2026-08-22"),
                    (4, 3, 750.00, "Entradas a parque de atracciones", "2026-08-23"),
                    (4, 1, 190.00, "Snacks para maratón de películas", "2026-08-24"),
                    (4, 2, 140.00, "Suscripción Max (HBO)", "2026-08-25"),
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