# src/views/record_view.py
import flet as ft

from controllers.category_controller import CategoryController
from controllers.expense_controller import ExpenseController
from controllers.income_controller import IncomeController
from controllers.origin_controller import OriginController
from views.components.record_table import RecordGlassTable
from views.components.common.header import Header
from views.utils.theme import COLOR_ACCENT_PRIMARY


@ft.control
class RecordView(ft.Stack):
    expand: bool = True

    def init(self):
        self.expense_controller = ExpenseController()
        self.income_controller = IncomeController()
        self.category_controller = CategoryController()
        self.origin_controller = OriginController()

        self.expense_categories = [
            (cat.id, cat.name)
            for cat in self.category_controller.get_expense_categories()
            if cat.id is not None
        ]

        self.income_categories = [
            (cat.id, cat.name)
            for cat in self.category_controller.get_income_categories()
            if cat.id is not None
        ]

        self.origins = [
            (orig.id, orig.name)
            for orig in self.origin_controller.get_all_origins()
            if orig.id is not None
        ]

        self.columns_config = [
            {"label": "Fecha", "key": "date", "expand": 2, "is_date": True},
            {"label": "Categoría", "key": "category", "expand": 4},
            {"label": "Origen", "key": "origin", "expand": 2},
            {"label": "Monto", "key": "amount", "expand": 2, "numeric": True},
        ]

        self.expenses_list_view = RecordGlassTable(
            title="Gastos",
            detail_title="Detalle del Gasto",
            edit_title="Editar Gasto",
            filter_title="Filtrar Gastos",
            columns_config=self.columns_config,
            data=self._get_formatted_expenses(),
            categories_options=self.expense_categories,
            origins_options=self.origins,
            empty_message="No hay gastos registrados.",
            on_delete=self._handle_delete_expense,
            on_edit=self._handle_edit_expense,
            minimized_height=54,
            collapsed_height=360,
            expanded_height=600,
        )

        self.incomes_list_view = RecordGlassTable(
            title="Ingresos",
            detail_title="Detalle del Ingreso",
            edit_title="Editar Ingreso",
            filter_title="Filtrar Ingresos",
            columns_config=self.columns_config,
            data=self._get_formatted_incomes(),
            categories_options=self.income_categories,
            origins_options=self.origins,
            empty_message="No hay ingresos registrados.",
            on_delete=self._handle_delete_income,
            on_edit=self._handle_edit_income,
            minimized_height=54,
            collapsed_height=360,
            expanded_height=600,
        )

        main_content = ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[
                ft.Column(
                    spacing=0,
                    tight=True,
                    controls=[
                        Header(
                            title="Historial",
                            logo_src=ft.Icons.HISTORY_ROUNDED,
                        ),
                        ft.Divider(
                            color=COLOR_ACCENT_PRIMARY,
                            height=2,
                        ),
                    ],
                ),
                self.expenses_list_view,
                self.incomes_list_view,
            ],
        )

        self.controls = [main_content]

    def _get_formatted_expenses(self) -> list[dict]:
        expenses_raw = self.expense_controller.fetch_history()
        cat_dict = dict(self.expense_categories)
        orig_dict = dict(self.origins)

        formatted = []
        for item in expenses_raw:
            cat_id = getattr(item, "category_id", None)
            orig_id = getattr(item, "origin_id", None)

            cat_name = (
                getattr(item, "category_name", None)
                or getattr(getattr(item, "category", None), "name", None)
                or cat_dict.get(cat_id, "Desconocida")
            )
            orig_name = (
                getattr(item, "origin_name", None)
                or getattr(getattr(item, "origin", None), "name", None)
                or orig_dict.get(orig_id, "Desconocido")
            )

            formatted.append({
                "id": getattr(item, "id", None),
                "date": getattr(item, "date", getattr(item, "created_at", "")),
                "category": cat_name,
                "category_id": cat_id,
                "origin": orig_name,
                "origin_id": orig_id,
                "amount": getattr(item, "amount", 0.0),
                "description": getattr(item, "description", ""),
            })

        return formatted

    def _get_formatted_incomes(self) -> list[dict]:
        incomes_raw = self.income_controller.fetch_history()
        cat_dict = dict(self.income_categories)
        orig_dict = dict(self.origins)

        formatted = []
        for item in incomes_raw:
            cat_id = getattr(item, "category_id", None)
            orig_id = getattr(item, "origin_id", None)

            cat_name = (
                getattr(item, "category_name", None)
                or getattr(getattr(item, "category", None), "name", None)
                or cat_dict.get(cat_id, "Desconocida")
            )
            orig_name = (
                getattr(item, "origin_name", None)
                or getattr(getattr(item, "origin", None), "name", None)
                or orig_dict.get(orig_id, "Desconocido")
            )

            formatted.append({
                "id": getattr(item, "id", None),
                "date": getattr(item, "date", getattr(item, "created_at", "")),
                "category": cat_name,
                "category_id": cat_id,
                "origin": orig_name,
                "origin_id": orig_id,
                "amount": getattr(item, "amount", 0.0),
                "description": getattr(item, "description", ""),
            })

        return formatted

    def _handle_delete_expense(self, item: dict) -> tuple[bool, str]:
        expense_id = item.get("id")
        return self.expense_controller.delete_expense(expense_id)

    def _handle_edit_expense(self, payload: dict) -> tuple[bool, str]:
        return self.expense_controller.update_expense(
            expense_id=payload.get("id"),
            category_id=payload.get("category_id"),
            amount_str=payload.get("amount_str"),
            origin_id=payload.get("origin_id"),
            description=payload.get("description", ""),
        )

    def _handle_delete_income(self, item: dict) -> tuple[bool, str]:
        income_id = item.get("id")
        return self.income_controller.delete_income(income_id)

    def _handle_edit_income(self, payload: dict) -> tuple[bool, str]:
        return self.income_controller.update_income(
            income_id=payload.get("id"),
            category_id=payload.get("category_id"),
            amount_str=payload.get("amount_str"),
            origin_id=payload.get("origin_id"),
            description=payload.get("description", ""),
        )

    def did_mount(self):
        print("update table data")
        if ExpenseController.is_dirty():
            self.expenses_list_view.update_data(self._get_formatted_expenses())
            ExpenseController.mark_clean()

        if IncomeController.is_dirty():
            self.incomes_list_view.update_data(self._get_formatted_incomes())
            IncomeController.mark_clean()
