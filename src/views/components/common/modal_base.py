# src/views/components/common/modal_bases.py
import flet as ft
from typing import Optional

from views.utils.theme import (
    GRADIENT_GLASS_CARD,
    GLASS_CARD_SHADOW,
    TEXT_MUTED,
    GLASS_CARD_BORDER_COLOR
)


@ft.control
class ModalBase(ft.AlertDialog):
    body: Optional[ft.Control] = None

    def init(self):
        self.bgcolor = ft.Colors.TRANSPARENT
        self.content_padding = 0
        self.action_button_padding = 0

        # Determinacion del contenido interno
        if not self.body:
            self.body = ft.Container(
                alignment=ft.Alignment.CENTER,
                padding=20,
                content=ft.Text(
                    "Empty",
                    color=TEXT_MUTED,
                    size=16,
                    weight=ft.FontWeight.W_500,
                ),
            )

        # Contenedor de fondo
        self.content = ft.Container(
            padding=ft.Padding.all(18),
            border_radius=20,
            gradient=GRADIENT_GLASS_CARD,
            shadow=GLASS_CARD_SHADOW,
            border=ft.Border.all(1, color=GLASS_CARD_BORDER_COLOR),
            blur=ft.Blur(16, 16, ft.BlurTileMode.CLAMP),
            content=self.body,
        )