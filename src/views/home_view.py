# src/views/home_view.py
import flet as ft
from views.components.common.header import Header
from views.components.quick_expense import QuickExpenseCard
from views.components.quick_income import QuickIncomeCard

class HomeView(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        self.controls = [
            Header(),
            QuickExpenseCard(initially_collapsed=False),
            QuickIncomeCard(initially_collapsed=True)
        ]