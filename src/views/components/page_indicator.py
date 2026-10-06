# src/views/components/page_indicator.py
import flet as ft
from dataclasses import field
from typing import Optional, Callable

from views.utils.theme import (
    COLOR_ACCENT_PRIMARY,
    TEXT_DISABLED,
    TEXT_MUTED,
    TEXT_PRIMARY,
)


@ft.control
class PageIndicator(ft.Container):
    icons: list[str] = field(default_factory=list)
    bar_height: int = 4
    total_width: int = 300
    selected_index: int = 0
    spacing: int = 6
    icon_size: int = 18
    on_select_page: Optional[Callable[[int], None]] = None

    def init(self):
        self.width = self.total_width
        self.alignment = ft.Alignment.CENTER

        count = len(self.icons)
        available_width = self.total_width - (self.spacing * count)
        self.indicators_width = available_width / max(1, count)
        
        self.lines: list[ft.Container] = self._build_lines()
        self.icon_controls: list[ft.Container] = self._build_icons()

        self.lines_row = ft.Row(
            spacing=self.spacing,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=self.lines
        )

        self.icons_row = ft.Row(
            spacing=self.spacing,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=self.icon_controls
        )

        self.content = ft.Stack(
            alignment=ft.Alignment.CENTER,
            controls=[
                self.lines_row,
                self.icons_row
            ]
        )


    def _build_lines(self) -> list[ft.Container]:
        lines = []
        for i in range(len(self.icons)):
            is_active = i == self.selected_index
            line_color = COLOR_ACCENT_PRIMARY if is_active else TEXT_DISABLED

            lines.append(
                ft.Container(
                    height=self.bar_height,
                    width=self.indicators_width,
                    border_radius=2,
                    bgcolor=line_color,
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
                )
            )
        return lines

    def _build_icons(self) -> list[ft.Icon]:
        icons = []
        for i, icon_name in enumerate(self.icons):
            is_active = i == self.selected_index
            icon_color = TEXT_PRIMARY if is_active else TEXT_MUTED

            # Callback para capturar el click
            def handle_click(e, index=i):
                self.set_selected_index(index)
                if self.on_select_page:
                    self.on_select_page(index)

            icons.append(
                ft.Container(
                    width=self.indicators_width,
                    alignment=ft.Alignment.CENTER,
                    on_click=handle_click,
                    content=ft.Icon(
                        icon=icon_name,
                        size=self.icon_size,
                        color=icon_color,
                    )
                )
            )

        return icons

    def set_selected_index(self, index: int):
        self.selected_index = index
        for i in range(len(self.icons)):
            is_active = i == self.selected_index
            line_color = COLOR_ACCENT_PRIMARY if is_active else TEXT_DISABLED
            icon_color = TEXT_PRIMARY if is_active else TEXT_MUTED

            if i < len(self.lines):
                self.lines[i].bgcolor = line_color
            if i < len(self.icon_controls):
                self.icon_controls[i].content.color = icon_color