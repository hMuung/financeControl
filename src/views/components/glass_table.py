import flet as ft
import flet_datatable2 as fdt

from views.components.common.glass_card import GlassCard
from views.components.common.gradient_button import GradientButton
from views.utils.theme import BACKGROUND_GRADIENT, HEADER_TEXT_COLOR


class GlassDataTable(ft.Stack):

    def __init__(
        self,
        title: str = "Gastos",
        columns_config: list[dict] = None,
        data: list[dict] = None,
        categories_options: list = None,
        origins_options: list = None,
        empty_message: str = "No hay datos registrados.",
        min_amount_limit: float = 0.0,
        max_amount_limit: float = 10000.0,
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
        self.data = data or []
        self.empty_message = empty_message
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.selected_item = None  # Almacena la fila seleccionada

        # Modal de filtros
        self.modal_card = ft.Container(
            width=float("inf"),
            padding=ft.Padding.symmetric(vertical=5, horizontal=8),
            border_radius=24,
            gradient=BACKGROUND_GRADIENT,
            border=ft.Border.all(1.5, ft.Colors.WHITE),
            shadow=ft.BoxShadow(
                blur_radius=30,
                color=ft.Colors.BLACK_45,
                offset=ft.Offset(0, 10),
            ),
            on_click=lambda e: None,
            content=ft.Column(
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Filtros",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=HEADER_TEXT_COLOR,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=HEADER_TEXT_COLOR,
                                tooltip="Cerrar",
                                on_click=self._close_filter_modal,
                            ),
                        ],
                    ),
                    ft.Container(
                        padding=ft.Padding.symmetric(vertical=20),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.Icon(
                                    ft.Icons.CONSTRUCTION_ROUNDED,
                                    size=36,
                                    color=HEADER_TEXT_COLOR,
                                ),
                                ft.Text(
                                    "Próximamente",
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    color=HEADER_TEXT_COLOR,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

        self.full_screen_modal = ft.Container(
            visible=False,
            expand=True,
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
            blur=ft.Blur(sigma_x=25, sigma_y=25),
            alignment=ft.Alignment.CENTER,
            on_click=self._close_filter_modal,
            content=self.modal_card,
        )

        # Modal y detalles de accion
        self.detail_content_column = ft.Column(spacing=12, tight=True)

        self.detail_modal_card = ft.Container(
            width=380,
            padding=ft.Padding.all(20),
            border_radius=24,
            gradient=BACKGROUND_GRADIENT,
            border=ft.Border.all(1.5, ft.Colors.WHITE),
            shadow=ft.BoxShadow(
                blur_radius=30,
                color=ft.Colors.BLACK_45,
                offset=ft.Offset(0, 10),
            ),
            on_click=lambda e: None,
            content=ft.Column(
                tight=True,
                spacing=15,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Detalles del Registro",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=HEADER_TEXT_COLOR,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=HEADER_TEXT_COLOR,
                                tooltip="Cerrar",
                                on_click=self._close_detail_modal,
                            ),
                        ],
                    ),
                    self.detail_content_column,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,
                        controls=[
                            GradientButton(
                                text="Eliminar",
                                icon=ft.Icons.DELETE_OUTLINED,
                                gradient=ft.LinearGradient(
                                    colors=[ft.Colors.RED_700, ft.Colors.RED_500]
                                ),
                                padding=ft.Padding.symmetric(vertical=8, horizontal=14),
                                on_click=self._handle_delete,
                            ),
                            GradientButton(
                                text="Modificar",
                                icon=ft.Icons.EDIT,
                                gradient=ft.LinearGradient(
                                    colors=[ft.Colors.BLUE_700, ft.Colors.BLUE_500]
                                ),
                                padding=ft.Padding.symmetric(vertical=8, horizontal=14),
                                on_click=self._handle_edit,
                            ),
                        ],
                    ),
                ],
            ),
        )

        self.detail_modal = ft.Container(
            visible=False,
            expand=True,
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
            blur=ft.Blur(sigma_x=25, sigma_y=25),
            alignment=ft.Alignment.CENTER,
            on_click=self._close_detail_modal,
            content=self.detail_modal_card,
        )

        # Boton para abrir filtros
        self.btn_filter_trigger = ft.IconButton(
            icon=ft.Icons.FILTER_LIST,
            icon_color=HEADER_TEXT_COLOR,
            tooltip="Abrir Filtros",
            on_click=self._open_filter_modal,
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

        self.glass_card = GlassCard(
            content=ft.Column(
                spacing=6,
                expand=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                self.title_text,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=HEADER_TEXT_COLOR,
                            ),
                            self.btn_filter_trigger,
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
            if self.full_screen_modal not in self.page.overlay:
                self.page.overlay.append(self.full_screen_modal)
            if self.detail_modal not in self.page.overlay:
                self.page.overlay.append(self.detail_modal)

    def will_unmount(self):
        if self.page:
            if self.full_screen_modal in self.page.overlay:
                self.page.overlay.remove(self.full_screen_modal)
            if self.detail_modal in self.page.overlay:
                self.page.overlay.remove(self.detail_modal)

    def _get_page(self, e=None):
        if e and hasattr(e, "page") and e.page:
            return e.page
        return self.page

    # Manejo de modals
    def _open_filter_modal(self, e=None):
        page = self._get_page(e)
        if page:
            if self.full_screen_modal not in page.overlay:
                page.overlay.append(self.full_screen_modal)
            self.full_screen_modal.visible = True
            page.update()

    def _close_filter_modal(self, e=None):
        self.full_screen_modal.visible = False
        page = self._get_page(e)
        if page:
            page.update()

    def _open_detail_modal(self, item: dict):
        self.selected_item = item
        num_val = self._parse_amount(item.get("amount", 0))

        # Construccion dinamica del contenido del detalle
        self.detail_content_column.controls = [
            self._build_info_row("Fecha:", self._format_date(item.get("date", ""))),
            self._build_info_row("Categoría:", str(item.get("category", "-"))),
            self._build_info_row("Monto:", f"${num_val:.2f}"),
            self._build_info_row("Origen:", str(item.get("origin", "-"))),
            ft.Divider(height=1, color=ft.Colors.WHITE_24),
            ft.Column(
                spacing=4,
                controls=[
                    ft.Text("Descripción:", size=14, weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR),
                    ft.Text(
                        str(item.get("description") or "Sin descripción"),
                        size=14,
                        color=HEADER_TEXT_COLOR,
                        italic=not bool(item.get("description")),
                    ),
                ],
            ),
        ]

        page = self._get_page()
        if page:
            if self.detail_modal not in page.overlay:
                page.overlay.append(self.detail_modal)
            self.detail_modal.visible = True
            page.update()

    def _close_detail_modal(self, e=None):
        self.detail_modal.visible = False
        page = self._get_page(e)
        if page:
            page.update()

    def _build_info_row(self, label: str, value: str) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, size=16, weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR),
                ft.Text(value, size=16, color=HEADER_TEXT_COLOR),
            ],
        )

    # Acciones
    def _handle_delete(self, e):
        item = self.selected_item
        self._close_detail_modal(e)
        if self.on_delete and item:
            self.on_delete(item)

    def _handle_edit(self, e):
        item = self.selected_item
        self._close_detail_modal(e)
        if self.on_edit and item:
            self.on_edit(item)

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

    def _build_rows(self) -> list[fdt.DataRow2]:
        if not self.data:
            return []

        rows = []
        for item in self.data:
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
                        ft.Container(
                            content=ft.Text(
                                text_val,
                                size=11,
                                color=HEADER_TEXT_COLOR,
                                weight=ft.FontWeight.W_500 if col.get("numeric") else ft.FontWeight.NORMAL,
                                text_align=ft.TextAlign.LEFT,
                            ),
                            expand=True,
                            alignment=ft.Alignment.CENTER_LEFT,
                            on_click=lambda e, data_item=item: self._open_detail_modal(data_item),
                        )
                    )
                )

            rows.append(fdt.DataRow2(cells=cells))
        return rows
    
    def update_data(self, new_data: list[dict]):
        self.data = new_data
        self.table.rows = self._build_rows()
        if self.page:
            self.update()