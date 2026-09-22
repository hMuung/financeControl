# src/main.py
import flet as ft

from config import BASE_DIR, APP_ICON_PATH
from views.components.background import Background
from views.components.bottom_bar import ModernGlassBottomBar

from views.home_view import HomeView
from views.record_view import RecordView
from views.empty_view import EmptyView

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    if APP_ICON_PATH.exists():
        page.window.icon = str(APP_ICON_PATH)

    # Coincidir con items de barra
    page_view = ft.PageView(
        selected_index=0,
        expand=True,
        controls=[
            HomeView(),
            RecordView(),
            EmptyView("Proyeccion"),
            EmptyView("Analisis"),
            EmptyView("Mas"),
        ],
    )

    # Clic en la barra -> Cambia el PageView
    def on_bottom_bar_click(index):
        page_view.selected_index = index
        page_view.update()

    bottom_bar = ModernGlassBottomBar(on_change=on_bottom_bar_click)

    # Deslizamiento con el dedo en PageView -> Cambia la Barra
    def on_page_swipe(e):
        new_index = int(e.data) if isinstance(e.data, str) else e.control.selected_index
        bottom_bar.set_selected_index(new_index, notify=False)

    page_view.on_change = on_page_swipe

    safe_content = ft.SafeArea(
        expand=True,
        content=ft.Container(
            padding=16,
            content=ft.Column(
                controls=[
                    page_view,
                    bottom_bar,
                ],
                spacing=10,
                expand=True,
            ),
        ),
    )

    page.overlay.extend([Background(), safe_content])

if __name__ == "__main__":
    ft.run(main, assets_dir=str(BASE_DIR))