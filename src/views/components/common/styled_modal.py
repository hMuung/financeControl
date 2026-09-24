# src/views/components/common/styled_modal.py
import flet as ft
from views.utils.theme import BACKGROUND_GRADIENT, MODAL_SHADOW, HEADER_TEXT_COLOR


class StyledModal(ft.Container):

    def __init__(
        self,
        title: str = "Modal",
        title_size: int = 18,
        title_color: str = HEADER_TEXT_COLOR,
        close_icon: ft.Icons = ft.Icons.CLOSE,
        close_icon_color: str = HEADER_TEXT_COLOR,
        content: ft.Container | None = None,
        padding: ft.Padding = ft.Padding.symmetric(vertical=5, horizontal=8)
    ):  

        if not content:
            content = ft.Container(
                padding=ft.Padding.symmetric(vertical=20),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Icon(
                            ft.Icons.CONSTRUCTION_ROUNDED,
                            size=36,
                            color=HEADER_TEXT_COLOR,
                        ),
                        ft.Text(
                            "Próximamente",
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=HEADER_TEXT_COLOR,
                        ),
                    ],
                ),
            )

        self.is_open = False

        modal_header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    title,
                    size=title_size,
                    weight=ft.FontWeight.BOLD,
                    color=title_color,
                ),
                ft.IconButton(
                    icon=close_icon,
                    icon_color=close_icon_color,
                    on_click=self.close,
                ),
            ],
        )

        self.modal_card_content = ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                modal_header,
                content
            ]
        )

        self.modal_card = ft.Container(
            width=float("inf"),
            padding=padding,
            border_radius=24,
            gradient=BACKGROUND_GRADIENT,
            border=ft.Border.all(1.5, ft.Colors.WHITE),
            shadow= MODAL_SHADOW,
            on_click=lambda e: None,
            content=self.modal_card_content
        )

        super().__init__(
            visible=False,
            expand=True,
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
            blur=ft.Blur(sigma_x=25, sigma_y=25),
            alignment=ft.Alignment.CENTER,
            on_click=self.close,
            content=self.modal_card
        )

    def _get_page(self, e=None):
        if e and hasattr(e, "page") and e.page:
            return e.page
        return self.page

    def open(self, e=None):
        page = self._get_page(e)
        if page:
            if self not in page.overlay:
                page.overlay.append(self)
            self.visible = True
            self.is_open=True
            page.update()

    def close(self, e=None):
        if self.is_open:
            self.visible = False
            page = self._get_page(e)
            if page:
                page.update()
