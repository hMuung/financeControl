# src/views/components/quick_income.py
import flet as ft

from controllers.category_controller import CategoryController
from controllers.income_controller import IncomeController
from controllers.origin_controller import OriginController
from views.components.common.base_form_card import BaseCollapsibleFormCard
from views.components.common.styled_dropdown import StyledDropdown
from views.components.common.styled_textfield import StyledTextField


class QuickIncomeCard(BaseCollapsibleFormCard):
    def __init__(self, initially_collapsed: bool = False):
        # Inicializar controladores
        self.controller = IncomeController()
        self.category_controller = CategoryController()
        self.origin_controller = OriginController()

        # Iniciar clase base (build_fields())
        super().__init__(
            title="INGRESO",
            title_icon=ft.Icons.TRENDING_UP_ROUNDED,
            button_text="Añadir",
            initially_collapsed=initially_collapsed,
        )

    def build_fields(self) -> list[ft.Control]:
        # Cargar datos desde los controladores
        categories = self.category_controller.get_income_categories()
        origins = self.origin_controller.get_income_origins()

        category_options = [
            (cat.id, cat.name, cat.color, cat.bg_color) for cat in categories
        ]
        origin_options = [
            (orig.id, orig.name, orig.color, orig.bg_color) for orig in origins
        ]

        # Campo Categoria/Tipo
        self.dd_category = StyledDropdown(
            label="Tipo",
            leading_icon=ft.Icons.CATEGORY_OUTLINED,
            options_list=category_options,
        )

        # Campo Origen/Destino
        self.dd_origin = StyledDropdown(
            label="Destino",
            hint_text="Selecciona el medio de pago",
            leading_icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
            options_list=origin_options,
        )

        # Campo Monto
        self.txt_amount = StyledTextField(
            label="Monto",
            hint_text="0.00",
            format_numeric=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.ATTACH_MONEY,
        )

        # Campo Descripcion
        self.txt_description = StyledTextField(
            label="Descripcion",
            hint_text="Nota adicional...",
            prefix_icon=ft.Icons.DESCRIPTION_OUTLINED,
        )

        return [
            self.dd_category,
            self.dd_origin,
            self.txt_amount,
            self.txt_description,
        ]

    def handle_submit(self) -> tuple[bool, str]:
        # Invocar la logica del controlador de ingresos
        return self.controller.create_income(
            category_id=self.dd_category.key,
            amount_str=self.txt_amount.value,
            origin_id=self.dd_origin.key,
            description=self.txt_description.value,
        )