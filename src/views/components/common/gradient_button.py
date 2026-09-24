# src/views/components/common/gradient_button.py
import flet as ft

class GradientButton(ft.Container):
    def __init__(
        self,
        text: str = "",
        icon: str | None = None,
        gradient: ft.Gradient | None = None,
        on_click=None,
        text_color: str = ft.Colors.WHITE,
        icon_color: str = ft.Colors.WHITE,
        border_radius: float | ft.BorderRadius = 10,
        padding: ft.Padding | float | None = None,
        width: float | None = None,
        height: float | None = None,
        disabled: bool = False,
        **kwargs
    ):
        # Construccion del contenido interno (Icono + Texto)
        controls = []
        if icon:
            controls.append(ft.Icon(icon, color=icon_color, size=18))
        if text:
            controls.append(
                ft.Text(text, color=text_color, weight=ft.FontWeight.BOLD)
            )

        # Padding por defecto estilo boton
        button_padding = (
            padding
            if padding is not None
            else ft.Padding.symmetric(vertical=10, horizontal=20)
        )

        super().__init__(
            content=ft.Row(
                controls=controls,
                alignment=ft.MainAxisAlignment.CENTER,
                tight=True,
                spacing=8,
            ),
            gradient=gradient,
            border_radius=border_radius,
            padding=button_padding,
            on_click=on_click if not disabled else None,
            ink=not disabled,  # Efecto ripple/onda al presionar
            width=width,
            height=height,
            disabled=disabled,
            **kwargs
        )