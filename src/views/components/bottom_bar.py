# src/views/components/bottom_bar.py 
import flet as ft
from views.utils.theme import (
    GLASS_BG_COLOR,
    GLASS_BORDER_COLOR,
    GLASS_BORDER_RADIUS,
    BUTTON_GRADIENT,
    INACTIVE_ICON_COLOR,
    TRANSPARENT_GRADIENT,
)

class ModernGlassBottomBar(ft.Container):
    def __init__(self, on_change=None):
        self.selected_index = 0
        self.on_change = on_change

        # Items
        self.items_data = [
            {"icon": ft.Icons.HOME_ROUNDED, "label": "Inicio"},
            {"icon": ft.Icons.RECEIPT_LONG_ROUNDED, "label": "Historial"},
            {"icon": ft.Icons.TRENDING_UP_ROUNDED, "label": "Proyeccion"},
            {"icon": ft.Icons.DONUT_LARGE_ROUNDED, "label": "Analisis"},
            {"icon": ft.Icons.MORE_HORIZ_ROUNDED, "label": "Mas"},
        ]

        self.item_controls = []
        self.row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        super().__init__(
            content=self.row,
            bgcolor=GLASS_BG_COLOR,
            border=ft.Border.all(1.5, GLASS_BORDER_COLOR),
            border_radius=GLASS_BORDER_RADIUS + 10,
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            blur=ft.Blur(20, 20, ft.BlurTileMode.CLAMP),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                offset=ft.Offset(0, 10),
            ),
        )
        self._build_items()

    def _build_items(self):
        row_controls = []
        for i, item in enumerate(self.items_data):
            is_selected = (i == self.selected_index)

            icon_ctrl = ft.Icon(
                item["icon"],
                color=ft.Colors.WHITE if is_selected else INACTIVE_ICON_COLOR,
                size=22,
            )

            text_ctrl = ft.Text(
                item["label"],
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
                size=11,
                visible=is_selected,
            )

            btn_container = ft.Container(
                content=ft.Row(
                    controls=[icon_ctrl, text_ctrl],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=ft.Padding.symmetric(
                    horizontal=16 if is_selected else 12, 
                    vertical=10
                ),
                border_radius=GLASS_BORDER_RADIUS,
                gradient=BUTTON_GRADIENT if is_selected else TRANSPARENT_GRADIENT,
                animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
                on_click=lambda e, idx=i: self._select_item(idx),
            )

            self.item_controls.append({
                "container": btn_container,
                "icon": icon_ctrl,
                "text": text_ctrl,
            })
            row_controls.append(btn_container)

        self.row.controls = row_controls

    def set_selected_index(self, index: int, notify: bool = False):
        """Actualiza la interfaz visual de la barra"""
        if index < 0 or index >= len(self.item_controls):
            return
        if self.selected_index == index and not notify:
            return

        self.selected_index = index

        for i, item in enumerate(self.item_controls):
            is_selected = (i == self.selected_index)
            
            item["icon"].color = ft.Colors.WHITE if is_selected else INACTIVE_ICON_COLOR
            item["text"].visible = is_selected
            item["container"].gradient = BUTTON_GRADIENT if is_selected else TRANSPARENT_GRADIENT
            item["container"].padding = ft.Padding.symmetric(
                horizontal=16 if is_selected else 12, 
                vertical=10
            )

        self.update()

        # Notifica al padre si el cambio se origin dentro de la barra
        if notify and self.on_change:
            self.on_change(self.selected_index)

    def _select_item(self, index):
        self.set_selected_index(index, notify=True)