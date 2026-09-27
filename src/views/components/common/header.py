# src/views/components/common/header.py
# src/views/components/header.py
import flet as ft
from config import APP_LOGO_PATH
from views.utils.theme import HEADER_TEXT_COLOR

def Header(
    title: str = "FINANCE CENTRAL", 
    logo_src: str | ft.Control | ft.Icon | None = str(APP_LOGO_PATH),
    title_color: str = HEADER_TEXT_COLOR
) -> ft.Row:
    "Componente de encabezado"
    controls = []

    if logo_src is not None:

        logo_content = None

        # Si ya es un Control
        if isinstance(logo_src, ft.Control):
            logo_content = logo_src

        elif isinstance(logo_src, str):
            # Comprobar si es una ruta de archivo
            is_image_path = (
                any(logo_src.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".svg", ".webp", ".ico"])
            )
            
            if is_image_path:
                logo_content = ft.Image(
                    src=logo_src, 
                    width=40,
                    height=40,
                    fit="contain",
                )
        elif isinstance(logo_src,ft.Icon):
            logo_content = logo_src

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

    # Añadir el titulo
    controls.append(
        ft.Text(
            title,
            size=28,
            weight=ft.FontWeight.BOLD,
            color=title_color,
        )
    )

    return ft.Row(
        controls=controls,
        spacing=12,
        alignment=ft.MainAxisAlignment.START,
    )