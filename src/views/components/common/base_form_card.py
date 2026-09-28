# views/components/common/base_form_card.py
import flet as ft

from views.components.common.glass_card import GlassCard
from views.components.common.gradient_button import GradientButton
from views.utils.theme import BUTTON_GRADIENT
from views.utils.toast import Toast


class BaseCollapsibleFormCard(GlassCard):
    def __init__(
        self,
        title: str,
        title_icon: str = None,
        button_text: str = "Añadir",
        initially_collapsed: bool = True,
        collapsed_height: int = 50,
    ):
        self.title_text = title
        self.title_icon = title_icon
        self.button_text = button_text
        self.is_collapsed = initially_collapsed
        self.collapsed_height = collapsed_height

        # Campos especificos
        self.fields = self.build_fields()

        # Boton de accion generico
        self.btn_submit = GradientButton(
            text=self.button_text,
            gradient=BUTTON_GRADIENT,
            icon=ft.Icons.ADD,
            on_click=self._on_submit_click,
        )

        # Boton para colapsar/extender
        self.btn_toggle = ft.IconButton(
            icon=ft.Icons.KEYBOARD_ARROW_UP if not self.is_collapsed else ft.Icons.KEYBOARD_ARROW_DOWN,
            tooltip="Colapsar" if not self.is_collapsed else "Expandir",
            on_click=self._toggle_collapse,
        )

        # Encabezado (Titulo + Icono + Boton de colapso)
        header_title_row = ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
            controls=[
                *( [ft.Icon(self.title_icon, size=20)] if self.title_icon else [] ),
                ft.Text(self.title_text, weight=ft.FontWeight.BOLD, size=16),
            ]
        )

        self.header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                header_title_row,
                self.btn_toggle,
            ],
        )

        # Cuerpo del formulario (Campos + Boton de enviar)
        self.body_container = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            visible=not self.is_collapsed,
            animate_opacity=200,  # Transicion visual suave de ocultar mostrar
            controls=[
                *self.fields,
                ft.Row(
                    controls=[self.btn_submit],
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
        )

        # Construccion del GlassCard
        super().__init__(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.header,
                    self.body_container,
                ],
            )
        )

    def _toggle_collapse(self, e):
        """Alterna visibilidad del contenido y cambia el icono."""
        self.is_collapsed = not self.is_collapsed
        self.body_container.visible = not self.is_collapsed
        self.btn_toggle.icon = (
            ft.Icons.KEYBOARD_ARROW_UP if not self.is_collapsed else ft.Icons.KEYBOARD_ARROW_DOWN
        )
        self.btn_toggle.tooltip = "Colapsar" if not self.is_collapsed else "Expandir"
        self.update()

    def _on_submit_click(self, e):
        """Procesa el formulario y maneja las notificaciones Toast"""

        success, message = self.handle_submit()
        if success:
            Toast.success(self.page, message)
            self.clear_fields()
        else:
            Toast.error(self.page, message)
        self.update()

    def clear_fields(self):
        """Limpia todos los controles del formulario"""
        for field in self.fields:
            if hasattr(field, "clean_data"):
                field.clean_data()
            elif hasattr(field, "value"):
                field.value = ""

    # Metodos que deben de tener las subclases
    def build_fields(self) -> list[ft.Control]:
        """Devuelve la lista de componentes/controles del formulario."""
        raise NotImplementedError("Debe implementar build_fields() en la subclase")

    def handle_submit(self) -> tuple[bool, str]:
        """Procesa la logica de negocio y retorna (exito, mensaje)."""
        raise NotImplementedError("Debe implementar handle_submit() en la subclase")