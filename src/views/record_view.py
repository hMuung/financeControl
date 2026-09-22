# src/views/record.py
import flet as ft

from controllers.expense_controller import ExpenseController  # <--- Controlador
from views.components.common.header import Header
from views.utils.theme import HEADER_TEXT_COLOR


class RecordView(ft.Column):
    def __init__(self):
        self.controller = ExpenseController()

        # Contenedor desplazable para la lista de textos
        self.history_container = ft.Column(
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        super().__init__(
            spacing=10,
            expand=True,
            controls=[
                Header(
                    title="Historial",
                    logo_src=ft.Icon(
                        ft.Icons.RECEIPT_LONG_ROUNDED,
                        color=HEADER_TEXT_COLOR,
                        size=28,
                    ),
                ),
                self.history_container,
            ],
        )

    def did_mount(self):
        """El componente entra en pantalla"""
        self.load_history()

    def load_history(self):
        """Obtiene las entidades Expense desde el controlador y las renderiza"""
        expenses = self.controller.fetch_history()

        self.history_container.controls.clear()

        if not expenses:
            self.history_container.controls.append(
                ft.Text("No hay registros guardados", color=ft.Colors.GREY_500, size=14)
            )
        else:
            for exp in expenses:
                # Formato de texto simple con las propiedades del modelo Expense
                text_line = f"• [{exp.date}] {exp.category} - ${exp.amount:.2f} ({exp.origin})"
                
                self.history_container.controls.append(
                    ft.Text(value=text_line, size=14, color=ft.Colors.WHITE)
                )

        self.update()