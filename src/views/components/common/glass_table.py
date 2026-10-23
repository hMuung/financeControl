# src/views/components/common/glass_table.py
from dataclasses import field
from typing import Any, Optional
import flet as ft

from views.utils.theme import (
    COLOR_ACCENT_BRIGHT,
    GLASS_CARD_BORDER_COLOR,
    GLASS_CARD_SHADOW,
    GRADIENT_GLASS_CARD,
    INPUT_BORDER_IDLE,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


@ft.control
class GlassDataTable(ft.Container):
    title: str = "Registros"
    title_size: int = 20
    icon_size: int = 30
    columns_config: list[dict] = field(default_factory=list)
    data: list[dict] = field(default_factory=list)
    empty_message: str = "No hay datos registrados."
    on_row_click: Any = None
    action_button: Optional[ft.Control] = None
    minimized_height: float = 54.0
    collapsed_height: float = 380.0
    expanded_height: float = 650.0

    def init(self):
        # Estados de control de la interfaz
        self.selected_item = None
        self.is_minimized = True
        self.is_expanded = False

        # Configuración del Container base
        self.height = self.minimized_height
        self.gradient = GRADIENT_GLASS_CARD
        self.border = ft.Border.all(1, GLASS_CARD_BORDER_COLOR)
        self.border_radius = 16
        self.shadow = GLASS_CARD_SHADOW
        self.padding = ft.Padding.symmetric(vertical=0, horizontal=5)
        self.animate_size = ft.Animation(250, ft.AnimationCurve.EASE_OUT)

        # Componentes base
        self.header_row = self._build_header_row()
        self.empty_control = self._build_empty_control()

        self.list_view = ft.ListView(
            expand=True,
            spacing=2,
            padding=ft.Padding.symmetric(vertical=4, horizontal=2),
            build_controls_on_demand=True,
            first_item_prototype=True,
            controls=self._build_rows(),
        )

        self.title_text_control = ft.Text(
            value=f"{self.title} ({len(self.data)})",
            size=self.title_size,
            weight=ft.FontWeight.BOLD,
            color=TEXT_PRIMARY,
        )

        # Botón para alternar solo barra (Minimizar / Desplegar)
        self.btn_minimize = ft.IconButton(
            icon=ft.Icons.KEYBOARD_ARROW_DOWN,
            icon_color=COLOR_ACCENT_BRIGHT,
            icon_size=self.icon_size,
            tooltip="Desplegar",
            on_click=self._toggle_minimize,
        )

        # Botón para alternar tamaño de apertura (Normal / Pantalla Máxima)
        self.btn_size_toggle = ft.IconButton(
            icon=ft.Icons.FULLSCREEN,
            icon_color=COLOR_ACCENT_BRIGHT,
            icon_size=self.icon_size,
            tooltip="Expandir",
            on_click=self._toggle_size,
        )

        # Agrupación de controles de la cabecera
        action_controls = []
        if self.action_button:
            action_controls.append(self.action_button)

        action_controls.extend([self.btn_size_toggle, self.btn_minimize])

        header_actions_row = ft.Row(
            controls=action_controls,
            spacing=2,
            alignment=ft.MainAxisAlignment.END,
        )

        header_controls = [
            ft.Container(width=4),
            self.title_text_control,
            ft.Container(expand=True),
            header_actions_row,
        ]

        self.table_container = ft.Container(
            content=self.list_view,
            border_radius=10,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            expand=True,
        )

        self.content = ft.Column(
            spacing=4,
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=header_controls,
                ),
                self.header_row,
                self.table_container,
            ],
        )

        self._apply_state()

    def _apply_state(self):
        if self.is_minimized:
            self.height = self.minimized_height
            self.header_row.visible = False
            self.table_container.visible = False

            self.btn_minimize.icon = ft.Icons.KEYBOARD_ARROW_DOWN
            self.btn_minimize.tooltip = "Desplegar"
            self.btn_size_toggle.visible = False
            if self.action_button:
                self.action_button.visible = False
        else:
            self.header_row.visible = True
            self.table_container.visible = True
            self.btn_minimize.icon = ft.Icons.KEYBOARD_ARROW_UP
            self.btn_minimize.tooltip = "Colapsar a barra"
            self.btn_size_toggle.visible = True
            if self.action_button:
                self.action_button.visible = True

            if self.is_expanded:
                self.height = self.expanded_height
                self.btn_size_toggle.icon = ft.Icons.FULLSCREEN_EXIT
            else:
                self.height = self.collapsed_height
                self.btn_size_toggle.icon = ft.Icons.FULLSCREEN

    def _toggle_minimize(self, e):
        self.is_minimized = not self.is_minimized
        self._apply_state()
        self.update()

    def _toggle_size(self, e):
        self.is_expanded = not self.is_expanded
        self._apply_state()
        self.update()

    def _get_page(self, e=None):
        if e and hasattr(e, "page") and e.page:
            return e.page
        return self.page

    @staticmethod
    def _parse_amount(val) -> float:
        if val is None:
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)
        s = str(val).replace("$", "").replace(",", "").strip()
        try:
            return float(s)
        except ValueError:
            return 0.0

    @staticmethod
    def _format_date(val, short_year: bool = False) -> str:
        if not val:
            return ""
        val_str = str(val).strip()
        try:
            clean_val = val_str.split("T")[0].split(" ")[0]
            parts = clean_val.split("-")
            if len(parts) == 3 and len(parts[0]) == 4:
                year = parts[0][-2:] if short_year else parts[0]
                return f"{parts[2]}/{parts[1]}/{year}"
        except Exception:
            pass
        return val_str

    def _update_title_count(self, count: int = None):
        if count is not None:
            self.title_text_control.value = f"{self.title} ({count})"
        else:
            self.title_text_control.value = f"{self.title} ({len(self.data)})"

    def _build_header_row(self) -> ft.Container:
        header_controls = []
        for idx, col in enumerate(self.columns_config):
            # Línea divisora vertical entre títulos
            if idx > 0:
                header_controls.append(
                    ft.Container(
                        width=1,
                        height=14,
                        bgcolor=INPUT_BORDER_IDLE,
                    )
                )

            header_controls.append(
                ft.Container(
                    content=ft.Text(
                        col["label"],
                        weight=ft.FontWeight.BOLD,
                        size=12,
                        color=TEXT_SECONDARY,
                        text_align=ft.TextAlign.RIGHT if col.get("numeric") else ft.TextAlign.LEFT,
                    ),
                    alignment=ft.Alignment.CENTER_RIGHT if col.get("numeric") else ft.Alignment.CENTER_LEFT,
                    expand=col.get("expand", 1),
                )
            )

        return ft.Container(
            content=ft.Row(
                controls=header_controls,
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#1AFFFFFF",  # Translúcido blanco suave para la cabecera
            padding=ft.Padding.symmetric(vertical=8, horizontal=10),
            border_radius=8,
        )

    def _build_empty_control(self) -> ft.Container:
        return ft.Container(
            content=ft.Text(
                self.empty_message,
                color=TEXT_MUTED,
                italic=True,
                size=12,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.Alignment.CENTER,
            padding=20,
        )

    def _build_single_row(self, item: dict) -> ft.Container:
        cells = []
        for col in self.columns_config:
            key = col["key"]
            val = item.get(key, "")

            if key == "date" or col.get("is_date"):
                text_val = self._format_date(val, short_year=True)
            elif col.get("numeric"):
                num_val = self._parse_amount(val)
                text_val = f"${int(round(num_val)):,}"
            else:
                text_val = str(val) if val is not None else ""

            cells.append(
                ft.Container(
                    content=ft.Text(
                        text_val,
                        size=12,
                        color=TEXT_PRIMARY,
                        weight=ft.FontWeight.W_500 if col.get("numeric") else ft.FontWeight.NORMAL,
                        text_align=ft.TextAlign.RIGHT if col.get("numeric") else ft.TextAlign.LEFT,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    alignment=ft.Alignment.CENTER_RIGHT if col.get("numeric") else ft.Alignment.CENTER_LEFT,
                    expand=col.get("expand", 1),
                )
            )

        # Fila con borde inferior como línea divisora horizontal
        row_container = ft.Container(
            content=ft.Row(controls=cells, spacing=10),
            padding=ft.Padding.symmetric(vertical=8, horizontal=10),
            border_radius=6,
            border=ft.Border.only(bottom=ft.BorderSide(1, INPUT_BORDER_IDLE)),
            ink=True,
            on_long_press=lambda e, data_item=item: self._handle_row_click(e, data_item),
        )

        row_container.data = item.get("id")
        row_container.item_data = item
        return row_container

    def _handle_row_click(self, e, item: dict):
        self.selected_item = item
        if self.on_row_click:
            self.on_row_click(e, item)

    def _build_rows(self) -> list[ft.Control]:
        controls = [self._build_single_row(item) for item in self.data]
        self.empty_control.visible = len(self.data) == 0
        controls.append(self.empty_control)
        return controls

    def _update_row_cells(self, row_ctrl: ft.Container, item: dict):
        if not hasattr(row_ctrl, "content") or not isinstance(row_ctrl.content, ft.Row):
            return

        row_cells = row_ctrl.content.controls
        for idx, col in enumerate(self.columns_config):
            key = col["key"]
            val = item.get(key, "")

            if key == "date" or col.get("is_date"):
                text_val = self._format_date(val, short_year=True)
            elif col.get("numeric"):
                num_val = self._parse_amount(val)
                text_val = f"${int(round(num_val)):,}"
            else:
                text_val = str(val) if val is not None else ""

            if idx < len(row_cells):
                row_cells[idx].content.value = text_val

        row_ctrl.on_long_press = lambda e, data_item=item: self._handle_row_click(e, data_item)

    def update_data(self, new_data: list[dict]):
        existing_controls_map = {
            ctrl.data: ctrl
            for ctrl in self.list_view.controls
            if getattr(ctrl, "data", None) is not None
        }

        updated_controls = []

        for item in new_data:
            item_id = item.get("id")

            if item_id is not None and item_id in existing_controls_map:
                row_ctrl = existing_controls_map[item_id]
                self._update_row_cells(row_ctrl, item)
                row_ctrl.item_data = item
                row_ctrl.visible = True
                updated_controls.append(row_ctrl)
            else:
                updated_controls.append(self._build_single_row(item))

        self.data = new_data
        self.empty_control.visible = len(new_data) == 0
        updated_controls.append(self.empty_control)

        self.list_view.controls = updated_controls
        self._update_title_count()

        if self.page:
            self.list_view.update()
            self.title_text_control.update()