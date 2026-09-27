# src/views/components/incomes_record_table.py
import flet as ft
import calendar
import math

from views.components.common.glass_table import GlassDataTable 
from views.components.common.gradient_button import GradientButton
from views.components.common.styled_modal import StyledModal
from views.components.common.styled_dropdown import StyledDropdown
from views.components.common.styled_textfield import StyledTextField
from views.utils.toast import Toast
from views.utils.theme import (
    HEADER_TEXT_COLOR, 
    CANCEL_GRADIENT, 
    DELETE_GRADIENT, 
    ACCEPT_GRADIENT, 
    MODIFI_GRADIENT
)


class IngresosGlassTable(GlassDataTable):

    def __init__(
        self,
        title: str = "Ingresos",
        columns_config: list[dict] = None,
        data: list[dict] = None,
        categories_options: list = None,
        origins_options: list = None,
        empty_message: str = "No hay ingresos registrados.",
        on_delete=None,
        on_edit=None,
    ):

        # Anchos relativos idénticos a los de gastos
        columns_config = columns_config or [
            {"label": "Fecha", "key": "date", "numeric": False, "expand": 2},
            {"label": "Categoría", "key": "category", "numeric": False, "expand": 3},
            {"label": "Monto", "key": "amount", "numeric": True, "expand": 2},
            {"label": "Origen", "key": "origin", "numeric": False, "expand": 3},
        ]

        self.on_delete = on_delete
        self.on_edit = on_edit
        self.categories_options = categories_options or []
        self.origins_options = origins_options or []

        # Botón de filtros
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

        # Configuración de modales
        self._init_detail_modal()
        self._init_edit_modal()
        self._init_filter_modal()
        self._update_amount_filter_range()

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
            title="Detalles del ingreso",
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
            title="Edición de ingreso",
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
        self.filter_dd_year = StyledDropdown(
            label="Año",
            options_list=[("all", "Todos")],
            value="all",
            leading_icon=ft.Icons.CALENDAR_TODAY_OUTLINED,
            on_change=self._update_days_dropdown,
        )

        months_list = [
            ("all", "Todos"),
            ("01", "Enero"), ("02", "Febrero"), ("03", "Marzo"),
            ("04", "Abril"), ("05", "Mayo"), ("06", "Junio"),
            ("07", "Julio"), ("08", "Agosto"), ("09", "Septiembre"),
            ("10", "Octubre"), ("11", "Noviembre"), ("12", "Diciembre"),
        ]

        self.filter_dd_month = StyledDropdown(
            label="Mes",
            options_list=months_list,
            value="all",
            leading_icon=ft.Icons.CALENDAR_MONTH_OUTLINED,
            on_change=self._update_days_dropdown,
        )

        days_list = [("all", "Todos")] + [(f"{i:02d}", str(i)) for i in range(1, 32)]
        self.filter_dd_day = StyledDropdown(
            label="Día",
            options_list=days_list,
            value="all",
            leading_icon=ft.Icons.TODAY_OUTLINED,
        )

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
                    on_click=self._clear_filters
                ),
                GradientButton(
                    text="Aplicar",
                    icon=ft.Icons.FILTER_ALT_OUTLINED,
                    gradient=ACCEPT_GRADIENT,
                    padding=ft.Padding.symmetric(vertical=8, horizontal=14),
                    on_click=self._apply_filters
                ),
            ],
        )

        self.filter_modal = StyledModal(
            title="Filtrar Ingresos",
            padding=ft.Padding.symmetric(vertical=5, horizontal=15),
            content=ft.Column(
                tight=True,
                spacing=12,
                controls=[
                    ft.Text("Fecha", weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR, size=14),
                    self.filter_dd_month,
                    ft.Row(
                        controls=[
                            self.filter_dd_day,
                            self.filter_dd_year,
                        ]
                    ),
                    ft.Text("Clasificación", weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR, size=14),
                    self.filter_dd_category,
                    self.filter_dd_origin,
                    ft.Text("Rango de Cantidad", weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR, size=14),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.filter_lbl_min, 
                            self.filter_lbl_max
                        ]
                    ),
                    self.filter_range_slider,
                    ft.Divider(height=1, color=ft.Colors.WHITE_24),
                    filter_action_buttons,
                ],
            ),
        )

    def _parse_item_date(self, date_str: str):
        if not date_str:
            return None, None, None
        try:
            if "-" in date_str:
                parts = date_str.split("T")[0].split(" ")[0].split("-")
                if len(parts) == 3:
                    return parts[0], parts[1].zfill(2), parts[2].zfill(2)
            elif "/" in date_str:
                parts = date_str.split(" ")[0].split("/")
                if len(parts) == 3:
                    return parts[2], parts[1].zfill(2), parts[0].zfill(2)
        except Exception:
            pass
        return None, None, None

    def _update_years_dropdown(self):
        years = set()
        for item in self.data:
            y, _, _ = self._parse_item_date(str(item.get("date", "")))
            if y:
                years.add(y)

        sorted_years = sorted(list(years), reverse=True)
        years_list = [("all", "Todos")] + [(y, y) for y in sorted_years]

        if hasattr(self.filter_dd_year, "options_list"):
            self.filter_dd_year.options_list = years_list

        if hasattr(self.filter_dd_year, "options"):
            self.filter_dd_year.options = [
                ft.dropdown.Option(key=k, text=v) for k, v in years_list
            ]
        elif hasattr(self.filter_dd_year, "dropdown"):
            self.filter_dd_year.dropdown.options = [
                ft.dropdown.Option(key=k, text=v) for k, v in years_list
            ]

    def _apply_filters(self, e=None):
        sel_year = getattr(self.filter_dd_year, "value", "all")
        sel_month = getattr(self.filter_dd_month, "value", "all")
        sel_day = getattr(self.filter_dd_day, "value", "all")
        
        sel_cat_id = getattr(self.filter_dd_category, "value", "all")
        sel_orig_id = getattr(self.filter_dd_origin, "value", "all")

        min_amt = self.filter_range_slider.start_value
        max_amt = self.filter_range_slider.end_value

        cat_map = {str(c[0]): c[1] for c in self.categories_options if len(c) > 1}
        orig_map = {str(o[0]): o[1] for o in self.origins_options if len(o) > 1}

        filtered_data = []

        for item in self.data:
            y, m, d = self._parse_item_date(str(item.get("date", "")))
            if sel_year != "all" and y != sel_year:
                continue
            if sel_month != "all" and m != sel_month:
                continue
            if sel_day != "all" and d != sel_day:
                continue

            if sel_cat_id != "all":
                target_cat_name = cat_map.get(str(sel_cat_id))
                item_cat = str(item.get("category", ""))
                item_cat_id = str(item.get("category_id", ""))
                if item_cat != target_cat_name and item_cat_id != str(sel_cat_id):
                    continue

            if sel_orig_id != "all":
                target_orig_name = orig_map.get(str(sel_orig_id))
                item_orig = str(item.get("origin", ""))
                item_orig_id = str(item.get("origin_id", ""))
                if item_orig != target_orig_name and item_orig_id != str(sel_orig_id):
                    continue

            amt = self._parse_amount(item.get("amount", 0))
            if not (min_amt <= amt <= max_amt):
                continue

            filtered_data.append(item)

        if filtered_data:
            self.list_view.controls = [self._build_single_row(item) for item in filtered_data]
        else:
            self.list_view.controls = [self._build_empty_control()]

        self.filter_modal.close(e)
        self.list_view.update()

    def _clear_filters(self, e=None):
        self.filter_dd_year.value = "all"
        self.filter_dd_month.value = "all"
        self.filter_dd_day.value = "all"
        self._update_days_dropdown()

        self.filter_dd_category.value = "all"
        self.filter_dd_category.color = None
        self.filter_dd_category.fill_color = None

        self.filter_dd_origin.value = "all"
        self.filter_dd_origin.color = None
        self.filter_dd_origin.fill_color = None

        max_val = self._get_max_income_amount()
        self.filter_range_slider.start_value = 0
        self.filter_range_slider.end_value = max_val
        self.filter_lbl_min.value = "$0"
        self.filter_lbl_max.value = f"${int(max_val):,}"

        if self.data:
            self.list_view.controls = [self._build_single_row(item) for item in self.data]
        else:
            self.list_view.controls = [self._build_empty_control()]

        self.filter_modal.close(e)
        self.filter_modal.update()
        self.list_view.update()

    def _get_max_days(self, month_val: str, year_val: str) -> int:
        if not month_val or month_val == "all":
            return 31
        try:
            month = int(month_val)
        except ValueError:
            return 31

        if not year_val or year_val == "all":
            if month == 2:
                return 29  
            return calendar.monthrange(2023, month)[1]

        try:
            year = int(year_val)
            return calendar.monthrange(year, month)[1]
        except ValueError:
            if month == 2:
                return 29
            return calendar.monthrange(2023, month)[1]

    def _update_days_dropdown(self, e=None):
        year_val = getattr(self.filter_dd_year, "value", "all")
        month_val = getattr(self.filter_dd_month, "value", "all")

        max_days = self._get_max_days(month_val, year_val)

        days_list = [("all", "Todos")] + [(f"{i:02d}", str(i)) for i in range(1, max_days + 1)]

        if hasattr(self.filter_dd_day, "options_list"):
            self.filter_dd_day.options_list = days_list

        if hasattr(self.filter_dd_day, "options"):
            self.filter_dd_day.options = [
                ft.dropdown.Option(key=key, text=text) for key, text in days_list
            ]
        elif hasattr(self.filter_dd_day, "dropdown"):
            self.filter_dd_day.dropdown.options = [
                ft.dropdown.Option(key=key, text=text) for key, text in days_list
            ]

        current_day = getattr(self.filter_dd_day, "value", "all")
        if current_day and current_day != "all":
            try:
                if int(current_day) > max_days:
                    self.filter_dd_day.value = f"{max_days:02d}"
            except ValueError:
                self.filter_dd_day.value = "all"

        if hasattr(self.filter_dd_day, "page") and self.filter_dd_day.page:
            self.filter_dd_day.update()

    def _get_max_income_amount(self) -> float:
        if not self.data:
            return 100.0
        
        amounts = [self._parse_amount(item.get("amount", 0)) for item in self.data]
        max_val = max(amounts) if amounts else 0.0
        return float(math.ceil(max_val)) if max_val > 0 else 100.0

    def _update_amount_filter_range(self):
        max_val = self._get_max_income_amount()

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

    def did_mount(self):
        if self.page and self.detail_modal not in self.page.overlay:
            self.page.overlay.append(self.detail_modal)

    def will_unmount(self):
        if self.page and self.detail_modal in self.page.overlay:
            self.page.overlay.remove(self.detail_modal)

    def _open_filter_modal(self, e=None):
        self._update_years_dropdown()
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

                self._update_title_count()
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

                cat_name = next((c[1] for c in self.categories_options if str(c[0]) == str(payload["category_id"])), self.selected_item.get("category"))
                orig_name = next((o[1] for o in self.origins_options if str(o[0]) == str(payload["origin_id"])), self.selected_item.get("origin"))

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
            self.edit_modal.close(e)
            self._open_detail_modal(e, self.selected_item)

    def _handle_cancel(self, e):
        self.edit_modal.close(e)
        self._open_detail_modal(e, self.selected_item)

    def update_data(self, new_data: list[dict]):
        super().update_data(new_data)
        self._update_years_dropdown()
        self._update_amount_filter_range()
        if self.page:
            self.update()