# src/views/components/common/floating_button.py
import flet as ft

from views.utils.theme import GRADIENT_BTN_PRIMARY, TEXT_PRIMARY, FLOATING_BUTTON_SHADOW


@ft.control
class FloatingButton(ft.Container):
    icon: str = ft.Icons.ADD
    icon_color: str = TEXT_PRIMARY
    icon_size: int = 25
    size: float = 56.0

    def init(self):
        self.width = self.size
        self.height = self.size
        self.border_radius = self.size / 2
        self.gradient = GRADIENT_BTN_PRIMARY
        self.alignment = ft.Alignment.CENTER
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS
        self.ink = True

        self.shadow = FLOATING_BUTTON_SHADOW

        self.content = ft.Icon(
            icon=self.icon,
            color=self.icon_color,
            size=self.icon_size,
        )