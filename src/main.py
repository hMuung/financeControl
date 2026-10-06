# src/main.py
import flet as ft

from config import APP_ICON_PATH, ASSETS_DIR

from views.components.background import Background
from views.components.page_indicator import PageIndicator

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

    views = [
        HomeView(),
        EmptyView(message="Historial"),
        EmptyView(message="Proyección"),
        EmptyView(message="Análisis"),
        EmptyView(message="Más"),
    ]

    def handle_indicator_select(index: int):
        page_view.selected_index = index

    # Indicador de pagina
    indicator = PageIndicator(
        icons=[
            ft.Icons.HOME_ROUNDED,
            ft.Icons.HISTORY_ROUNDED,
            ft.Icons.SHOW_CHART_ROUNDED,
            ft.Icons.ANALYTICS_ROUNDED,
            ft.Icons.MORE_VERT_ROUNDED,
        ],
        total_width=page.width-24,
        spacing=2,
        icon_size=20,
        selected_index=0,
        on_select_page=handle_indicator_select,

    )

    def handle_page_change(e: ft.ControlEvent):
        indicator.set_selected_index(e.control.selected_index)

    page_view = ft.PageView(
        on_change=handle_page_change,
        selected_index=0,
        expand=True,
        controls=views,
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
                    content=ft.Column(
                        expand=True,
                        spacing=12,
                        controls=[
                            page_view,
                            indicator,
                        ],
                    ),
                )
            ),
        ],
    )

    page.add(app_layout)

    print("New start")


if __name__ == "__main__":
    ft.run(main, assets_dir=str(ASSETS_DIR))