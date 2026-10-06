# src/main.py
import flet as ft

from config import APP_ICON_PATH, ASSETS_DIR

from views.components.background import Background

from views.empty_view import EmptyView
from views.home_view import HomeView


def main(page: ft.Page):
    page.platform = ft.PagePlatform.ANDROID
    page.window.resizable = False
    page.padding = 0
    page.spacing = 0

    # Configurar iconos de sistema a blanco
    page.theme = ft.Theme(
        system_overlay_style=ft.SystemOverlayStyle(
            status_bar_icon_brightness=ft.Brightness.LIGHT
        )
    )

    if APP_ICON_PATH.exists():
        page.window.icon = str(APP_ICON_PATH)

    # Instancias de vistas
    background = Background()
    home_view = HomeView()

    page_view = ft.PageView(
        selected_index=0,
        expand=True,
        controls=[
            home_view,
            EmptyView(message="Historial"),
            EmptyView(message="Proyeccion"),
            EmptyView(message="Analisis"),
            EmptyView(message="Mas"),
        ],
    )

    app_layout = ft.Stack(
        expand=True,
        controls=[
            background,
            ft.Container(
                expand=True,
                padding=ft.Padding.only(
                    top=0,
                    left=12,
                    right=12,
                    bottom=12
                ),
                content=ft.SafeArea(
                    expand=True,
                    content=page_view,
                )
            ),
        ],
    )

    page.add(app_layout)

    print("New start")


if __name__ == "__main__":
    ft.run(main, assets_dir=str(ASSETS_DIR))