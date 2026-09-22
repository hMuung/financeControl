import flet as ft

from views.components.common.glass_card import GlassCard
from views.components.common.gradient_button import GradientButton
from views.components.common.styled_dropdown import StyledDropdown
from views.components.common.styled_textfield import StyledTextField
from views.utils.theme import BUTTON_GRADIENT

class QuickExpenseCard(GlassCard):
    def __init__(self):
        # 1. Campo Categoria
        self.dd_category = StyledDropdown(
            label="Categoria",
            leading_icon=ft.Icons.CATEGORY_OUTLINED,
            options_list=[
                ("Comida", ft.Colors.GREEN_700, ft.Colors.GREEN_100),
                ("Transporte", ft.Colors.ORANGE_700, ft.Colors.ORANGE_100),
               ("Servivios", ft.Colors.RED_700, ft.Colors.RED_100)
            ]
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

        # 4. Boton Añadir
        self.btn_add = GradientButton(
            text="Añadir",
            gradient=BUTTON_GRADIENT,
            icon=ft.Icons.ADD,
            on_click=self._on_add_click,
        )

        # Etiqueta para mostrar mensaje de error
        self.label = ft.Text(
            value="",
            color=ft.Colors.RED_400,
            size=16,
            weight=ft.FontWeight.W_500
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
                    ft.Row(
                        controls=[self.label, self.btn_add],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
            )
        )

    def _on_add_click(self, e):
        category = self.dd_category.value
        amount = self.txt_amount.value
        origin = self.dd_origin.value

        # Validar si alguno de los campos está vacío
        message = ""
        if not category:
            message = "Falta Categoria."
        if not amount:
            message = "Falta Cantidad."
        if not origin:
            message = "Falta Origen."

        if message:
            self.label.value = message
            self.label.color=ft.Colors.RED_400
            self.update()
            return

        # Marcar como registrado y liberar campos
        self.label.value = "Registro correcto"
        self.label.color=ft.Colors.GREEN_400
        self.dd_category.clean_data()
        self.txt_amount.clean_data()
        self.dd_origin.clean_data()
        self.update()

        print(f"Añadido: {category}, {amount}, {origin}")