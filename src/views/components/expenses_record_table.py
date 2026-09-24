# src/views/components/expenses_record_table.py
import flet as ft

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


class GastosGlassTable(GlassDataTable):

    def __init__(
        self,
        title: str = "Gastos",
        columns_config: list[dict] = None,
        data: list[dict] = None,
        categories_options: list = None,
        origins_options: list = None,
        empty_message: str = "No hay datos registrados.",
        on_delete=None,
        on_edit=None,
    ):
        columns_config = columns_config or [
            {"label": "Fecha", "key": "date", "numeric": False},
            {"label": "Categoría", "key": "category", "numeric": False},
            {"label": "Monto", "key": "amount", "numeric": True},
            {"label": "Origen", "key": "origin", "numeric": False},
        ]

        self.on_delete = on_delete
        self.on_edit = on_edit
        self.categories_options = categories_options or []
        self.origins_options = origins_options or []

        # Boton de filtros
        btn_filter_trigger = ft.IconButton(
            icon=ft.Icons.FILTER_LIST,
            icon_color=HEADER_TEXT_COLOR,
            tooltip="Abrir Filtros",
            on_click=self._open_filter_modal,
        )

        # Inicializacion de la clase padre
        super().__init__(
            title=title,
            columns_config=columns_config,
            data=data or [],
            empty_message=empty_message,
            on_row_click=self._open_detail_modal,
            action_button=btn_filter_trigger,
        )

        # Configuracion de Modales
        self.filter_modal = StyledModal(title="Filtrar", content=None)
        self._init_detail_modal()
        self._init_edit_modal()

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
            title="Detalles del registro",
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
            hint_text="0.00",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.edit_tf_description = StyledTextField(
            label="Descripcion",
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
            title="Edicion de registro",
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

    # Ciclo de vida para overlay de modales
    def did_mount(self):
        if self.page and self.detail_modal not in self.page.overlay:
            self.page.overlay.append(self.detail_modal)

    def will_unmount(self):
        if self.page and self.detail_modal in self.page.overlay:
            self.page.overlay.remove(self.detail_modal)

    # Handlers y Control de Modales
    def _open_filter_modal(self, e=None):
        self.filter_modal.open(e)

    def _open_detail_modal(self, e, item: dict):
        num_val = self._parse_amount(item.get("amount", 0))

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

        self.edit_dd_category.value = str(cat_match[0]) if cat_match else None
        self.edit_dd_origin.value = str(orig_match[0]) if orig_match else None
        self.edit_tf_amount.value = str(item.get("amount", ""))
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
                self._open_detail_modal(e, self.selected_item)
            else:
                Toast.error(page, message)
        else:
            self.edit_modal.close(e)
            self._open_detail_modal(e, self.selected_item)

    def _handle_cancel(self, e):
        self.edit_modal.close(e)
        self._open_detail_modal(e, self.selected_item)