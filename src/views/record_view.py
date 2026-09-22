# src/views/record.py
import flet as ft
from views.components.common.header import Header
from views.utils.theme import HEADER_TEXT_COLOR

class RecordView(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            expand=True,
        )
        self.controls = [
            Header(
                title="Historial",
                logo_src=ft.Icon(
                    ft.Icons.RECEIPT_LONG_ROUNDED,
                    color=HEADER_TEXT_COLOR,
                    size=28,
                )
            )
        ]