# src/views/components/common/glass_table.py
import flet as ft

from views.components.common.glass_card import GlassCard
from views.utils.theme import HEADER_TEXT_COLOR


class GlassDataTable(ft.Stack):

    def __init__(
        self,
        title: str = "Registros",
        columns_config: list[dict] = None,
        data: list[dict] = None,
        empty_message: str = "No hay datos registrados.",
        on_row_click=None,
        action_button: ft.Control = None,
        minimized_height: float = 50,   # Altura solo barra
        collapsed_height: float = 380,  # Altura estandar abierta
        expanded_height: float = 650,   # Altura maxima abierta
    ):
        self.title_text = title
        self.columns_config = columns_config or []
        self.data = data or []
        self.empty_message = empty_message
        self.on_row_click = on_row_click
        self.selected_item = None
        self.action_button = action_button

        # Alturas configurables
        self.minimized_height = minimized_height
        self.collapsed_height = collapsed_height
        self.expanded_height = expanded_height

        # Estado inicial
        self.is_minimized = True
        self.is_expanded = False

        self.header_row = self._build_header_row()

        self.empty_control = self._build_empty_control()

        self.list_view = ft.ListView(
            expand=True,
            spacing=2,
            padding=ft.Padding.symmetric(vertical=4, horizontal=4),
            build_controls_on_demand=True,
            first_item_prototype=True,
            controls=self._build_rows(),
        )

        self.title_text_control = ft.Text(
            value=f"{self.title_text} ({len(self.data)})",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=HEADER_TEXT_COLOR,
        )

        # Boton para alternar solo barra (Minimizar / Desplegar)
        self.btn_minimize = ft.IconButton(
            icon=ft.Icons.KEYBOARD_ARROW_DOWN,
            icon_color=HEADER_TEXT_COLOR,
            icon_size=25,
            tooltip="Desplegar",
            on_click=self._toggle_minimize,
        )

        # Boton para alternar tamaño de apertura (Normal / Pantalla Maxima)
        self.btn_size_toggle = ft.IconButton(
            icon=ft.Icons.FULLSCREEN,
            icon_color=HEADER_TEXT_COLOR,
            icon_size=23,
            tooltip="Expandir",
            on_click=self._toggle_size,
        )

        # Agrupacion de controles en la cabecera
        action_controls = []
        if self.action_button:
            action_controls.append(self.action_button)
        
        action_controls.append(self.btn_size_toggle)
        action_controls.append(self.btn_minimize)

        header_actions_row = ft.Row(
            controls=action_controls,
            spacing=1,
            alignment=ft.MainAxisAlignment.END,
        )

        header_controls = [
            ft.Container(width=5),
            self.title_text_control, 
            ft.Container(expand=True),
            header_actions_row
        ]

        self.table_container = ft.Container(
            content=self.list_view,
            border_radius=10,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            expand=True,
        )

        self.glass_card = GlassCard(
            padding=0,
            content=ft.Column(
                spacing=6,
                expand=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=header_controls,
                    ),
                    self.header_row,
                    self.table_container,
                ],
            )
        )

        super().__init__(
            height=self.minimized_height,
            controls=[self.glass_card]
        )

        self._apply_state()

    def _apply_state(self):
        if self.is_minimized:
            # Estado barra cerrada
            self.height = self.minimized_height
            self.header_row.visible = False
            self.table_container.visible = False
            
            # Iconos de cabecera
            self.btn_minimize.icon = ft.Icons.KEYBOARD_ARROW_DOWN
            self.btn_minimize.tooltip = "Desplegar"
            self.btn_size_toggle.visible = False
            if self.action_button:
                self.action_button.visible = False
        else:
            # Estado tabla abierta
            self.header_row.visible = True
            self.table_container.visible = True
            self.btn_minimize.icon = ft.Icons.KEYBOARD_ARROW_UP
            self.btn_minimize.tooltip = "Colapsar a barra"
            self.btn_size_toggle.visible = True
            if self.action_button:
                self.action_button.visible = True

            # Altura maxima o normal
            if self.is_expanded:
                self.height = self.expanded_height
                self.btn_size_toggle.icon = ft.Icons.FULLSCREEN_EXIT
                self.btn_size_toggle.tooltip = "Reducir tamaño"
            else:
                self.height = self.collapsed_height
                self.btn_size_toggle.icon = ft.Icons.FULLSCREEN
                self.btn_size_toggle.tooltip = "Expandir al máximo"

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

    def _update_title_count(self,count: int = None):
        if count:
            self.title_text_control.value = f"{self.title_text} ({count})"
            return
        self.title_text_control.value = f"{self.title_text} ({len(self.data)})"

    def _build_header_row(self) -> ft.Container:
        header_cells = [
            ft.Container(
                content=ft.Text(
                    col["label"],
                    weight=ft.FontWeight.BOLD,
                    size=11,
                    color=HEADER_TEXT_COLOR,
                    text_align=ft.TextAlign.CENTER,
                ),
                alignment=ft.Alignment.CENTER,
                expand=col.get("expand", 1),
            )
            for col in self.columns_config
        ]
        return ft.Container(
            content=ft.Row(controls=header_cells, spacing=10),
            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            padding=ft.Padding.symmetric(vertical=8, horizontal=8),
            border_radius=6,
        )

    def _build_empty_control(self) -> ft.Container:
        return ft.Container(
            content=ft.Text(
                self.empty_message,
                color=ft.Colors.BLACK_54,
                italic=True,
                size=11,
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
                        size=11,
                        color=HEADER_TEXT_COLOR,
                        weight=ft.FontWeight.W_500 if col.get("numeric") else ft.FontWeight.NORMAL,
                        text_align=ft.TextAlign.LEFT,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    alignment=ft.Alignment.CENTER_LEFT,
                    expand=col.get("expand", 1),
                )
            )

        row_container = ft.Container(
            content=ft.Row(controls=cells, spacing=10),
            padding=ft.Padding.symmetric(vertical=6, horizontal=8),
            border_radius=4,
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