# src/views/components/common/glass_card.py
import flet as ft
from views.utils.theme import GLASS_BG_COLOR, GLASS_BORDER_COLOR, GLASS_BORDER_RADIUS

class GlassCard(ft.Container):
    """Contenedor base con efecto cristal/espejo."""

    def __init__(
        self,
        content: ft.Control = None,
        padding: ft.Padding = ft.Padding.symmetric(vertical=8,horizontal=8),
        border_radius: int = GLASS_BORDER_RADIUS,
        width: float = float("inf"),  # Ocupa todo el ancho disponible
        **kwargs
    ):
        super().__init__(
            padding=padding,
            border_radius=border_radius,
            bgcolor=GLASS_BG_COLOR,
            border=ft.border.Border.all(1, GLASS_BORDER_COLOR),
            content=content,
            width=width,
            **kwargs
        )