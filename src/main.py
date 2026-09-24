# src/main.py
import flet as ft
import os
from pathlib import Path

from config import APP_ICON_PATH, BASE_DIR, DB_NAME

from views.components.background import Background
from views.components.bottom_bar import ModernGlassBottomBar

from views.empty_view import EmptyView
from views.home_view import HomeView
from views.record_view import RecordView

from services.category_service import CategoryService
from services.origin_service import OriginService
from services.expense_service import ExpenseService


def init_database():
    """Elimina la DB existente y la vuelve a instanciar con sus seeds"""
    db_path = Path(DB_NAME)

    # Eliminar archivo de la DB si existe
    if db_path.exists():
        try:
            os.remove(db_path)
            print(f"[DEV] Base de datos '{DB_NAME}' eliminada para Hot Reload.")
        except Exception as e:
            print(f"[DEV] Error al borrar la base de datos: {e}")

    # Eliminar archivos temporales de SQLite si se crearon (WAL / SHM)
    for extra in [Path(f"{DB_NAME}-wal"), Path(f"{DB_NAME}-shm")]:
        if extra.exists():
            os.remove(extra)

    """Inicializa la DB y carga las seeds en el orden de dependencias"""
    CategoryService()._seed_if_empty()
    OriginService()._seed_if_empty()
    ExpenseService()._seed_if_empty()


def main(page: ft.Page):

    init_database()

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