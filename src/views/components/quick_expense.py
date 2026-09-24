# src/views/components/quick_expense.py
import flet as ft

from controllers.expense_controller import ExpenseController
from controllers.category_controller import CategoryController
from controllers.origin_controller import OriginController
from views.components.common.glass_card import GlassCard
from views.components.common.gradient_button import GradientButton
from views.components.common.styled_dropdown import StyledDropdown
from views.components.common.styled_textfield import StyledTextField
from views.utils.theme import BUTTON_GRADIENT
from views.utils.toast import Toast


class QuickExpenseCard(GlassCard):
    def __init__(self):
        # Instancias de los controladores
        self.controller = ExpenseController()
        self.category_controller = CategoryController()
        self.origin_controller = OriginController()

        # Cargar datos dinamicos desde la base de datos
        categories = self.category_controller.get_all_categories()
        origins = self.origin_controller.get_all_origins()

        # Mapear los modelos a tuplas
        category_options = [
            (cat.id, cat.name, cat.color, cat.bg_color) for cat in categories
        ]
        
        origin_options = [
            (orig.id, orig.name, orig.color, orig.bg_color) for orig in origins
        ]

        # Campo Categoria con datos dinamicos
        self.dd_category = StyledDropdown(
            label="Categoria",
            leading_icon=ft.Icons.CATEGORY_OUTLINED,
            options_list=category_options,
        )

        # Campo Monto
        self.txt_amount = StyledTextField(
            label="Monto",
            hint_text="0.00",
            format_numeric=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.ATTACH_MONEY,
        )

        # Campo Origen con datos dinamicos
        self.dd_origin = StyledDropdown(
            label="Origen",
            hint_text="Selecciona el medio de pago",
            leading_icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
            options_list=origin_options,
        )

        # Campo Descripcion (Opcional)
        self.txt_description = StyledTextField(
            label="Descripcion",
            hint_text="Nota adicional...",
            prefix_icon=ft.Icons.DESCRIPTION_OUTLINED,
        )

        # Boton Añadir
        self.btn_add = GradientButton(
            text="Añadir",
            gradient=BUTTON_GRADIENT,
            icon=ft.Icons.ADD,
            on_click=self._on_add_click,
        )

        # Estructura visual del componente
        super().__init__(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("GASTO", weight=ft.FontWeight.BOLD, size=16),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    self.dd_category,
                    self.dd_origin,
                    self.txt_amount,
                    self.txt_description,
                    ft.Row(
                        controls=[self.btn_add],
                        alignment=ft.MainAxisAlignment.END,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
            )
        )

    def _on_add_click(self, e):
        # Obtener valores de la interfaz
        category = self.dd_category.key
        amount = self.txt_amount.value
        origin = self.dd_origin.key
        description = self.txt_description.value

        # Proceso de la validacion y guardado
        success, message = self.controller.create_expense(
            category_id=category,
            amount_str=amount,
            origin_id=origin,
            description=description,
        )

        # Mostrar respuesta segun el resultado
        if success:
            Toast.success(self.page, message)
            # Limpiar entradas de la UI
            self.dd_category.clean_data()
            self.txt_amount.clean_data()
            self.dd_origin.clean_data()
            self.txt_description.clean_data()
        else:
            Toast.error(self.page, message)

        self.update()