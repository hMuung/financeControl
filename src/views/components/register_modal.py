# src/views/components/register_modal.py
import flet as ft

from views.components.common.amount_textfield import AmountTextField
from views.components.common.base_button import cancel_button, save_button
from views.components.common.base_dropdown import BaseDropdown
from views.components.common.desciption_textfield import DescriptionTextField
from views.components.common.modal_base import ModalBase
from views.utils.theme import (
    ALERT_COLOR,
    COLOR_ACCENT_PRIMARY,
    EXPENSE_COLOR,
    INCOME_COLOR,
    INPUT_BG_IDLE,
    TEXT_MUTED,
    TEXT_PRIMARY,
)


@ft.control
class RegisterModal(ModalBase):

    def init(self):
        self.modal = True
        self.selected_type: str = "Ingreso"
        self._buttons: dict[str, tuple[ft.Container, ft.Text]] = {}

        self._type_colors = {
            "Ingreso": INCOME_COLOR,
            "Egreso": EXPENSE_COLOR,
            "Transferencia": COLOR_ACCENT_PRIMARY,
        }

        self.OPCIONES_DICT = {
            "ingreso": [
                ("Nómina", "#000000", INCOME_COLOR, ft.Icons.ATTACH_MONEY_ROUNDED),
                ("Ventas", "#FFFFFF", COLOR_ACCENT_PRIMARY, ft.Icons.STORE_ROUNDED),
                ("Inversiones", "#FFFFFF", ALERT_COLOR, ft.Icons.SHOW_CHART_ROUNDED),
                ("Freelance", "#FFFFFF", EXPENSE_COLOR, ft.Icons.WORK_ROUNDED),
            ],
            "egreso": [
                ("Alimentación", "#FFFFFF", EXPENSE_COLOR, ft.Icons.RESTAURANT_ROUNDED),
                ("Servicios", "#000000", ALERT_COLOR, ft.Icons.LIGHTBULB_ROUNDED),
                ("Transporte", "#FFFFFF", COLOR_ACCENT_PRIMARY, ft.Icons.DIRECTIONS_BUS_ROUNDED),
                ("Salud", "#FFFFFF", INCOME_COLOR, ft.Icons.LOCAL_HOSPITAL_ROUNDED),
            ],
            "cuentas": [
                ("Efectivo", "#000000", INCOME_COLOR, ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED),
                ("Banco", "#FFFFFF", ALERT_COLOR, ft.Icons.ACCOUNT_BALANCE_ROUNDED),
                ("Tarjeta", "#FFFFFF", COLOR_ACCENT_PRIMARY, ft.Icons.CREDIT_CARD_ROUNDED),
            ],
        }

        header = ft.Container(
            width=float("inf"),
            height=40,
            padding=0,
            border=ft.Border(bottom=ft.BorderSide(1, TEXT_MUTED)),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value="Registro",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_ROUNDED,
                        icon_color=TEXT_PRIMARY,
                        icon_size=20,
                        tooltip="Volver",
                        on_click=self._handle_back,
                    ),
                ],
            ),
        )

        selector_controls = []
        options = list(self._type_colors.keys())

        for i, option in enumerate(options):
            is_selected = option == self.selected_type

            if i == 0:
                btn_radius = ft.BorderRadius.only(top_left=20, bottom_left=20)
            elif i == len(options) - 1:
                btn_radius = ft.BorderRadius.only(top_right=20, bottom_right=20)
            else:
                btn_radius = ft.BorderRadius.all(0)

            text_ctrl = ft.Text(
                value=option,
                size=12,
                weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.W_500,
                color=self._get_text_color(is_selected),
            )

            btn_container = ft.Container(
                expand=True,
                height=36,
                alignment=ft.Alignment.CENTER,
                bgcolor=self._get_bg_color(option, is_selected),
                animate=ft.Animation(100, ft.AnimationCurve.EASE_IN_OUT),
                content=text_ctrl,
                on_click=lambda e, opt=option: self._select_option(opt),
                border_radius=btn_radius,
            )

            self._buttons[option] = (btn_container, text_ctrl)
            selector_controls.append(btn_container)

            if i < len(options) - 1:
                selector_controls.append(
                    ft.Container(
                        width=1,
                        height=36,
                        bgcolor="#FFFFFF",
                    )
                )

        self._selector_row = ft.Row(
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=selector_controls,
        )

        selector_bar = ft.Container(
            bgcolor=INPUT_BG_IDLE,
            border=ft.Border.all(1, color="#FFFFFF"),
            border_radius=20,
            padding=0,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=self._selector_row,
        )

        self.amount_input = AmountTextField()

        self.category_dropdown = BaseDropdown(
            options_dict=self.OPCIONES_DICT,
            default_key="ingreso",
            label="Categoría",
            border_radius=16,
            max_menu_height=180,
        )

        self.account_dropdown = BaseDropdown(
            options_dict=self.OPCIONES_DICT,
            default_key="cuentas",
            label="Destino",
            border_radius=16,
            max_menu_height=180,
        )

        self.description_input = DescriptionTextField(
            label="Descripción opcional",
            border_radius=16,
        )

        self.description_row = ft.Row(
            tight=True,
            controls=[self.description_input],
        )

        self.body = ft.Column(
            tight=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                header,
                selector_bar,
                self.amount_input,
                self.description_row,
                ft.Row(
                    tight=True,
                    controls=[self.category_dropdown],
                ),
                ft.Row(
                    tight=True,
                    controls=[self.account_dropdown],
                ),
                ft.Row(
                    tight=True,
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        cancel_button(on_click=self._handle_back),
                        save_button(on_click=self._handle_save),
                    ],
                ),
            ],
        )

        super().init()

    def _get_bg_color(self, option: str, is_selected: bool) -> str:
        if not is_selected:
            return ft.Colors.TRANSPARENT
        return self._type_colors.get(option, COLOR_ACCENT_PRIMARY)

    def _get_text_color(self, is_selected: bool) -> str:
        return TEXT_PRIMARY if is_selected else TEXT_MUTED

    def _select_option(self, option: str):
        if self.selected_type == option:
            return

        self.selected_type = option

        # Barra de categoria
        for opt, (container, text_ctrl) in self._buttons.items():
            is_sel = opt == option
            container.bgcolor = self._get_bg_color(opt, is_sel)
            text_ctrl.color = self._get_text_color(is_sel)
            text_ctrl.weight = ft.FontWeight.BOLD if is_sel else ft.FontWeight.W_500

        # Limpiar entradas
        self.amount_input.amount = 0
        self.description_input.clean_data()
        self.account_dropdown.clean_data()
        self.category_dropdown.clean_data()

        # Actualizacion de dd segun opcion de barra
        if option == "Ingreso":
            self.description_row.visible = True
            self.category_dropdown.set_dropdown(label="Categoría", key="ingreso")
            self.account_dropdown.set_dropdown(label="Destino", key="cuentas")

        elif option == "Egreso":
            self.description_row.visible = True
            self.category_dropdown.set_dropdown(label="Categoría", key="egreso")
            self.account_dropdown.set_dropdown(label="Origen", key="cuentas")

        elif option == "Transferencia":
            self.description_row.visible = False
            self.category_dropdown.set_dropdown(label="Origen", key="cuentas")
            self.account_dropdown.set_dropdown(label="Destino", key="cuentas")

        # Refrescar interfaz
        if self.body and self.body.page:
            self.body.update()

    def _handle_save(self, e):
        monto = self.amount_input.amount
        descripcion = self.description_input.value if self.description_row.visible else ""
        categoria_o_origen = self.category_dropdown.value
        cuenta_o_destino = self.account_dropdown.value

        print(f"[{self.selected_type}] {monto=}, {descripcion=}, {categoria_o_origen=}, {cuenta_o_destino=}")
        self._handle_back(e)

    def _handle_back(self, e):
        e.page.pop_dialog()
        self.page.update(self)