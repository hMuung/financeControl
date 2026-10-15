# src/views/components/common/base_dropdown.py
import flet as ft
from dataclasses import field

from src.views.utils.theme import (
    COLOR_ACCENT_BRIGHT,
    COLOR_BG_MAIN,
    TEXT_MUTED,
    TEXT_PRIMARY,
)

_OptionTuple = (
    tuple[str | int, str, str, str, str | None]
    | tuple[str | int, str, str, str]
    | tuple[str, str, str, str | None]
    | tuple[str, str, str]
    | tuple[str | int, str]
)


@ft.control
class BaseDropdown(ft.Dropdown):
    options_dict: dict[str, list[_OptionTuple] | tuple[_OptionTuple, ...]] = field(
        default_factory=dict
    )
    options_list: list[_OptionTuple] | tuple[_OptionTuple, ...] = field(
        default_factory=tuple
    )
    label: str | None = None
    hint_text: str | None = None
    default_key: str | None = None
    leading_icon: str | None = None
    default_fill_color: str = COLOR_BG_MAIN
    default_color: str = TEXT_PRIMARY
    border_radius: float = 16
    focused_color: str = COLOR_ACCENT_BRIGHT
    max_menu_height: float = 150

    def init(self):
        self.expand = True
        self._options_by_key: dict[str, list[ft.dropdown.Option]] = {}
        self._colors_by_key: dict[str, dict[str, dict]] = {}
        self._option_colors: dict[str, dict] = {}

        if not self.label and self.hint_text:
            self.label = self.hint_text

        custom_border = {
            ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                border_radius=self.border_radius,
                side=ft.BorderSide(color="#FFFFFF", width=1),
            ),
            ft.ControlState.FOCUSED: ft.OutlineInputBorder(
                border_radius=self.border_radius,
                side=ft.BorderSide(color=self.focused_color, width=1.5),
            ),
        }

        custom_menu_style = ft.MenuStyle(
            shape=ft.RoundedRectangleBorder(radius=self.border_radius),
            padding=0,
        )

        self.filled = True
        self.dense = True
        self.content_padding = ft.Padding.symmetric(vertical=6, horizontal=12)
        self.border = custom_border
        self.menu_style = custom_menu_style
        self.menu_height = self.max_menu_height
        self.on_select = self._internal_on_select

        self.fill_color = self.default_fill_color
        self.color = self.default_color

        if self.label:
            self.label_style = ft.TextStyle(color=TEXT_MUTED, size=16)

        if self.options_dict:
            for key_name, opts in self.options_dict.items():
                formatted_opts, color_map = self._build_options(opts)
                self._options_by_key[key_name] = formatted_opts
                self._colors_by_key[key_name] = color_map

        if self.default_key and self.default_key in self._options_by_key:
            self.options = self._options_by_key[self.default_key]
            self._option_colors = self._colors_by_key[self.default_key]
        elif self.options_list:
            formatted_opts, color_map = self._build_options(self.options_list)
            self.options = formatted_opts
            self._option_colors = color_map
        elif self._options_by_key:
            first_key = next(iter(self._options_by_key))
            self.options = self._options_by_key[first_key]
            self._option_colors = self._colors_by_key[first_key]

        if self.value and self.value in self._option_colors:
            self._apply_option_style(self.value)

    def set_dropdown(self, label: str, key: str):
        self.label = label
        self.hint_text = label

        if key in self._options_by_key:
            self.options = self._options_by_key[key]
            self._option_colors = self._colors_by_key[key]

        self.clean_data()

    def _build_options(
        self, options_list: list[_OptionTuple] | tuple[_OptionTuple, ...]
    ) -> tuple[list[ft.dropdown.Option], dict[str, dict]]:
        option_colors = {}
        formatted_options = []

        if options_list:
            for opt in options_list:
                if not isinstance(opt, (tuple, list)):
                    continue

                key_val = ""
                text_val = ""
                text_color = self.default_color
                bg_color = self.default_fill_color
                icon_val = None

                if len(opt) == 5:
                    key_val, text_val, text_color, bg_color, icon_val = (
                        str(opt[0]),
                        str(opt[1]),
                        opt[2],
                        opt[3],
                        opt[4],
                    )
                elif len(opt) == 4:
                    is_color = isinstance(opt[1], str) and (
                        opt[1].startswith("#") or "COLOR" in opt[1].upper()
                    )
                    if is_color:
                        key_val, text_val, text_color, bg_color, icon_val = (
                            str(opt[0]),
                            str(opt[0]),
                            opt[1],
                            opt[2],
                            opt[3],
                        )
                    else:
                        key_val, text_val, text_color, bg_color = (
                            str(opt[0]),
                            str(opt[1]),
                            opt[2],
                            opt[3],
                        )
                elif len(opt) == 3:
                    key_val, text_val, text_color, bg_color = (
                        str(opt[0]),
                        str(opt[0]),
                        opt[1],
                        opt[2],
                    )
                elif len(opt) == 2:
                    key_val, text_val = str(opt[0]), str(opt[1])
                else:
                    continue

                option_colors[key_val] = {
                    "bgcolor": bg_color,
                    "color": text_color,
                    "icon": icon_val,
                }

                opt_style = ft.ButtonStyle(
                    color=text_color,
                    bgcolor=bg_color,
                )

                row_controls = []
                if icon_val:
                    row_controls.append(
                        ft.Icon(icon=icon_val, color=text_color, size=18)
                    )
                row_controls.append(
                    ft.Text(value=text_val, color=text_color, size=13)
                )

                opt_content = ft.Row(
                    controls=row_controls,
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )

                formatted_options.append(
                    ft.dropdown.Option(
                        key=key_val,
                        text=text_val,
                        style=opt_style,
                        content=opt_content,
                    )
                )

        return formatted_options, option_colors

    def _apply_option_style(self, key_val: str):
        colors = self._option_colors.get(key_val, {})
        if colors:
            text_color = colors.get("color") or self.default_color
            bg_color = colors.get("bgcolor") or self.default_fill_color
            icon_val = colors.get("icon")

            self.fill_color = bg_color
            self.color = text_color
            self.leading_icon = icon_val

            if self.label:
                self.label_style = ft.TextStyle(color=text_color, size=16)

            if self.page:
                self.page.update(self)

    @property
    def key(self):
        return self.value

    @key.setter
    def key(self, val):
        self.value = str(val) if val is not None else None

    def clean_data(self):
        self.value = None
        self.fill_color = self.default_fill_color
        self.color = self.default_color
        self.leading_icon = None
        if self.label:
            self.label_style = ft.TextStyle(color=TEXT_MUTED, size=16)
        if self.page:
            self.page.update(self)

    def _internal_on_select(self, e):
        if self.value in self._option_colors:
            self._apply_option_style(self.value)