# src/views/empty_view.py
import flet as ft

from views.utils.theme import TEXT_MUTED


@ft.control
class EmptyView(ft.Column):
    message: str = "EMPTY"
    expand: bool = True
    alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.CENTER

    def init(self):
        self.controls = [
            ft.Text(
                self.message,
                size=20,
                weight=ft.FontWeight.BOLD,
                color=TEXT_MUTED,
                text_align=ft.TextAlign.CENTER,
            ),
        ]