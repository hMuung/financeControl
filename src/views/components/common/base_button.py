# src/views/components/common/base_button.py
from typing import Any, Callable
import flet as ft

from src.views.utils.theme import (
    COLOR_BTN_SECONDARY_BG,
    COLOR_BTN_TERTIARY_TEXT,
    GRADIENT_BTN_PRIMARY,
    TEXT_PRIMARY,
)


@ft.control
class BaseButton(ft.Container):

    text: str = ""
    icon: str | None = None
    gradient: ft.LinearGradient | None = None
    bgcolor: str | None = None
    border_color: str | None = None
    text_color: str = TEXT_PRIMARY
    icon_color: str | None = None
    height: float = 40
    width: float = 120
    border_radius: float = 16

    def init(self):
        self.height = self.height
        self.width = self.width
        self.ink=True
        self.border_radius = self.border_radius
        self.alignment = ft.Alignment.CENTER
        self.padding = ft.Padding.symmetric(horizontal=12, vertical=0)
        self.animate = ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT)

        if self.gradient:
            self.gradient = self.gradient
        else:
            self.bgcolor = self.bgcolor or ft.Colors.TRANSPARENT

        if self.border_color:
            self.border = ft.Border.all(1, color=self.border_color)

        row_controls = []
        eff_icon_color = self.icon_color or self.text_color

        if self.icon:
            row_controls.append(
                ft.Icon(
                    icon=self.icon,
                    color=eff_icon_color,
                    size=18,
                )
            )

        row_controls.append(
            ft.Text(
                value=self.text,
                color=self.text_color,
                size=14,
                weight=ft.FontWeight.BOLD,
            )
        )

        self.content = ft.Row(
            controls=row_controls,
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )


def save_button(
    text: str = "Guardar",
    icon: str = ft.Icons.CHECK_ROUNDED,
    on_click: Callable[[Any], None] | None = None
) -> BaseButton:
    btn= BaseButton(
        text=text,
        icon=icon,
        gradient=GRADIENT_BTN_PRIMARY,
        text_color=TEXT_PRIMARY,
    )
    btn.on_click = on_click
    return btn


def cancel_button(
    text: str = "Cancelar",
    icon: str = ft.Icons.CLOSE_ROUNDED,
    on_click: Callable[[Any], None] | None = None,
) -> BaseButton:
    btn = BaseButton(
        text=text,
        icon=icon,
        bgcolor=COLOR_BTN_SECONDARY_BG,
        border_color="#FFFFFF",
        text_color=COLOR_BTN_TERTIARY_TEXT,
    )
    btn.on_click = on_click
    return btn