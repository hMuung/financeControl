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
        format_numeric: bool = False,
        on_change=None,
        **kwargs,
    ):
        self.format_numeric = format_numeric
        self._user_on_change = on_change

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
            on_change=self._on_text_change,
            **kwargs,
        )

    def _on_text_change(self, e):
        if self.format_numeric:
            digits = "".join(c for c in (self.value or "") if c.isdigit())
            if digits:
                self.value = f"{int(digits):,}"
            else:
                self.value = ""
            self.update()

        if self._user_on_change:
            self._user_on_change(e)

    def clean_data(self):
        self.value = None
        self.fill_color = None
        self.color = None