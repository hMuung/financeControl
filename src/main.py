# src/main.py
import flet as ft

from config import APP_ICON_PATH, BASE_DIR
from views.components.background import Background
from views.components.bottom_bar import ModernGlassBottomBar
from views.empty_view import EmptyView
from views.home_view import HomeView
from views.record_view import RecordView


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.platform = ft.PagePlatform.ANDROID
    page.window.resizable = False
    page.padding = 0
    page.spacing = 0

    if APP_ICON_PATH.exists():
        page.window.icon = str(APP_ICON_PATH)

    # Instancias de vistas
    home_view = HomeView()
    record_view = RecordView()

    # Coincidir con items de barra
    page_view = ft.PageView(
        selected_index=0,
        expand=True,
        controls=[
            home_view,
            record_view,
            EmptyView("Proyeccion"),
            EmptyView("Analisis"),
            EmptyView("Mas"),
        ],
    )

    # Auxiliar para recargar la vista del historial
    def check_and_reload(index: int):
        if index == 1:
            record_view.load_history()

    # Clic en la barra -> Cambia el PageView
    def on_bottom_bar_click(index):
        page_view.selected_index = index
        check_and_reload(index)
        page_view.update()

    bottom_bar = ModernGlassBottomBar(on_change=on_bottom_bar_click)

    # Deslizamiento con el dedo en PageView -> Cambia la Barra
    def on_page_swipe(e):
        new_index = (
            int(e.data) if isinstance(e.data, str) else e.control.selected_index
        )
        check_and_reload(new_index)
        bottom_bar.set_selected_index(new_index, notify=False)

    page_view.on_change = on_page_swipe

    safe_content = ft.SafeArea(
        expand=True,
        content=ft.Container(
            padding=ft.Padding.symmetric(vertical=0, horizontal=12),
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

    app_layout = ft.Stack(
        width=page.width,
        height=page.height,
        controls=[
            Background(),
            safe_content,
        ],
    )


    page.add(app_layout)


if __name__ == "__main__":
    ft.run(main, assets_dir=str(BASE_DIR))