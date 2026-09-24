# src/viewa/components/glass_table.py
import flet as ft
import flet_datatable2 as fdt

from views.utils.toast import Toast
from views.components.common.glass_card import GlassCard
from views.components.common.gradient_button import GradientButton
from views.components.common.styled_modal import StyledModal
from views.components.common.styled_dropdown import StyledDropdown
from views.components.common.styled_textfield import StyledTextField
from views.utils.theme import (
    HEADER_TEXT_COLOR, 
    CANCEL_GRADIENT, 
    DELETE_GRADIENT, 
    ACCEPT_GRADIENT, 
    MODIFI_GRADIENT
)

class GlassDataTable(ft.Stack):

    def __init__(
        self,
        title: str = "Gastos",
        columns_config: list[dict] = None,
        data: list[dict] = [],
        categories_options: list = None,
        origins_options: list = None,
        empty_message: str = "No hay datos registrados.",
        min_amount_limit: float = 0.0,
        max_amount_limit: float = float("inf"),
        on_delete=None,  # Callback para eliminar
        on_edit=None,    # Callback para modificar
    ):
        self.title_text = title
        self.columns_config = columns_config or [
            {"label": "Fecha", "key": "date", "numeric": False},
            {"label": "Categoría", "key": "category", "numeric": False},
            {"label": "Monto", "key": "amount", "numeric": True},
            {"label": "Origen", "key": "origin", "numeric": False},
        ]

        self.data = data
        self.empty_message = empty_message
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.selected_item = None
        self.categories_options = categories_options
        self.origins_options = origins_options

        # Modal de filtros
        self.filter_modal = StyledModal(
            title="Filtrar",
            content=None
        )

        btn_filter_trigger = ft.IconButton(
            icon=ft.Icons.FILTER_LIST,
            icon_color=HEADER_TEXT_COLOR,
            tooltip="Abrir Filtros",
            on_click=self._open_filter_modal,
        )

        # Modal de detalles de accion
        self.detail_modal_content = ft.Column(spacing=12, tight=True)

        detail_modal_action_buttons = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
            controls=[
                GradientButton(
                    text="Eliminar",
                    icon=ft.Icons.DELETE_OUTLINED,
                    gradient=DELETE_GRADIENT,
                    padding=ft.Padding.symmetric(vertical=8, horizontal=14),
                    on_click=self._handle_delete,
                ),
                GradientButton(
                    text="Modificar",
                    icon=ft.Icons.EDIT,
                    gradient=MODIFI_GRADIENT,
                    padding=ft.Padding.symmetric(vertical=8, horizontal=14),
                    on_click=self._handle_edit,
                ),
            ],
        )

        self.detail_modal = StyledModal(
            title="Detalles del registro",
            padding=ft.Padding.symmetric(vertical=5,horizontal=15),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    self.detail_modal_content,
                    detail_modal_action_buttons
                ]
            )
        )

        # Modal de edicion
        self.edit_dd_category = StyledDropdown(
            label="Categoría",
            options_list=self.categories_options,
            leading_icon=ft.Icons.CATEGORY_OUTLINED,
        )

        self.edit_dd_origin = StyledDropdown(
            label="Origen",
            options_list=self.origins_options,
            leading_icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
        )

        self.edit_tf_amount = StyledTextField(
            label="Monto",
            hint_text="0.00",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.edit_tf_description = StyledTextField(
            label="Descripcion",
            hint_text="Nota adicional...",
            prefix_icon=ft.Icons.DESCRIPTION_OUTLINED,
        )

        self.edit_modal_content = ft.Column(
            spacing=12, 
            tight=True,
            controls=[
                self.edit_dd_category,
                self.edit_dd_origin,
                self.edit_tf_amount,
                self.edit_tf_description,
            ]
        )

        edit_modal_action_buttons = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
            controls=[
                GradientButton(
                    text="Cancelar",
                    icon=ft.Icons.CANCEL_ROUNDED,
                    gradient=CANCEL_GRADIENT,
                    padding=ft.Padding.symmetric(vertical=8, horizontal=14),
                    on_click=self._handle_cancel,
                ),
                GradientButton(
                    text="Guardar",
                    icon=ft.Icons.SAVE_ROUNDED,
                    gradient=ACCEPT_GRADIENT,
                    padding=ft.Padding.symmetric(vertical=8, horizontal=14),
                    on_click=self._handle_save,
                ),
            ],
        )


        self.edit_modal = StyledModal(
            title="Ediccion de registro",
            padding=ft.Padding.symmetric(vertical=5,horizontal=15),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    self.edit_modal_content,
                    edit_modal_action_buttons
                ]
            )
        )

        # Estructura compacta de la tabla DataTable2
        self.table = fdt.DataTable2(
            expand=True,
            fixed_top_rows=1,
            show_checkbox_column=False,
            empty=ft.Text(
                self.empty_message,
                color=ft.Colors.BLACK_54,
                italic=True,
                size=11,
            ),
            columns=self._build_columns(),
            rows=self._build_rows(),
            heading_row_color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
            heading_row_height=32,
            data_row_height=30,
            divider_thickness=0.5,
            column_spacing=10,
            horizontal_margin=8,
        )

        self.title_text_control = ft.Text(
            value=f"{self.title_text} ({len(self.data)})",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=HEADER_TEXT_COLOR,
        )

        self.glass_card = GlassCard(
            content=ft.Column(
                spacing=6,
                expand=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.title_text_control,
                            btn_filter_trigger,
                        ],
                    ),
                    ft.Container(
                        content=self.table,
                        border_radius=10,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        expand=True,
                    ),
                ],
            )
        )

        main_layout = ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    content=self.glass_card,
                    expand=1,
                ),
                ft.Container(
                    expand=1,
                ),
            ],
        )

        super().__init__(
            expand=True,
            controls=[
                main_layout,
            ],
        )

    # Ciclo de vida
    def did_mount(self):
        if self.page:
            if self.detail_modal not in self.page.overlay:
                self.page.overlay.append(self.detail_modal)

    def will_unmount(self):
        if self.page:
            if self.detail_modal in self.page.overlay:
                self.page.overlay.remove(self.detail_modal)

    def _get_page(self, e=None):
        if e and hasattr(e, "page") and e.page:
            return e.page
        return self.page

    # Manejo de modals
    def _open_filter_modal(self, e=None):
        self.filter_modal.open(e)

    def _close_filter_modal(self, e=None):
        self.filter_modal.close(e)

    def _open_detail_modal(self, e, item: dict):
        self.selected_item = item
        num_val = self._parse_amount(item.get("amount", 0))

        # Construccion dinamica del contenido del detalle
        self.detail_modal_content.controls = [
            self._build_info_row("Fecha:", self._format_date(item.get("date", ""))),
            self._build_info_row("Categoría:", str(item.get("category", "-"))),
            self._build_info_row("Monto:", f"${num_val:.2f}"),
            self._build_info_row("Origen:", str(item.get("origin", "-"))),
            ft.Divider(height=1, color=ft.Colors.WHITE_24),
            ft.Column(
                spacing=4,
                controls=[
                    ft.Text("Descripcion:", size=14, weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR),
                    ft.Text(
                        str(item.get("description") or "Sin descripción"),
                        size=14,
                        color=HEADER_TEXT_COLOR,
                        italic=not bool(item.get("description")),
                    ),
                ],
            ),
        ]

        self.detail_modal.open(e)

    def _close_detail_modal(self, e=None):
        self.detail_modal.close(e)

    def _open_edit_modal(self, e=None):
        self.edit_modal.open(e)
    
    def _close_edit_modal(self, e=None):
        self.edit_modal.close(e)

    def _build_info_row(self, label: str, value: str) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, size=16, weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR),
                ft.Text(value, size=16, color=HEADER_TEXT_COLOR),
            ],
        )

    def _handle_edit(self, e):
        item = self.selected_item

        if not item:
            return

        # Acceso por índice de tupla: c[0] es ID, c[1] es Nombre
        cat_match = next(
            (c for c in (self.categories_options or []) if len(c) > 1 and c[1] == item.get("category")), 
            None
        )
        orig_match = next(
            (o for o in (self.origins_options or []) if len(o) > 1 and o[1] == item.get("origin")), 
            None
        )

        self.edit_dd_category.value = str(cat_match[0]) if cat_match else None
        self.edit_dd_origin.value = str(orig_match[0]) if orig_match else None
        self.edit_tf_amount.value = str(item.get("amount", ""))
        self.edit_tf_description.value = str(item.get("description", ""))

        self._close_detail_modal(e)
        self._open_edit_modal(e)

    def _handle_delete(self, e):
        item = self.selected_item
        self._close_detail_modal(e)

        if self.on_delete and item:
            success, message = self.on_delete(item)
            page = self._get_page(e)

            if success:
                Toast.success(page, message)
                item_id = item.get("id")

                # Quitar de la lista de datos en memoria
                self.data = [i for i in self.data if i.get("id") != item_id]

                # Eliminar solo la fila de la lista de controles de la tabla
                self.table.rows = [r for r in self.table.rows if getattr(r, "data", None) != item_id]

                self._update_title_count()
                self.update()
            else:
                Toast.error(page, message)

    def _handle_save(self, e):
        page = self._get_page(e)

        if not self.selected_item:
            Toast.error(page, "Error al guardar.")
            self._close_edit_modal(e)
            return

        payload = {
            "id": self.selected_item.get("id"),
            "category_id": int(self.edit_dd_category.value) if self.edit_dd_category.value else None,
            "origin_id": int(self.edit_dd_origin.value) if self.edit_dd_origin.value else None,
            "amount_str": self.edit_tf_amount.value,
            "description": self.edit_tf_description.value,
        }

        if self.on_edit:
            success, message = self.on_edit(payload)
            if success:
                Toast.success(page, message)
                self._close_edit_modal(e)

                # Resolver nombres visuales
                cat_name = next(
                    (c[1] for c in (self.categories_options or []) if str(c[0]) == str(payload["category_id"])), 
                    self.selected_item.get("category")
                )
                orig_name = next(
                    (o[1] for o in (self.origins_options or []) if str(o[0]) == str(payload["origin_id"])), 
                    self.selected_item.get("origin")
                )

                # Actualizar diccionario en memoria
                self.selected_item.update({
                    "category": cat_name,
                    "origin": orig_name,
                    "amount": self._parse_amount(payload["amount_str"]),
                    "description": payload["description"],
                })

                item_id = self.selected_item.get("id")

                # Reemplazar unicamente el elemento modificado en la lista de filas
                for idx, row in enumerate(self.table.rows):
                    if getattr(row, "data", None) == item_id:
                        self.table.rows[idx] = self._build_single_row(self.selected_item)
                        break

                # Renderizar unicamente la tabla
                self.table.update()

                self._open_detail_modal(e, self.selected_item)
            else:
                Toast.error(page, message)
        else:
            self._close_edit_modal(e)
            self._open_detail_modal(e, self.selected_item)

    def _handle_cancel(self,e):
        self._close_edit_modal(e)
        self._open_detail_modal(e,self.selected_item)

    # Construcccion de la tabla
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
    def _format_date(val) -> str:
        if not val:
            return ""
        val_str = str(val).strip()
        try:
            clean_val = val_str.split("T")[0].split(" ")[0]
            parts = clean_val.split("-")
            if len(parts) == 3 and len(parts[0]) == 4:
                return f"{parts[2]}/{parts[1]}/{parts[0]}"
        except Exception:
            pass
        return val_str

    def _update_title_count(self):
        self.title_text_control.value = f"{self.title_text} ({len(self.data)})"

    def _build_columns(self) -> list[fdt.DataColumn2]:
        cols = []
        for col in self.columns_config:
            cols.append(
                fdt.DataColumn2(
                    label=ft.Container(
                        content=ft.Text(
                            col["label"],
                            weight=ft.FontWeight.BOLD,
                            size=11,
                            color=HEADER_TEXT_COLOR,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.Alignment.CENTER,
                        expand=True,
                    ),
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                    numeric=False,
                )
            )
        return cols

    # Construye una sola fila y le asigna su ID en la propiedad .data
    def _build_single_row(self, item: dict) -> fdt.DataRow2:
        cells = []
        for col in self.columns_config:
            key = col["key"]
            val = item.get(key, "")

            if key == "date" or col.get("is_date"):
                text_val = self._format_date(val)
            elif col.get("numeric"):
                num_val = self._parse_amount(val)
                text_val = f"${num_val:.2f}"
            else:
                text_val = str(val) if val is not None else ""

            cells.append(
                ft.DataCell(
                    content=ft.Text(
                        text_val,
                        size=11,
                        color=HEADER_TEXT_COLOR,
                        weight=ft.FontWeight.W_500 if col.get("numeric") else ft.FontWeight.NORMAL,
                        text_align=ft.TextAlign.LEFT,
                    )
                )
            )

        row = fdt.DataRow2(
            cells=cells,
            on_double_tap=lambda e, data_item=item: self._open_detail_modal(e, data_item),
            on_long_press=lambda e, data_item=item: self._open_detail_modal(e, data_item)
        )

        # ID dentro de la propia fila
        row.data = item.get("id")
        return row

    def _build_rows(self) -> list[fdt.DataRow2]:
        if not self.data:
            return []
        return [self._build_single_row(item) for item in self.data]
    
    def update_data(self, new_data: list[dict]):
        self.data = new_data
        self.table.rows = self._build_rows()
        self._update_title_count()
        if self.page:
            self.update()