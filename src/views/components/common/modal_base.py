# src/views/components/common/custom_modal.py
from dataclasses import field
from typing import Optional
import flet as ft

from views.utils.theme import (
    COLOR_GLASS_BORDER_TOP,
    GRADIENT_GLASS_CARD,
    TEXT_MUTED,
)


@ft.control
class ModalBase(ft.AlertDialog):
    body: Optional[ft.Control] = None

    def init(self):
        # Fondo transparente
        self.bgcolor = ft.Colors.TRANSPARENT
        self.shadow_color = GRADIENT_GLASS_CARD
        self.content_padding = 0
        self.action_button_padding = 0
        

        # Determinacion del contenido interno
        if not self.body:
            self.body = ft.Container(
                width=200,
                height=200,
                alignment=ft.Alignment.CENTER,
                padding=20,
                content=ft.Text(
                    "Empty",
                    color=TEXT_MUTED,
                    size=16,
                    weight=ft.FontWeight.W_500,
                ),
            )

        # Contenedor con efecto Glassmorphism Morado
        self.content = ft.Container(
            expand=True,
            padding=20,
            border_radius=20,
            gradient=GRADIENT_GLASS_CARD,
            border=ft.Border.all(1, COLOR_GLASS_BORDER_TOP),
            blur=ft.Blur(16, 16, ft.BlurTileMode.CLAMP),
            content=self.body,
        )

    def open_dialog(self, page: ft.Page):
        page.show_dialog(self)

    def close_dialog(self, page: ft.Page):
        page.pop_dialog(self)