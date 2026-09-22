# src/views/components/header.py
import flet as ft

from config import APP_LOGO_PATH

def Header(title: str = "FINANCE CENTRAL", logo_src: str = str(APP_LOGO_PATH)) -> ft.Row:
    "Componente de encabezado"
    return ft.Row(
        controls=[
            ft.Container(
                content=ft.Image(
                    src=logo_src, 
                    width=40,
                    height=40,
                    fit="contain",
                ),
                bgcolor=ft.Colors.TRANSPARENT,
                padding=0,
                border_radius=12,
                alignment=ft.Alignment.CENTER,
            ),
            ft.Text(
                title,
                size=28,
                weight=ft.FontWeight.BOLD,
                color="#2D3748",
            ),
        ],
        spacing=12,
        alignment=ft.MainAxisAlignment.START,
    )