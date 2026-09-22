# src/views/empty_view.py
import flet as ft

class EmptyView(ft.Column):
    def __init__(self, message: str = "empty"):
        super().__init__(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.message = message
        self.controls = [
            ft.Text(self.message, size=22, weight=ft.FontWeight.BOLD),
        ]