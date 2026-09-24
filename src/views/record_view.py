# src/views/record.py
import flet as ft

from controllers.expense_controller import ExpenseController
from views.components.glass_table import GlassDataTable
from views.components.common.header import Header
from views.utils.theme import HEADER_TEXT_COLOR


class RecordView(ft.Column):
    def __init__(self):
        self.controller = ExpenseController()

        # Instancia de la tabla con los manejadores de eventos
        self.glass_table = GlassDataTable(
            title="Gastos",
            categories_options=["Comida", "Transporte", "Servicios", "Hogar", "Entretenimiento"],
            origins_options=["Efectivo", "Tarjeta de Débito", "Tarjeta de Crédito"],
            empty_message="No hay gastos que coincidan con los filtros.",
            min_amount_limit=0.0,
            max_amount_limit=5000.0,
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
            if success:
                self.load_history()  # Recargar datos si se eliminó con éxito
                
        return success, message

    def handle_edit_expense(self, item: dict):  
        pass

    def save_edited_expense(self, updated_item: dict):
        pass