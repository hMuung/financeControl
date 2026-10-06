# src/main.py
import flet as ft
import sqlite3

from config import APP_ICON_PATH, DB_NAME, ASSETS_DIR

from views.components.background import Background
from views.components.bottom_bar import ModernGlassBottomBar

from views.empty_view import EmptyView
from views.home_view import HomeView
from views.record_view import RecordView

from controllers.expense_controller import ExpenseController
from controllers.income_controller import IncomeController


def reset_database():

    """Limpia las tablas para forzar a los servicios a recrearlas y re-sembrar."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Elimina las tablas existentes
            cursor.execute("DROP TABLE IF EXISTS categories")
            cursor.execute("DROP TABLE IF EXISTS origins")
            cursor.execute("DROP TABLE IF EXISTS expenses")
            cursor.execute("DROP TABLE IF EXISTS incomes")
            conn.commit()
            print("Tablas reiniciadas con éxito.")
    except sqlite3.OperationalError as e:
        print(f"No se pudieron reiniciar las tablas: {e}")


def main(page: ft.Page):

    #reset_database()

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
        is_exp_dirty = ExpenseController.is_dirty()
        is_inc_dirty = IncomeController.is_dirty()

        if is_exp_dirty or is_inc_dirty:

            if index == 0:
                home_view.refresh_summary()

            if index == 1:
                if is_exp_dirty:
                    record_view.load_expense_history()
                if is_inc_dirty:
                    record_view.load_income_history()

            ExpenseController.mark_clean()
            IncomeController.mark_clean()


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
        #bottom_bar.set_selected_index(new_index, notify=False)

    page_view.on_change = on_page_swipe

    safe_content = ft.SafeArea(
        expand=True,
        content=ft.Container(
            padding=ft.Padding.symmetric(vertical=0, horizontal=12),
            content=ft.Column(
                controls=[
                    page_view,
                    #bottom_bar,
                ],
                spacing=10,
                expand=True,
            ),
        ),
    )

    app_layout_s = ft.Stack(
        expand=True,
        controls=[
            safe_content,
        ],
    )

    app_layout = ft.Stack(
        expand=True,
        #width=page.width,
        #height=page.height,
        controls=[
            Background(),
            app_layout_s,
        ],
    )


    page.add(app_layout)


if __name__ == "__main__":
    ft.run(main, assets_dir=str(ASSETS_DIR))