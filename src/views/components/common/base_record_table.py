# src/views/components/common/bases_record_table.py
from datetime import date, datetime
import math
import flet as ft

from views.components.common.glass_table import GlassDataTable
from views.components.common.gradient_button import GradientButton
from views.components.common.styled_modal import StyledModal
from views.components.common.styled_dropdown import StyledDropdown
from views.components.common.styled_textfield import StyledTextField
from views.components.common.period_selector import PeriodSelector
from views.utils.toast import Toast
from views.utils.theme import (
    HEADER_TEXT_COLOR,
    CANCEL_GRADIENT,
    DELETE_GRADIENT,
    ACCEPT_GRADIENT,
    MODIFI_GRADIENT,
)


class BaseRecordGlassTable(GlassDataTable):
    """Clase base reutilizable para tablas de registros con detalle, edicion y filtros"""

    def __init__(
        self,
        title: str = "Registros",
        detail_title: str = "Detalles del registro",
        edit_title: str = "Edición de registro",
        filter_title: str = "Filtrar",
        columns_config: list[dict] = None,
        data: list[dict] = None,
        categories_options: list = None,
        origins_options: list = None,
        empty_message: str = "No hay registros que coincidan.",
        on_delete=None,
        on_edit=None,
    ):
        columns_config = columns_config or [
            {"label": "Fecha", "key": "date", "numeric": False, "expand": 2},
            {"label": "Categoría", "key": "category", "numeric": False, "expand": 3},
            {"label": "Monto", "key": "amount", "numeric": True, "expand": 2},
            {"label": "Origen", "key": "origin", "numeric": False, "expand": 3},
        ]

        self.detail_title = detail_title
        self.edit_title = edit_title
        self.filter_title = filter_title
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.categories_options = categories_options or []
        self.origins_options = origins_options or []

        btn_filter_trigger = ft.IconButton(
            icon=ft.Icons.FILTER_LIST,
            icon_color=HEADER_TEXT_COLOR,
            icon_size=25,
            tooltip="Abrir Filtros",
            on_click=self._open_filter_modal,
        )

        super().__init__(
            title=title,
            columns_config=columns_config,
            data=data or [],
            empty_message=empty_message,
            on_row_click=self._open_detail_modal,
            action_button=btn_filter_trigger,
        )

        self._init_detail_modal()
        self._init_edit_modal()
        self._init_filter_modal()
        self._update_amount_filter_range()

    # Inicializacion de Modales

    def _init_detail_modal(self):
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
            title=self.detail_title,
            padding=ft.Padding.symmetric(vertical=5, horizontal=15),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[self.detail_modal_content, detail_modal_action_buttons],
            ),
        )

    def _init_edit_modal(self):
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
            hint_text="0",
            format_numeric=True,
            prefix_icon=ft.Icons.ATTACH_MONEY,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.edit_tf_description = StyledTextField(
            label="Descripción",
            hint_text="Nota adicional...",
            prefix_icon=ft.Icons.DESCRIPTION_OUTLINED,
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
            title=self.edit_title,
            padding=ft.Padding.symmetric(vertical=5, horizontal=15),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    ft.Column(
                        spacing=12,
                        tight=True,
                        controls=[
                            self.edit_dd_category,
                            self.edit_dd_origin,
                            self.edit_tf_amount,
                            self.edit_tf_description,
                        ],
                    ),
                    edit_modal_action_buttons,
                ],
            ),
        )

    def _init_filter_modal(self):
        # Selector de Período Integrado
        self.period_selector = PeriodSelector(allow_all=True)

        cat_opts = [("all", "Todas")] + list(self.categories_options)
        orig_opts = [("all", "Todos")] + list(self.origins_options)

        self.filter_dd_category = StyledDropdown(
            label="Categoría",
            options_list=cat_opts,
            value="all",
            leading_icon=ft.Icons.CATEGORY_OUTLINED,
        )
        self.filter_dd_origin = StyledDropdown(
            label="Origen",
            options_list=orig_opts,
            value="all",
            leading_icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
        )

        self.filter_lbl_min = ft.Text("$0", size=15, weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR)
        self.filter_lbl_max = ft.Text("$100", size=15, weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR)

        self.filter_range_slider = ft.RangeSlider(
            min=0,
            max=100,
            start_value=0,
            end_value=100,
            active_color=HEADER_TEXT_COLOR,
            inactive_color=ft.Colors.WHITE_24,
            on_change=self._on_range_slider_change,
        )

        filter_action_buttons = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
            controls=[
                GradientButton(
                    text="Limpiar",
                    icon=ft.Icons.RESTART_ALT_ROUNDED,
                    gradient=CANCEL_GRADIENT,
                    padding=ft.Padding.symmetric(vertical=8, horizontal=14),
                    on_click=self._clear_filters,
                ),
                GradientButton(
                    text="Aplicar",
                    icon=ft.Icons.FILTER_ALT_OUTLINED,
                    gradient=ACCEPT_GRADIENT,
                    padding=ft.Padding.symmetric(vertical=8, horizontal=14),
                    on_click=self._apply_filters,
                ),
            ],
        )

        self.filter_modal = StyledModal(
            title=self.filter_title,
            padding=ft.Padding.symmetric(vertical=5, horizontal=15),
            content=ft.Column(
                tight=True,
                spacing=12,
                controls=[
                    ft.Text("Fecha y Período", weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR, size=14),
                    self.period_selector,
                    ft.Text("Clasificación", weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR, size=14),
                    self.filter_dd_category,
                    self.filter_dd_origin,
                    ft.Text("Rango de Cantidad", weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR, size=14),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[self.filter_lbl_min, self.filter_lbl_max],
                    ),
                    self.filter_range_slider,
                    ft.Divider(height=1, color=ft.Colors.WHITE_24),
                    filter_action_buttons,
                ],
            ),
        )

    # Utilidades y Procesamiento de Datos
    def _parse_item_date(self, date_val) -> date | None:
        if not date_val:
            return None
        if isinstance(date_val, date):
            return date_val
        if isinstance(date_val, datetime):
            return date_val.date()
        date_str = str(date_val)
        try:
            if "-" in date_str:
                parts = date_str.split("T")[0].split(" ")[0].split("-")
                if len(parts) == 3:
                    return date(int(parts[0]), int(parts[1]), int(parts[2]))
            elif "/" in date_str:
                parts = date_str.split(" ")[0].split("/")
                if len(parts) == 3:
                    return date(int(parts[2]), int(parts[1]), int(parts[0]))
        except Exception:
            pass
        return None

    def _get_max_amount(self) -> float:
        if not self.data:
            return 100.0
        amounts = [self._parse_amount(item.get("amount", 0)) for item in self.data]
        max_val = max(amounts) if amounts else 0.0
        return float(math.ceil(max_val)) if max_val > 0 else 100.0

    def _update_amount_filter_range(self):
        max_val = self._get_max_amount()
        self.filter_range_slider.min = 0
        self.filter_range_slider.max = max_val
        self.filter_range_slider.start_value = 0
        self.filter_range_slider.end_value = max_val

        if hasattr(self, "filter_lbl_min") and hasattr(self, "filter_lbl_max"):
            self.filter_lbl_min.value = "$0"
            self.filter_lbl_max.value = f"${int(max_val):,}"

    def _on_range_slider_change(self, e):
        min_val = int(round(e.control.start_value))
        max_val = int(round(e.control.end_value))
        self.filter_lbl_min.value = f"${min_val:,}"
        self.filter_lbl_max.value = f"${max_val:,}"
        self.filter_lbl_min.update()
        self.filter_lbl_max.update()

    # Logica de Filtros
    def _apply_filters(self, e=None):
        start_date, end_date = self.period_selector.get_date_range()

        sel_cat_id = getattr(self.filter_dd_category, "value", "all")
        sel_orig_id = getattr(self.filter_dd_origin, "value", "all")

        min_amt = self.filter_range_slider.start_value
        max_amt = self.filter_range_slider.end_value

        cat_map = {str(c[0]): c[1] for c in self.categories_options if len(c) > 1}
        orig_map = {str(o[0]): o[1] for o in self.origins_options if len(o) > 1}

        visible_count = 0

        for ctrl in self.list_view.controls:
            if ctrl == self.empty_control:
                continue

            item = getattr(ctrl, "item_data", None)
            if not item:
                continue

            is_visible = True

            # Evaluación de Rango de Fecha / Período
            if start_date != "all":
                item_dt = self._parse_item_date(item.get("date"))
                if not item_dt:
                    is_visible = False
                elif start_date and end_date:
                    if not (start_date <= item_dt <= end_date):
                        is_visible = False
                else:
                    is_visible = False

            # Evaluación de Categoría
            if is_visible and sel_cat_id != "all":
                target_cat_name = cat_map.get(str(sel_cat_id))
                item_cat = str(item.get("category", ""))
                item_cat_id = str(item.get("category_id", ""))
                if item_cat != target_cat_name and item_cat_id != str(sel_cat_id):
                    is_visible = False

            # Evaluación de Origen
            if is_visible and sel_orig_id != "all":
                target_orig_name = orig_map.get(str(sel_orig_id))
                item_orig = str(item.get("origin", ""))
                item_orig_id = str(item.get("origin_id", ""))
                if item_orig != target_orig_name and item_orig_id != str(sel_orig_id):
                    is_visible = False

            # Evaluación de Monto
            if is_visible:
                amt = self._parse_amount(item.get("amount", 0))
                if not (min_amt <= amt <= max_amt):
                    is_visible = False

            ctrl.visible = is_visible
            if is_visible:
                visible_count += 1

        self.empty_control.visible = (visible_count == 0)

        self.filter_modal.close(e)
        self.list_view.update()
        self._update_title_count(visible_count)
        self.title_text_control.update()

    def _clear_filters(self, e=None):
        self.period_selector.mode = "ALL"
        self.period_selector._update_trigger_label()

        self.filter_dd_category.value = "all"
        self.filter_dd_category.color = None
        self.filter_dd_category.fill_color = None

        self.filter_dd_origin.value = "all"
        self.filter_dd_origin.color = None
        self.filter_dd_origin.fill_color = None

        max_val = self._get_max_amount()
        self.filter_range_slider.start_value = 0
        self.filter_range_slider.end_value = max_val
        self.filter_lbl_min.value = "$0"
        self.filter_lbl_max.value = f"${int(max_val):,}"

        visible_count = 0
        for ctrl in self.list_view.controls:
            if ctrl == self.empty_control:
                continue
            ctrl.visible = True
            visible_count += 1

        self.empty_control.visible = (visible_count == 0)

        self.filter_modal.close(e)
        self.filter_modal.update()
        self.list_view.update()
        self._update_title_count(visible_count)
        self.title_text_control.update()

    # Eventos de Ciclo de Vida y Modales
    def did_mount(self):
        if self.page:
            if self.detail_modal not in self.page.overlay:
                self.page.overlay.append(self.detail_modal)
            if self.filter_modal not in self.page.overlay:
                self.page.overlay.append(self.filter_modal)
            if self.edit_modal not in self.page.overlay:
                self.page.overlay.append(self.edit_modal)

    def will_unmount(self):
        if self.page:
            if self.detail_modal in self.page.overlay:
                self.page.overlay.remove(self.detail_modal)
            if self.filter_modal in self.page.overlay:
                self.page.overlay.remove(self.filter_modal)
            if self.edit_modal in self.page.overlay:
                self.page.overlay.append(self.edit_modal)

    def _open_filter_modal(self, e=None):
        self.filter_modal.open(e)

    def _open_detail_modal(self, e, item: dict):
        num_val = self._parse_amount(item.get("amount", 0))

        self.detail_modal_content.controls = [
            self._build_info_row("Fecha:", self._format_date(item.get("date", ""), short_year=False)),
            self._build_info_row("Categoría:", str(item.get("category", "-"))),
            self._build_info_row("Monto:", f"${int(round(num_val)):,}"),
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
        self.detail_modal.open(e)

    def _build_info_row(self, label: str, value: str) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, size=16, weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR),
                ft.Text(value, size=16, color=HEADER_TEXT_COLOR),
            ],
        )

    # Manejadores CRUD
    def _handle_edit(self, e):
        item = self.selected_item
        if not item:
            return

        cat_match = next((c for c in self.categories_options if len(c) > 1 and c[1] == item.get("category")), None)
        orig_match = next((o for o in self.origins_options if len(o) > 1 and o[1] == item.get("origin")), None)

        if cat_match:
            self.edit_dd_category.value = str(cat_match[0])
            if len(cat_match) >= 4:
                self.edit_dd_category.color = cat_match[2]
                self.edit_dd_category.fill_color = cat_match[3]
        else:
            self.edit_dd_category.value = None

        if orig_match:
            self.edit_dd_origin.value = str(orig_match[0])
            if len(orig_match) >= 4:
                self.edit_dd_origin.color = orig_match[2]
                self.edit_dd_origin.fill_color = orig_match[3]
        else:
            self.edit_dd_origin.value = None

        num_val = self._parse_amount(item.get("amount", 0))
        self.edit_tf_amount.value = f"{int(round(num_val)):,}"
        self.edit_tf_description.value = str(item.get("description", ""))

        self.detail_modal.close(e)
        self.edit_modal.open(e)

    def _handle_delete(self, e):
        item = self.selected_item
        self.detail_modal.close(e)

        if self.on_delete and item:
            success, message = self.on_delete(item)
            page = self._get_page(e)

            if success:
                Toast.success(page, message)
                item_id = item.get("id")
                self.data = [i for i in self.data if i.get("id") != item_id]
                self.list_view.controls = [c for c in self.list_view.controls if getattr(c, "data", None) != item_id]

                if not self.list_view.controls:
                    self.list_view.controls = [self._build_empty_control()]

                self._update_amount_filter_range()
                self.update()
            else:
                Toast.error(page, message)

    def _handle_save(self, e):
        page = self._get_page(e)

        if not self.selected_item:
            Toast.error(page, "Error al guardar.")
            self.edit_modal.close(e)
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
                self.edit_modal.close(e)

                cat_name = next(
                    (c[1] for c in self.categories_options if str(c[0]) == str(payload["category_id"])),
                    self.selected_item.get("category"),
                )
                orig_name = next(
                    (o[1] for o in self.origins_options if str(o[0]) == str(payload["origin_id"])),
                    self.selected_item.get("origin"),
                )

                self.selected_item.update({
                    "category": cat_name,
                    "origin": orig_name,
                    "amount": self._parse_amount(payload["amount_str"]),
                    "description": payload["description"],
                })

                item_id = self.selected_item.get("id")
                for idx, ctrl in enumerate(self.list_view.controls):
                    if getattr(ctrl, "data", None) == item_id:
                        self.list_view.controls[idx] = self._build_single_row(self.selected_item)
                        break

                self.list_view.update()
                self._update_amount_filter_range()
                self._open_detail_modal(e, self.selected_item)
            else:
                Toast.error(page, message)
        else:
            self._open_detail_modal(e, self.selected_item)
            self.edit_modal.close(e)

    def _handle_cancel(self, e):
        self._open_detail_modal(e, self.selected_item)
        self.edit_modal.close(e)

    def update_data(self, new_data: list[dict]):
        super().update_data(new_data)
        self._update_amount_filter_range()
        if self.page:
            self.update()