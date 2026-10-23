# src/views/components/common/base_record_table.py
from dataclasses import field
import math
from typing import Any, Optional

import flet as ft

from views.components.common.glass_table import GlassDataTable
from views.components.common.modal_base import ModalBase
from views.utils.toast import Toast
from views.utils.theme import (
    COLOR_ACCENT_BRIGHT,
    COLOR_ACCENT_PRIMARY,
    COLOR_BTN_SECONDARY_BG,
    COLOR_BTN_SECONDARY_BORDER,
    COLOR_BTN_SECONDARY_TEXT,
    COLOR_SURFACE_CARD,
    EXPENSE_COLOR,
    GRADIENT_BTN_PRIMARY,
    INPUT_BG_IDLE,
    INPUT_BORDER_FOCUS,
    INPUT_BORDER_IDLE,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


@ft.control
class RecordGlassTable(GlassDataTable):

    detail_title: str = "Detalles del registro"
    edit_title: str = "Edición de registro"
    filter_title: str = "Filtrar"
    categories_options: list = field(default_factory=list)
    origins_options: list = field(default_factory=list)
    on_delete: Any = None
    on_edit: Any = None

    def init(self):

        self.btn_filter = ft.IconButton(
            icon=ft.Icons.FILTER_LIST,
            icon_color=COLOR_ACCENT_BRIGHT,
            icon_size=25,
            tooltip="Abrir Filtros",
            on_click=self._open_filter_modal,
        )
        self.btn_filter
        self.on_row_click = self._open_detail_modal

        super().init()

        self._init_detail_modal()
        #self._init_edit_modal()
        #self._init_filter_modal()
        #self._update_amount_filter_range()

    # Helpers de apertura y cierre de modales
    def _open_modal(self, modal: ModalBase):
        if self.page:
            self.page.show_dialog(modal)

    def _close_modal(self):
        if self.page:
            self.page.pop_dialog()

    # Componentes visuales secundarios
    def _build_modal_header(self, title: str, modal: Optional[ModalBase]) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    title,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color=TEXT_MUTED,
                    icon_size=20,
                    tooltip="Cerrar",
                    on_click=lambda e: self._close_modal()
                ),
            ],
        )


    # Inicialización de Modales
    def _init_detail_modal(self):
        # Controles reutilizables para el detalle
        self.detail_txt_date = ft.Text(size=15, weight=ft.FontWeight.W_500, color=TEXT_PRIMARY)
        self.detail_txt_category = ft.Text(size=15, weight=ft.FontWeight.W_500, color=TEXT_PRIMARY)
        self.detail_txt_amount = ft.Text(size=15, weight=ft.FontWeight.W_500, color=TEXT_PRIMARY)
        self.detail_txt_origin = ft.Text(size=15, weight=ft.FontWeight.W_500, color=TEXT_PRIMARY)
        self.detail_txt_description = ft.Text(size=14)

        self.detail_modal_content = ft.Column(
            spacing=12,
            tight=True,
            controls=[
                self._build_info_row("Fecha:", self.detail_txt_date),
                self._build_info_row("Categoría:", self.detail_txt_category),
                self._build_info_row("Monto:", self.detail_txt_amount),
                self._build_info_row("Origen:", self.detail_txt_origin),
                ft.Divider(height=1, color=COLOR_ACCENT_PRIMARY),
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Descripción:", size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        self.detail_txt_description,
                    ],
                ),
            ],
        )

        detail_modal_action_buttons = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
            controls=[
                
            ],
        )

        modal_body = ft.Column(
            tight=True,
            spacing=14,
            controls=[
                self._build_modal_header(self.detail_title, None),
                self.detail_modal_content,
                detail_modal_action_buttons,
            ],
        )

        self.detail_modal = ModalBase(body=modal_body)
        modal_body.controls[0] = self._build_modal_header(self.detail_title, self.detail_modal)

   
    # Calculo y rangos de datos
    def _get_max_amount(self) -> float:
        if not self.data:
            return 100.0
        amounts = [self._parse_amount(item.get("amount", 0)) for item in self.data]
        max_val = max(amounts) if amounts else 0.0
        return float(math.ceil(max_val)) if max_val > 0 else 100.0

    # Manejo de apertura de modales
    def _open_filter_modal(self, e=None):
        print("open")

    def _open_detail_modal(self, e, item: dict):
        self.selected_item = item
        num_val = self._parse_amount(item.get("amount", 0))

        # Actualización de valores sin recrear los controles
        self.detail_txt_date.value = self._format_date(item.get("date", ""), short_year=False)
        self.detail_txt_category.value = str(item.get("category", "-"))
        self.detail_txt_amount.value = f"${int(round(num_val)):,}"
        self.detail_txt_origin.value = str(item.get("origin", "-"))

        desc = item.get("description")
        self.detail_txt_description.value = str(desc or "Sin descripción")
        self.detail_txt_description.color = TEXT_SECONDARY if desc else TEXT_MUTED
        self.detail_txt_description.italic = not bool(desc)

        self._open_modal(self.detail_modal)

    def _build_info_row(self, label: str, value_control: ft.Control) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, size=15, weight=ft.FontWeight.BOLD, color=TEXT_SECONDARY),
                value_control,
            ],
        )

   


    def update_data(self, new_data: list[dict]):
        super().update_data(new_data)
        #self._update_amount_filter_range()
        if self.page:
            self.update()