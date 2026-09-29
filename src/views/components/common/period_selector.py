# src/views/components/common/period_selector.py
import flet as ft
from datetime import date
import calendar
import time
from typing import Any

MONTH_NAMES_SHORT = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
MONTH_NAMES_FULL = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

@ft.control
class PeriodSelector(ft.Container):
    on_change: Any = None
    min_year: int | None = None
    max_year: int | None = None
    allow_all: bool = True

    def init(self):
        self.mode: str = "ALL" if self.allow_all else "DAYS"

        today = date.today()
        if self.max_year is None:
            self.max_year = today.year

        if self.min_year and today.year < self.min_year:
            start_date_val = date(self.min_year, 1, 1)
            start_month_val = (self.min_year, 1)
            start_year_val = self.min_year
        elif self.max_year and today.year > self.max_year:
            start_date_val = date(self.max_year, 12, 31)
            start_month_val = (self.max_year, 12)
            start_year_val = self.max_year
        else:
            start_date_val = today
            start_month_val = (today.year, today.month)
            start_year_val = today.year

        self.start_date: date | None = start_date_val
        self.end_date: date | None = None

        self.start_month: tuple[int, int] | None = start_month_val
        self.end_month: tuple[int, int] | None = None

        self.start_year: int | None = start_year_val
        self.end_year: int | None = None

        self.view_year: int = start_year_val
        self.view_month: int = start_month_val[1]
        self.year_page_start: int = (start_year_val // 12) * 12

        self._last_click_time: float = 0
        self._last_click_target: Any = None

        self.period_text = ft.Text("Seleccionar periodo", size=16, weight=ft.FontWeight.BOLD)

        #self.border = ft.Border.all(1.5, ft.Colors.OUTLINE)
        self.border_radius = ft.BorderRadius.all(16)
        self.padding = ft.Padding.symmetric(horizontal=12, vertical=10)
        self.bgcolor = ft.Colors.WHITE
        self.ink = True
        self.on_click = self._open_picker_dialog

        self.content = ft.Row(
            controls=[
                ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.PRIMARY),
                self.period_text,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.GREY_700),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.dialog = None
        self._update_trigger_label()

    def get_date_range(self) -> tuple[Any, Any]:
        if self.mode == "ALL":
            return "all", "all"

        if self.mode == "DAYS":
            if not self.start_date:
                return None, None
            end = self.end_date or self.start_date
            return min(self.start_date, end), max(self.start_date, end)

        elif self.mode == "MONTHS":
            if not self.start_month:
                return None, None
            end = self.end_month or self.start_month
            s_m = min(self.start_month, end)
            e_m = max(self.start_month, end)

            start_date_res = date(s_m[0], s_m[1], 1)
            last_day_of_month = calendar.monthrange(e_m[0], e_m[1])[1]
            end_date_res = date(e_m[0], e_m[1], last_day_of_month)

            return start_date_res, end_date_res

        elif self.mode == "YEARS":
            if not self.start_year:
                return None, None
            end = self.end_year or self.start_year
            s_y = min(self.start_year, end)
            e_y = max(self.start_year, end)

            start_date_res = date(s_y, 1, 1)
            end_date_res = date(e_y, 12, 31)

            return start_date_res, end_date_res

        return None, None

    def get_value(self) -> dict:
        start_d, end_d = self.get_date_range()
        return {
            "mode": self.mode,
            "start_date": start_d,
            "end_date": end_d,
            "formatted": self.get_formatted_value(),
        }

    def _update_trigger_label(self):
        self.period_text.value = self.get_formatted_value()

    def get_formatted_value(self) -> str:
        if self.mode == "ALL":
            return "Todo"

        start_d, end_d = self.get_date_range()
        if not start_d or not end_d:
            return "Sin seleccion"

        if self.mode == "DAYS":
            if start_d == end_d:
                return start_d.strftime("%d/%m/%Y")
            return f"{start_d.strftime('%d/%m/%Y')} - {end_d.strftime('%d/%m/%Y')}"

        elif self.mode == "MONTHS":
            s_str = f"{MONTH_NAMES_SHORT[start_d.month-1]} {start_d.year}"
            e_str = f"{MONTH_NAMES_SHORT[end_d.month-1]} {end_d.year}"
            if start_d.month == end_d.month and start_d.year == end_d.year:
                return s_str
            return f"{s_str} - {e_str}"

        elif self.mode == "YEARS":
            if start_d.year == end_d.year:
                return str(start_d.year)
            return f"{start_d.year} - {end_d.year}"

        return "Sin seleccion"

    def _open_picker_dialog(self, e=None):
        self._build_dialog()
        if self.page:
            self.page.show_dialog(self.dialog)

    def _close_dialog(self, e=None):
        if self.page:
            self.page.pop_dialog()

    def _apply_selection(self, e=None):
        self._update_trigger_label()
        self._close_dialog()
        self.page.update(self)
        if self.on_change:
            self.on_change(self.get_value())

    def _select_all_period(self, e=None):
        self.mode = "ALL"
        self._apply_selection()

    def _build_dialog(self):
        self.grid_container = ft.Column(spacing=8, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
        self.header_title = ft.Text("", weight=ft.FontWeight.BOLD, size=14)
        
        self.header_title_button = ft.TextButton(
            content=self.header_title, 
            on_click=self._on_header_title_click
        )

        self._render_current_view()

        # Construccion dinamica de las acciones del dialogo segun allow_all
        action_controls = []
        if self.allow_all:
            action_controls.append(ft.TextButton(content=ft.Text("Todo"), on_click=self._select_all_period))
            actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        else:
            actions_alignment = ft.MainAxisAlignment.END

        right_buttons = ft.Row(
            [
                ft.TextButton(content=ft.Text("Cancelar"), on_click=self._close_dialog),
                ft.Button(content=ft.Text("Aplicar"), on_click=self._apply_selection),
            ],
            spacing=4,
        )
        action_controls.append(right_buttons)

        self.dialog = ft.AlertDialog(
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            title=ft.Text("Seleccionar Periodo", size=16, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.IconButton(icon=ft.Icons.CHEVRON_LEFT, on_click=self._nav_prev),
                                self.header_title_button,
                                ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT, on_click=self._nav_next),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Divider(height=1),
                        self.grid_container,
                    ],
                    tight=True,
                ),
                width=310,
            ),
            actions=[
                ft.Row(
                    action_controls,
                    alignment=actions_alignment,
                )
            ],
        )

    def _on_header_title_click(self, e=None):
        if self.mode in ("DAYS", "ALL"):
            self.mode = "MONTHS"
        elif self.mode == "MONTHS":
            self.mode = "YEARS"
        elif self.mode == "YEARS":
            self.mode = "DAYS"
        self._render_current_view()

    def _nav_prev(self, e=None):
        if self.mode in ("DAYS", "ALL"):
            if self.min_year and self.view_year == self.min_year and self.view_month == 1:
                return
            if self.view_month == 1:
                self.view_month = 12
                self.view_year -= 1
            else:
                self.view_month -= 1
        elif self.mode == "MONTHS":
            if self.min_year and self.view_year <= self.min_year:
                return
            self.view_year -= 1
        elif self.mode == "YEARS":
            if self.min_year and (self.year_page_start - 12) < (self.min_year // 12) * 12:
                return
            self.year_page_start -= 12
        self._render_current_view()

    def _nav_next(self, e=None):
        if self.mode in ("DAYS", "ALL"):
            if self.max_year and self.view_year == self.max_year and self.view_month == 12:
                return
            if self.view_month == 12:
                self.view_month = 1
                self.view_year += 1
            else:
                self.view_month += 1
        elif self.mode == "MONTHS":
            if self.max_year and self.view_year >= self.max_year:
                return
            self.view_year += 1
        elif self.mode == "YEARS":
            if self.max_year and (self.year_page_start + 12) > self.max_year:
                return
            self.year_page_start += 12
        self._render_current_view()

    def _render_current_view(self):
        if self.mode == "MONTHS":
            self._render_months_view()
        elif self.mode == "YEARS":
            self._render_years_view()
        else:
            self._render_days_view()

    def _render_days_view(self):
        today = date.today()
        self.header_title.value = f"{MONTH_NAMES_FULL[self.view_month - 1]} {self.view_year}"

        week_days = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"]
        header_row = ft.Row(
            [
                ft.Container(
                    content=ft.Text(day, weight=ft.FontWeight.BOLD, size=11), 
                    expand=True, 
                    alignment=ft.Alignment.CENTER
                ) for day in week_days
            ],
            spacing=2,
        )

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdatescalendar(self.view_year, self.view_month)

        day_rows = []
        for week in month_days:
            controls_row = []
            for d in week:
                is_disabled = (
                    (self.min_year is not None and d.year < self.min_year) or
                    (self.max_year is not None and d.year > self.max_year)
                )
                is_current_month = d.month == self.view_month
                is_today = (d == today)
                is_selected = False
                is_in_range = False

                if not is_disabled and self.mode == "DAYS":
                    end = self.end_date or self.start_date
                    if self.start_date and end:
                        start_clean = min(self.start_date, end)
                        end_clean = max(self.start_date, end)
                        if d == start_clean or d == end_clean:
                            is_selected = True
                        elif start_clean < d < end_clean:
                            is_in_range = True

                border = None
                font_weight = ft.FontWeight.NORMAL

                if is_disabled:
                    bg_color = None
                    text_color = ft.Colors.GREY_300
                    click_handler = None
                else:
                    click_handler = lambda e, curr_d=d: self._select_day(curr_d)

                    if is_selected:
                        bg_color = ft.Colors.PRIMARY
                        text_color = ft.Colors.WHITE
                        font_weight = ft.FontWeight.BOLD
                    elif is_in_range:
                        bg_color = ft.Colors.PRIMARY_CONTAINER
                        text_color = ft.Colors.ON_PRIMARY_CONTAINER
                    else:
                        bg_color = None
                        text_color = ft.Colors.ON_SURFACE if is_current_month else ft.Colors.GREY_400

                    if is_today:
                        border_color = ft.Colors.WHITE if is_selected else ft.Colors.PRIMARY
                        border = ft.Border.all(1.5, border_color)
                        font_weight = ft.FontWeight.BOLD
                        if not is_selected:
                            text_color = ft.Colors.PRIMARY

                btn = ft.Container(
                    content=ft.Text(str(d.day), color=text_color, size=12, weight=font_weight),
                    expand=True,
                    height=34,
                    border=border,
                    border_radius=ft.BorderRadius.all(17),
                    bgcolor=bg_color,
                    alignment=ft.Alignment.CENTER,
                    ink=not is_disabled,
                    on_click=click_handler,
                )
                controls_row.append(btn)
            day_rows.append(ft.Row(controls_row, spacing=2))

        self.grid_container.controls = [header_row, ft.Column(day_rows, spacing=2)]

    def _select_day(self, selected_d):
        today = date.today()
        self.mode = "DAYS"
        self.start_month = (today.year, today.month)
        self.end_month = None
        self.start_year = today.year
        self.end_year = None

        if self.start_date is None or (self.start_date and self.end_date):
            self.start_date = selected_d
            self.end_date = None
        else:
            if selected_d < self.start_date:
                self.start_date = selected_d
                self.end_date = None
            else:
                self.end_date = selected_d
        self._render_days_view()

    def _render_months_view(self):
        today = date.today()
        self.header_title.value = f"Año {self.view_year}"

        rows = []
        for r in range(4):
            row_controls = []
            for c in range(3):
                m_idx = r * 3 + c + 1
                curr_month_val = (self.view_year, m_idx)
                is_disabled = (
                    (self.min_year is not None and self.view_year < self.min_year) or
                    (self.max_year is not None and self.view_year > self.max_year)
                )

                is_current_month = (curr_month_val == (today.year, today.month))
                is_selected = False
                is_in_range = False

                if not is_disabled and self.mode == "MONTHS":
                    end = self.end_month or self.start_month
                    if self.start_month and end:
                        s_clean = min(self.start_month, end)
                        e_clean = max(self.start_month, end)
                        if curr_month_val == s_clean or curr_month_val == e_clean:
                            is_selected = True
                        elif s_clean < curr_month_val < e_clean:
                            is_in_range = True

                border = None
                font_weight = ft.FontWeight.BOLD

                if is_disabled:
                    bg_color = None
                    text_color = ft.Colors.GREY_300
                    click_handler = None
                else:
                    click_handler = lambda e, m_val=curr_month_val: self._handle_month_click(m_val)

                    if is_selected:
                        bg_color = ft.Colors.PRIMARY
                        text_color = ft.Colors.WHITE
                    elif is_in_range:
                        bg_color = ft.Colors.PRIMARY_CONTAINER
                        text_color = ft.Colors.ON_PRIMARY_CONTAINER
                    else:
                        bg_color = None
                        text_color = ft.Colors.ON_SURFACE

                    if is_current_month:
                        border_color = ft.Colors.WHITE if is_selected else ft.Colors.PRIMARY
                        border = ft.Border.all(1.5, border_color)
                        if not is_selected:
                            text_color = ft.Colors.PRIMARY

                btn = ft.Container(
                    content=ft.Text(MONTH_NAMES_SHORT[m_idx - 1], color=text_color, weight=font_weight),
                    expand=True,
                    height=40,
                    border=border,
                    border_radius=ft.BorderRadius.all(8),
                    bgcolor=bg_color,
                    alignment=ft.Alignment.CENTER,
                    ink=not is_disabled,
                    on_click=click_handler,
                )
                row_controls.append(btn)
            rows.append(ft.Row(row_controls, spacing=6))

        self.grid_container.controls = [ft.Column(rows, spacing=6)]

    def _handle_month_click(self, m_val):
        now = time.time()
        if (now - self._last_click_time) < 0.35 and self._last_click_target == m_val:
            self._last_click_time = 0
            self._last_click_target = None
            self._drill_down_month(m_val)
        else:
            self._last_click_time = now
            self._last_click_target = m_val
            self._select_month(m_val)

    def _select_month(self, m_val):
        today = date.today()
        self.mode = "MONTHS"
        self.start_date = today
        self.end_date = None
        self.start_year = today.year
        self.end_year = None

        if self.start_month is None or (self.start_month and self.end_month):
            self.start_month = m_val
            self.end_month = None
        else:
            if m_val < self.start_month:
                self.start_month = m_val
                self.end_month = None
            else:
                self.end_month = m_val
        self._render_months_view()

    def _drill_down_month(self, m_val):
        today = date.today()
        self.start_month = (today.year, today.month)
        self.end_month = None
        self.start_year = today.year
        self.end_year = None
        self.start_date = today
        self.end_date = None

        self.view_year = m_val[0]
        self.view_month = m_val[1]
        self.mode = "DAYS"
        self._render_current_view()

    def _render_years_view(self):
        today = date.today()
        start_y = self.year_page_start
        end_page_y = start_y + 11
        self.header_title.value = f"{start_y} - {end_page_y}"

        rows = []
        for r in range(4):
            row_controls = []
            for c in range(3):
                y_val = start_y + (r * 3 + c)
                is_disabled = (
                    (self.min_year is not None and y_val < self.min_year) or
                    (self.max_year is not None and y_val > self.max_year)
                )

                is_current_year = (y_val == today.year)
                is_selected = False
                is_in_range = False

                if not is_disabled and self.mode == "YEARS":
                    end = self.end_year or self.start_year
                    if self.start_year and end:
                        s_clean = min(self.start_year, end)
                        e_clean = max(self.start_year, end)
                        if y_val == s_clean or y_val == e_clean:
                            is_selected = True
                        elif s_clean < y_val < e_clean:
                            is_in_range = True

                border = None
                font_weight = ft.FontWeight.BOLD

                if is_disabled:
                    bg_color = None
                    text_color = ft.Colors.GREY_300
                    click_handler = None
                else:
                    click_handler = lambda e, y=y_val: self._handle_year_click(y)

                    if is_selected:
                        bg_color = ft.Colors.PRIMARY
                        text_color = ft.Colors.WHITE
                    elif is_in_range:
                        bg_color = ft.Colors.PRIMARY_CONTAINER
                        text_color = ft.Colors.ON_PRIMARY_CONTAINER
                    else:
                        bg_color = None
                        text_color = ft.Colors.ON_SURFACE

                    if is_current_year:
                        border_color = ft.Colors.WHITE if is_selected else ft.Colors.PRIMARY
                        border = ft.Border.all(1.5, border_color)
                        if not is_selected:
                            text_color = ft.Colors.PRIMARY

                btn = ft.Container(
                    content=ft.Text(str(y_val), color=text_color, weight=font_weight),
                    expand=True,
                    height=40,
                    border=border,
                    border_radius=ft.BorderRadius.all(8),
                    bgcolor=bg_color,
                    alignment=ft.Alignment.CENTER,
                    ink=not is_disabled,
                    on_click=click_handler,
                )
                row_controls.append(btn)
            rows.append(ft.Row(row_controls, spacing=6))

        self.grid_container.controls = [ft.Column(rows, spacing=6)]

    def _handle_year_click(self, y_val):
        now = time.time()
        if (now - self._last_click_time) < 0.35 and self._last_click_target == y_val:
            self._last_click_time = 0
            self._last_click_target = None
            self._drill_down_year(y_val)
        else:
            self._last_click_time = now
            self._last_click_target = y_val
            self._select_year(y_val)

    def _select_year(self, y_val):
        today = date.today()
        self.mode = "YEARS"
        self.start_date = today
        self.end_date = None
        self.start_month = (today.year, today.month)
        self.end_month = None

        if self.start_year is None or (self.start_year and self.end_year):
            self.start_year = y_val
            self.end_year = None
        else:
            if y_val < self.start_year:
                self.start_year = y_val
                self.end_year = None
            else:
                self.end_year = y_val
        self._render_years_view()

    def _drill_down_year(self, y_val):
        today = date.today()
        self.start_year = today.year
        self.end_year = None
        self.start_month = (today.year, today.month)
        self.end_month = None
        self.start_date = today
        self.end_date = None

        self.view_year = y_val
        self.mode = "MONTHS"
        self._render_current_view()