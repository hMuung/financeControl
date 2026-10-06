# src/views/components/common/header.py
import flet as ft

from config import APP_LOGO_PATH
from views.utils.theme import TEXT_PRIMARY


@ft.control
class Header(ft.Row):
    title: str = "EMPTY"
    logo_src: str | ft.Control | None = str(APP_LOGO_PATH)
    title_color: str = TEXT_PRIMARY
    spacing: int = 12
    alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START

    def init(self):
        controls = []

        if self.logo_src is not None:
            logo_content = None

            if isinstance(self.logo_src, ft.Control):
                logo_content = self.logo_src
            elif isinstance(self.logo_src, str):
                is_image_path = any(
                    self.logo_src.lower().endswith(ext)
                    for ext in [".png", ".jpg", ".jpeg", ".svg", ".webp", ".ico"]
                )
                if is_image_path:
                    logo_content = ft.Image(
                        src=self.logo_src,
                        width=40,
                        height=40,
                        fit=ft.BoxFit.CONTAIN,
                    )

            if logo_content:
                controls.append(
                    ft.Container(
                        content=logo_content,
                        bgcolor=ft.Colors.TRANSPARENT,
                        padding=0,
                        border_radius=12,
                        alignment=ft.Alignment.CENTER,
                    )
                )

        controls.append(
            ft.Text(
                self.title,
                size=28,
                weight=ft.FontWeight.BOLD,
                color=self.title_color,
            )
        )

        self.controls = controls