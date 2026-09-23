# src/views/components/common/styled_textfield.py
import flet as ft

class StyledTextField(ft.TextField):
    def __init__(
        self,
        label: str | None = None,
        hint_text: str | None = None,
        prefix_icon: str | None = None,
        keyboard_type: ft.KeyboardType | None = None,
        border_radius: int = 16,
        focused_color: str = ft.Colors.BLUE,
        expand: bool = True,
        dense: bool = True,
        content_padding: ft.Padding | None = ft.Padding.all(0),
        **kwargs,
    ):
        custom_border = {
            ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                border_radius=border_radius,
                side=ft.BorderSide(color=ft.Colors.TRANSPARENT),
            ),
            ft.ControlState.FOCUSED: ft.OutlineInputBorder(
                border_radius=border_radius,
                side=ft.BorderSide(color=focused_color),
            ),
        }

        super().__init__(
            label=label,
            hint_text=hint_text,
            prefix_icon=prefix_icon,
            keyboard_type=keyboard_type,
            filled=True,
            expand=expand,
            border=custom_border,
            dense=dense,
            content_padding=content_padding,
            **kwargs,
        )

    def clean_data(self):
        self.value = None
        self.fill_color = None
        self.color = None