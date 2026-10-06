# src/views/home_view.py
import flet as ft

from views.components.common.header import Header


@ft.control
class HomeView(ft.Column):
    spacing: int = 10
    scroll: ft.ScrollMode = ft.ScrollMode.HIDDEN
    expand: bool = True

    def init(self):
        self.controls = [
            Header(title="CASH FLOW REGISTER"),
        ]