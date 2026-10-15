# src/views/components/common/amount_textfield.py
import flet as ft


from views.utils.theme import (
    COLOR_ACCENT_PRIMARY,
    TEXT_MUTED,
    TEXT_PRIMARY,
)


@ft.control
class AmountTextField(ft.Column):
    label_text: str = "Monto"
    initial_amount: float = 0.0

    def init(self):
        self.spacing = 0
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self._numeric_value: float = self.initial_amount

        self.label_control = ft.Text(
            value=self.label_text,
            size=15,
            color=TEXT_PRIMARY,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
        )

        formatted_init = ""
        if self.initial_amount > 0:
            formatted_init = (
                f"{int(self.initial_amount):,}"
                if self.initial_amount.is_integer()
                else f"{self.initial_amount:,.2f}"
            )

        self.input_field = ft.TextField(
            value=formatted_init,
            hint_text="$0.00",
            prefix="$",
            prefix_style=ft.TextStyle(
                color=TEXT_PRIMARY,
                weight=ft.FontWeight.BOLD,
                size=20,
            ),
            hint_style=ft.TextStyle(
                color=TEXT_MUTED,
                weight=ft.FontWeight.BOLD,
                size=20,
            ),
            text_size=20,
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(
                color=TEXT_PRIMARY,
                weight=ft.FontWeight.BOLD,
            ),
            border={
                ft.ControlState.DEFAULT: ft.UnderlineInputBorder(
                    side=ft.BorderSide(color=COLOR_ACCENT_PRIMARY, width=1)
                ),
                ft.ControlState.FOCUSED: ft.UnderlineInputBorder(
                    side=ft.BorderSide(color=COLOR_ACCENT_PRIMARY, width=2)
                ),
            },
            bgcolor=ft.Colors.TRANSPARENT,
            content_padding=ft.Padding.symmetric(horizontal=0, vertical=8),
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._handle_change,
        )

        self.controls = [
            self.label_control,
            self.input_field,
        ]

    def _handle_change(self, e: ft.ControlEvent):
        raw_val = e.control.value or ""

        # Mantener solo digitos y un unico punto
        cleaned = ""
        has_dot = False
        for char in raw_val:
            if char.isdigit():
                cleaned += char
            elif char == "." and not has_dot:
                cleaned += char
                has_dot = True

        if not cleaned:
            self._numeric_value = 0.0
            e.control.value = ""
        else:
            parts = cleaned.split(".")
            int_part = parts[0]
            dec_part = parts[1][:2] if len(parts) > 1 else None

            formatted_int = f"{int(int_part):,}" if int_part else "0"

            if dec_part is not None:
                e.control.value = f"{formatted_int}.{dec_part}"
                self._numeric_value = float(f"{int_part or 0}.{dec_part}")
            elif has_dot:
                e.control.value = f"{formatted_int}."
                self._numeric_value = float(int_part or 0)
            else:
                e.control.value = formatted_int
                self._numeric_value = float(int_part or 0)

        if self.page:
            self.page.update(self)

    @property
    def amount(self) -> float:
        return self._numeric_value

    @amount.setter
    def amount(self, val: float):
        self._numeric_value = val
        if val == 0:
            self.input_field.value = ""
        elif val.is_integer():
            self.input_field.value = f"{int(val):,}"
        else:
            self.input_field.value = f"{val:,.2f}"

        if self.page:
            self.page.update(self)