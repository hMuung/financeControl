# src/views/components/background.py
import flet as ft

from views.utils.theme import BACKGROUND_GRADIENT


@ft.control
class Background(ft.Container):
    expand: bool = True

    def init(self):
        self.gradient = BACKGROUND_GRADIENT