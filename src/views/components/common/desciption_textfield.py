# src/views/components/common/description_textfield.py
import flet as ft

from src.views.utils.theme import (
    COLOR_ACCENT_BRIGHT,
    COLOR_BG_MAIN,
    TEXT_MUTED,
    TEXT_PRIMARY,
)


@ft.control
class DescriptionTextField(ft.TextField):
    label: str | None = "Descripción (opcional)"
    border_radius: float = 16
    default_fill_color: str = COLOR_BG_MAIN
    focused_color: str = COLOR_ACCENT_BRIGHT
    blur_color: str = TEXT_MUTED

    def init(self):
        self.expand = True
        self.filled = True
        self.dense = True
        self.color = TEXT_PRIMARY
        self.fill_color = self.default_fill_color
        self.content_padding = ft.Padding.symmetric(vertical=10, horizontal=14)
        self.text_size = 14
        self.cursor_color = COLOR_ACCENT_BRIGHT

        self.label_style = ft.TextStyle(color=self.blur_color, size=13)

        self.border = {
            ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                border_radius=self.border_radius,
                side=ft.BorderSide(color=self.blur_color, width=1),
            ),
            ft.ControlState.FOCUSED: ft.OutlineInputBorder(
                border_radius=self.border_radius,
                side=ft.BorderSide(color=self.focused_color, width=1.5),
            ),
        }

    def clean_data(self):
        self.value = ""
        if self.page:
            self.page.update(self)