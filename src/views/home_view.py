# src/views/home_view.py
import flet as ft

from views.components.common.floating_button import FloatingButton
from views.components.common.header import Header

from views.components.balance_card import BalanceCard

from views.utils.theme import COLOR_ACCENT_PRIMARY


@ft.control
class HomeView(ft.Stack):
    expand: bool = True
    def init(self):
           
        # Instancia del control
        card = BalanceCard(
        ingresos=2500.00,
        egresos=1000.50,
        title="Ingresos vs Egresos (Octubre)",
    )

        # Contenido principal
        main_content = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
            controls=[
                Header(
                    title="CASH FLOW REGISTER",
                    logo_src=ft.Icons.ATTACH_MONEY_ROUNDED
                ),
                ft.Divider(
                    color=COLOR_ACCENT_PRIMARY,
                    height=2
                ),
                card
            ],
        )

        # Boton flotante
        floating_button = FloatingButton(
            icon=ft.Icons.ADD,
            on_click=self._handle_floating_button_click,
        )

        floating_button_column = ft.Column(
            controls=[
                floating_button,
                ft.Container( # Spacing container
                    height=0,
                    width=float("inf")
                )
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.END
        )
        

        self.controls = [
            main_content,
            floating_button_column
        ]

    def _handle_floating_button_click(self, e: ft.ControlEvent):
        pass
