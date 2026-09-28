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

        # Cargar opciones de categorías y orígenes
        expense_categories = self.category_controller.get_expense_categories()
        expense_origins = self.origin_controller.get_expense_origins()
        income_categories = getattr(self.category_controller, "get_income_categories", lambda: [])()
        income_origins = getattr(self.origin_controller, "get_income_origins", lambda: [])()

        # Instancia de la tabla de Gastos
        self.expenses_glass_table = GastosGlassTable(
            categories_options=self._format_options(expense_categories),
            origins_options=self._format_options(expense_origins),
            on_delete=self.handle_delete_expense,
            on_edit=self.handle_edit_expense,
        )

        # Instancia de la tabla de Ingresos
        self.incomes_glass_table = IngresosGlassTable(
            categories_options=self._format_options(income_categories),
            origins_options=self._format_options(income_origins),
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

    @staticmethod
    def _format_options(items: list) -> list[tuple]:
        return [(item.id, item.name, item.color, item.bg_color) for item in items]

    @staticmethod
    def _format_history(records: list) -> list[dict]:
        return [
            {
                "id": getattr(r, "id", None),
                "date": r.date,
                "category": r.category_name,
                "amount": r.amount,
                "origin": r.origin_name,
                "description": getattr(r, "description", ""),
            }
            for r in records
        ]

    def did_mount(self):
        self.load_expense_history()
        self.load_income_history()

    def load_expense_history(self):
        expenses = self.expense_controller.fetch_history()
        self.expenses_glass_table.update_data(self._format_history(expenses))

    def load_income_history(self):
        incomes = self.income_controller.fetch_history()
        self.incomes_glass_table.update_data(self._format_history(incomes))

    def handle_delete_expense(self, item: dict):
        expense_id = item.get("id")
        if expense_id is not None and hasattr(self.expense_controller, "delete_expense"):
            return self.expense_controller.delete_expense(expense_id)
        return False, "Error al eliminar gasto"

    def handle_edit_expense(self, payload: dict):
        return self.expense_controller.update_expense(
            expense_id=payload.get("id"),
            category_id=payload.get("category_id"),
            amount_str=payload.get("amount_str"),
            origin_id=payload.get("origin_id"),
            description=payload.get("description", ""),
        )

    def handle_delete_income(self, item: dict):
        income_id = item.get("id")
        if income_id is not None and hasattr(self.income_controller, "delete_income"):
            return self.income_controller.delete_income(income_id)
        return False, "Error al eliminar ingreso"

    def handle_edit_income(self, payload: dict):
        return self.income_controller.update_income(
            income_id=payload.get("id"),
            category_id=payload.get("category_id"),
            amount_str=payload.get("amount_str"),
            origin_id=payload.get("origin_id"),
            description=payload.get("description", ""),
        )