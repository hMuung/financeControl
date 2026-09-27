# src/views/record_view.py
import flet as ft

from controllers.expense_controller import ExpenseController
from controllers.income_controller import IncomeController
from controllers.category_controller import CategoryController
from controllers.origin_controller import OriginController
from views.components.expenses_record_table import GastosGlassTable
from views.components.incomes_record_table import IngresosGlassTable
from views.components.common.header import Header
from views.utils.theme import HEADER_TEXT_COLOR


class RecordView(ft.Column):
    def __init__(self):
        self.expense_controller = ExpenseController()
        self.income_controller = IncomeController()
        self.category_controller = CategoryController()
        self.origin_controller = OriginController()

        # Obtener categorías y orígenes de Gastos
        expense_categories = self.category_controller.get_expense_categories()
        expense_origins = self.origin_controller.get_expense_origins()

        # Obtener categorías y orígenes de Ingresos
        income_categories = getattr(self.category_controller, "get_income_categories", lambda: [])()
        income_origins = getattr(self.origin_controller, "get_income_origins", lambda: [])()

        # Formatear opciones para Gastos
        exp_category_options = [
            (cat.id, cat.name, cat.color, cat.bg_color) for cat in expense_categories
        ]
        exp_origin_options = [
            (orig.id, orig.name, orig.color, orig.bg_color) for orig in expense_origins
        ]

        # Formatear opciones para Ingresos
        inc_category_options = [
            (cat.id, cat.name, cat.color, cat.bg_color) for cat in income_categories
        ]
        inc_origin_options = [
            (orig.id, orig.name, orig.color, orig.bg_color) for orig in income_origins
        ]

        # Instancia de la tabla de Gastos
        self.expenses_glass_table = GastosGlassTable(
            title="Gastos",
            categories_options=exp_category_options,
            origins_options=exp_origin_options,
            empty_message="No hay gastos que coincidan.",
            on_delete=self.handle_delete_expense,
            on_edit=self.handle_edit_expense,
        )

        # Instancia de la tabla de Ingresos
        self.incomes_glass_table = IngresosGlassTable(
            title="Ingresos",
            categories_options=inc_category_options,
            origins_options=inc_origin_options,
            empty_message="No hay ingresos que coincidan.",
            on_delete=self.handle_delete_income,
            on_edit=self.handle_edit_income,
        )

        super().__init__(
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                Header(
                    title="Historial",
                    logo_src=ft.Icon(
                        ft.Icons.RECEIPT_LONG_ROUNDED,
                        color=HEADER_TEXT_COLOR,
                        size=28,
                    ),
                ),
                self.expenses_glass_table,
                self.incomes_glass_table,
            ],
        )

    def did_mount(self):
        self.load_expense_history()
        self.load_income_history()

    def load_expense_history(self):
        expenses = self.expense_controller.fetch_history()
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
        self.expenses_glass_table.update_data(table_data)

    def load_income_history(self):
        incomes = self.income_controller.fetch_history()
        table_data = [
            {
                "id": getattr(inc, "id", None),
                "date": inc.date,
                "category": inc.category_name,
                "amount": inc.amount,
                "origin": inc.origin_name,
                "description": getattr(inc, "description", ""),
            }
            for inc in incomes
        ]
        self.incomes_glass_table.update_data(table_data)

    def handle_delete_expense(self, item: dict):
        success, message = False, "Error al eliminar gasto"
        expense_id = item.get("id")
        if expense_id is not None and hasattr(self.expense_controller, "delete_expense"):
            success, message = self.expense_controller.delete_expense(expense_id)
        return success, message

    def handle_edit_expense(self, payload: dict):  
        expense_id = payload.get("id")
        category_id = payload.get("category_id")
        origin_id = payload.get("origin_id")
        amount_str = payload.get("amount_str")
        description = payload.get("description", "")

        success, message = self.expense_controller.update_expense(
            expense_id=expense_id,
            category_id=category_id,
            amount_str=amount_str,
            origin_id=origin_id,
            description=description,
        )
        return success, message

    def handle_delete_income(self, item: dict):
        success, message = False, "Error al eliminar ingreso"
        income_id = item.get("id")
        if income_id is not None and hasattr(self.income_controller, "delete_income"):
            success, message = self.income_controller.delete_income(income_id)
        return success, message

    def handle_edit_income(self, payload: dict):
        income_id = payload.get("id")
        category_id = payload.get("category_id")
        origin_id = payload.get("origin_id")
        amount_str = payload.get("amount_str")
        description = payload.get("description", "")

        success, message = self.income_controller.update_income(
            income_id=income_id,
            category_id=category_id,
            amount_str=amount_str,
            origin_id=origin_id,
            description=description,
        )
        return success, message