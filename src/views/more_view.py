# src/views/record_view.py
import flet as ft

from controllers.expense_controller import ExpenseController
from views.components.common.glass_table import GlassDataTable
from views.components.common.header import Header
from views.utils.theme import HEADER_TEXT_COLOR


class RecordView(ft.Column):
    def __init__(self):
        self.controller = ExpenseController()

        # Definición flexible de las columnas
        columns_config = [
            {"label": "Fecha", "key": "date", "numeric": False},
            {"label": "Categoría", "key": "category", "numeric": False},
            {"label": "Monto", "key": "amount", "numeric": True},
            {"label": "Origen", "key": "origin", "numeric": False},
        ]

        # Instancia de la tabla estilizada reutilizable
        self.glass_table = GlassDataTable(
            columns_config=columns_config,
            empty_message="No hay gastos registrados aún.",
        )

        super().__init__(
            spacing=10,
            expand=True,
            controls=[
                Header(
                    title="Historial",
                    logo_src=ft.Icon(
                        ft.Icons.RECEIPT_LONG_ROUNDED,
                        color=HEADER_TEXT_COLOR,
                        size=28,
                    ),
                ),
                self.glass_table,  # <--- Agregamos el componente reutilizable
            ],
        )

    def did_mount(self):
        self.load_history()

    def load_history(self):
        """Obtiene las entidades Expense del controller y las pasa en formato dict a la tabla."""
        expenses = self.controller.fetch_history()

        # Mapeo de objetos Expense a lista de dicts
        table_data = [
            {
                "date": exp.date,
                "category": exp.category,
                "amount": exp.amount,
                "origin": exp.origin,
            }
            for exp in expenses
        ]

        self.glass_table.update_data(table_data)