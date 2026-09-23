# src/views/components/quick_expense.py
import flet as ft

from controllers.expense_controller import ExpenseController
from views.components.common.glass_card import GlassCard
from views.components.common.gradient_button import GradientButton
from views.components.common.styled_dropdown import StyledDropdown
from views.components.common.styled_textfield import StyledTextField
from views.utils.theme import BUTTON_GRADIENT
from views.utils.toast import Toast


class QuickExpenseCard(GlassCard):
    def __init__(self):
        # Instancia del controlador
        self.controller = ExpenseController()

        # 1. Campo Categoria
        self.dd_category = StyledDropdown(
            label="Categoria",
            leading_icon=ft.Icons.CATEGORY_OUTLINED,
            options_list=[
                ("Comida", ft.Colors.GREEN_700, ft.Colors.GREEN_100),
                ("Transporte", ft.Colors.ORANGE_700, ft.Colors.ORANGE_100),
                ("Servicios", ft.Colors.RED_700, ft.Colors.RED_100),
            ],
        )

        # 2. Campo Monto
        self.txt_amount = StyledTextField(
            label="Monto",
            hint_text="0.00",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.ATTACH_MONEY,
        )

        # 3. Campo Origen
        self.dd_origin = StyledDropdown(
            label="Origen",
            hint_text="Selecciona el medio de pago",
            leading_icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
            options_list=["Efectivo", "Tarjeta de Débito", "Tarjeta de Crédito"],
        )

        # 4. Campo Descripcion (Opcional)
        self.txt_description = StyledTextField(
            label="Descripcion",
            hint_text="Nota adicional...",
            prefix_icon=ft.Icons.DESCRIPTION_OUTLINED,
        )

        # 5. Boton Añadir
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
                    self.txt_amount,
                    self.dd_origin,
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
        category = self.dd_category.value
        amount = self.txt_amount.value
        origin = self.dd_origin.value
        description = self.txt_description.value

        # Proceso de la validacion y guardado
        success, message = self.controller.create_expense(
            category=category,
            amount_str=amount,
            origin=origin,
            description=description,
        )

        # Mostrar respuesta segun el resultado
        if success:
            Toast.success(self.page,message)
            # Limpiar entradas de la UI
            self.dd_category.clean_data()
            self.txt_amount.clean_data()
            self.dd_origin.clean_data()
            self.txt_description.clean_data()
        else:
            Toast.error(self.page,message)

        self.update()