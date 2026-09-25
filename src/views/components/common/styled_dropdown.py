# src/views/components/common/styled_dropdown.py
import flet as ft
from config import MAX_MENU_HEIGHT


class StyledDropdown(ft.Dropdown):
    def __init__(
        self,
        label: str | None = None,
        hint_text: str | None = None,
        leading_icon: str | None = None,
        options_list: list[tuple[int | str, str, str, str] | tuple[int | str, str]] | None = None,
        border_radius: int = 16,
        focused_color: str = ft.Colors.BLUE,
        max_menu_height: int = MAX_MENU_HEIGHT,
        expand: bool = True,
        dense: bool = True,
        content_padding: ft.Padding | None = ft.Padding.all(0),
        on_change=None,
        **kwargs,
    ):
        # Guarda los colores por defecto definidos externamente o por el tema
        self._default_fill_color = kwargs.get("fill_color")
        self._default_color = kwargs.get("color")

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

        custom_menu_style = ft.MenuStyle(
            shape=ft.RoundedRectangleBorder(radius=border_radius),
            padding=0,
        )

        self._user_on_select = on_change
        self._option_colors = {}  # Diccionario key -> {"bgcolor": ..., "color": ...}

        formatted_options = []
        if options_list:
            for opt in options_list:
                if not isinstance(opt, (tuple, list)):
                    continue

                text_color = None
                bg_color = None

                # Tupla de 4 elementos -> (key, text, color, bg_color)
                if len(opt) == 4:
                    key_val = str(opt[0])
                    text_val = str(opt[1])
                    text_color = opt[2]
                    bg_color = opt[3]

                # Tupla de 2 elementos -> (key, text)
                elif len(opt) == 2:
                    key_val = str(opt[0])
                    text_val = str(opt[1])

                else:
                    continue

                # Guarda los colores asociados a la clave
                self._option_colors[key_val] = {
                    "bgcolor": bg_color,
                    "color": text_color,
                }

                opt_style = None
                if text_color or bg_color:
                    opt_style = ft.ButtonStyle(
                        color=text_color,
                        bgcolor=bg_color,
                    )

                formatted_options.append(
                    ft.dropdown.Option(
                        key=key_val,
                        text=text_val,
                        style=opt_style,
                    )
                )

        initial_value = kwargs.get("value")
        if initial_value and initial_value in self._option_colors:
            colors = self._option_colors[initial_value]
            kwargs["fill_color"] = colors["bgcolor"] or self._default_fill_color
            kwargs["color"] = colors["color"] or self._default_color

        super().__init__(
            label=label,
            hint_text=hint_text,
            leading_icon=leading_icon,
            filled=True,
            expand=expand,
            dense=dense,
            border=custom_border,
            menu_style=custom_menu_style,
            options=formatted_options,
            menu_height=max_menu_height,
            on_select=self._internal_on_select,
            content_padding=content_padding,
            **kwargs,
        )

    @property
    def key(self):
        return self.value

    @key.setter
    def key(self, val):
        self.value = str(val) if val is not None else None

    def clean_data(self):
        self.value = None
        self.fill_color = self._default_fill_color
        self.color = self._default_color

    def _internal_on_select(self, e):
        colors = self._option_colors.get(self.value, {})
        self.fill_color = colors.get("bgcolor") or self._default_fill_color
        self.color = colors.get("color") or self._default_color
        self.update()

        if self._user_on_select:
            self._user_on_select(e)