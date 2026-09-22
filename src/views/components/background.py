# src/views/components/background.py
import flet as ft

from views.utils.theme import BACKGROUND_GRADIENT

def Background() -> ft.Container :
    return ft.Container(
            expand=True,
            gradient=BACKGROUND_GRADIENT,
        )
