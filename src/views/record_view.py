# src/views/record.py
import flet as ft

from controllers.expense_controller import ExpenseController
from controllers.category_controller import CategoryController
from controllers.origin_controller import OriginController
from views.components.expenses_record_table import GastosGlassTable
from views.components.common.header import Header
from views.utils.theme import HEADER_TEXT_COLOR


class RecordView(ft.Column):
    def __init__(self):
        self.controller = ExpenseController()
        self.controller = ExpenseController()
        self.category_controller = CategoryController()
        self.origin_controller = OriginController()

        # Obtener datos de la DB
        categories = self.category_controller.get_expense_categories()
        origins = self.origin_controller.get_expense_origins()

        # Obtener datos desde la base de datos
        category_options = [
            (cat.id, cat.name, cat.color, cat.bg_color) for cat in categories
        ]
        
        origin_options = [
            (orig.id, orig.name, orig.color, orig.bg_color) for orig in origins
        ]

        # Instancia de la tabla con los manejadores de eventos
        self.glass_table = GastosGlassTable(
            title="Gastos",
            categories_options=category_options,
            origins_options=origin_options,
            empty_message="No hay gastos que coincidan.",
            on_delete=self.handle_delete_expense,
            on_edit=self.handle_edit_expense,
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
                self.glass_table,
            ],
        )

    def did_mount(self):
        self.load_history()

    def load_history(self):
        expenses = self.controller.fetch_history()
        table_data = [
            {
                "id": getattr(exp, "id", None),
                "date": exp.date,
                "category": exp.category_name,
                "amount": exp.amount,
                "origin": exp.origin_name,
                "description": getattr(exp, "description", ""),  
            }
            for exp in expenses
        ]
        self.glass_table.update_data(table_data)

    def handle_delete_expense(self, item: dict):
        success, message = False, "Error al eliminar gasto"
        
        # Validar que exista el id y no sea None
        expense_id = item.get("id")
        if expense_id is not None and hasattr(self.controller, "delete_expense"):
            success, message = self.controller.delete_expense(expense_id)
                
        return success, message

    def handle_edit_expense(self, payload: dict):  
        expense_id = payload.get("id")
        category_id = payload.get("category_id")
        origin_id = payload.get("origin_id")
        amount_str = payload.get("amount_str")
        description = payload.get("description", "")

        success, message = self.controller.update_expense(
            expense_id=expense_id,
            category_id=category_id,
            amount_str=amount_str,
            origin_id=origin_id,
            description=description,
        )

        return success, message