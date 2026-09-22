# src/views/home_view.py
import flet as ft
from views.components.common.header import Header
from views.components.quick_expense import QuickExpenseCard

class HomeView(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            expand=True,
        )
        self.controls = [
            Header(),
            QuickExpenseCard(),
        ]