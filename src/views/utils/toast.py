# src/views/utils/toast.py
import flet as ft
from src.views.utils.theme import TOAST_COLORS


class Toast:
    @staticmethod
    def success(page: ft.Page, message: str, duration: int = 3000):
        Toast._show(
            page=page,
            message=message,
            toast_type="success",
            icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
            duration=duration,
        )

    @staticmethod
    def error(page: ft.Page, message: str, duration: int = 3000):
        Toast._show(
            page=page,
            message=message,
            toast_type="error",
            icon=ft.Icons.ERROR_OUTLINE,
            duration=duration,
        )

    @staticmethod
    def warning(page: ft.Page, message: str, duration: int = 3000):
        Toast._show(
            page=page,
            message=message,
            toast_type="warning",
            icon=ft.Icons.WARNING_AMBER_ROUNDED,
            duration=duration,
        )

    @staticmethod
    def info(page: ft.Page, message: str, duration: int = 3000):
        Toast._show(
            page=page,
            message=message,
            toast_type="info",
            icon=ft.Icons.INFO_OUTLINE,
            duration=duration,
        )

    @staticmethod
    def _show(page: ft.Page, message: str, toast_type: str, icon: str, duration: int):
        if not page:
            return
        
        colors = TOAST_COLORS.get(
            toast_type,
            {"primary": ft.Colors.BLUE_700, "secondary": ft.Colors.BLUE_500},
        )
        primary_color = colors["primary"]
        secondary_color = colors["secondary"]
        radius = 16  # Radio para bordes

        snack_bar = ft.SnackBar(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(icon, color=ft.Colors.WHITE, size=20),
                        ft.Text(
                            message,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.W_500,
                            expand=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                    colors=[primary_color, secondary_color],
                ),
                padding=ft.Padding.symmetric(vertical=12, horizontal=16),
            ),
            bgcolor=ft.Colors.TRANSPARENT,
            elevation=0,
            duration=duration,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.Margin.all(15),
            padding=0,
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            shape=ft.RoundedRectangleBorder(radius=radius),
        )

        page.show_dialog(snack_bar)