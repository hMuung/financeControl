import flet as ft


class StyledDropdown(ft.Dropdown):
    def __init__(
        self,
        label: str | None = None,
        hint_text: str | None = None,
        leading_icon: str | None = None,
        options_list: list[str | tuple[str, str, str] | tuple[str, str] | dict | ft.dropdown.Option] | None = None,
        border_radius: int = 16,
        focused_color: str = ft.Colors.BLUE,
        expand: bool = True,
        dense: bool = True,
        on_change=None,
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

        custom_menu_style = ft.MenuStyle(
            shape=ft.RoundedRectangleBorder(radius=border_radius),
            padding=0,
        )

        self._user_on_select = on_change
        self._option_colors = {}  # Diccionario key -> {"bgcolor": ..., "color": ...}

        formatted_options = []
        if options_list:
            for opt in options_list:
                if isinstance(opt, ft.dropdown.Option):
                    formatted_options.append(opt)
                    continue

                text_val = ""
                key_val = ""
                text_color = None
                bg_color = None

                # Formato Tupla/Lista: ("Texto", "color_texto", "color_fondo")
                if isinstance(opt, (tuple, list)):
                    text_val = key_val = opt[0]
                    text_color = opt[1] if len(opt) > 1 else None
                    bg_color = opt[2] if len(opt) > 2 else None

                # Formato Diccionario
                elif isinstance(opt, dict):
                    text_val = opt.get("text", opt.get("key", ""))
                    key_val = opt.get("key", text_val)
                    text_color = opt.get("color", opt.get("text_color"))
                    bg_color = opt.get("bgcolor", opt.get("bg_color"))

                # Formato String simple
                elif isinstance(opt, str):
                    text_val = key_val = opt

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

        # Asigna el color de fondo/texto previo a construir
        initial_value = kwargs.get("value")
        if initial_value and initial_value in self._option_colors:
            colors = self._option_colors[initial_value]
            if colors["bgcolor"]:
                kwargs["fill_color"] = colors["bgcolor"]
            if colors["color"]:
                kwargs["color"] = colors["color"]

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
            on_select=self._internal_on_select,
            **kwargs,
        )

    def clean_data(self):
        self.value = None
        self.fill_color = None
        self.color = None

    def _internal_on_select(self, e):
        # Actualiza dinamicamente fill_color
        if self.value in self._option_colors:
            colors = self._option_colors[self.value]
            if colors["bgcolor"]:
                self.fill_color = colors["bgcolor"]
            if colors["color"]:
                self.color = colors["color"]
            self.update()

        # Ejecuta la callback original si se declaro
        if self._user_on_select:
            self._user_on_select(e)