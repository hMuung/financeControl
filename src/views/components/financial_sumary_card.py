import flet as ft
import flet_charts as ftch

from controllers.expense_controller import ExpenseController
from controllers.income_controller import IncomeController
from views.components.common.glass_card import GlassCard
from views.utils.theme import HEADER_TEXT_COLOR

# Mapeo estatico global de colores
COLOR_MAP = {
    ft.Colors.TEAL_400: "#26a69a",
    ft.Colors.PINK_400: "#ec407a",
    ft.Colors.GREEN_700: "#388e3c",
    ft.Colors.RED_700: "#d32f2f",
    ft.Colors.AMBER_700: "#ffa000",
}

# Mapeo de periodo DB -> (Titulo UI, Icono)
PERIOD_CONFIG = {
    "today": ("Por Hoy", ft.Icons.TODAY),
    "week": ("Esta Semana", ft.Icons.DATE_RANGE),
    "month": ("Este Mes", ft.Icons.CALENDAR_MONTH),
    "year": ("Este Año", ft.Icons.CALENDAR_TODAY),
    "all_time": ("Histórico", ft.Icons.HISTORY),
}


class FinancialSummaryCard(GlassCard):

    def __init__(
        self,
        period: str = "month",
        setpoint_low: float = 0.0,
        setpoint_high: float = 1000.0,
        center_space_radius: int = 20,
        section_radius: int = 70,
        section_spacing: int = 3,
        income_color: str = ft.Colors.TEAL_400,
        expense_color: str = ft.Colors.PINK_400,
    ):
        self.period = period
        self.setpoint_low = setpoint_low
        self.setpoint_high = setpoint_high
        self.center_space_radius = center_space_radius
        self.section_radius = section_radius
        self.section_spacing = section_spacing
        self.income_color = income_color
        self.expense_color = expense_color

        self.income_ctrl = IncomeController()
        self.expense_ctrl = ExpenseController()

        # Cacheo de valores anteriores para el mecanismo de diffing
        self.total_ingresos = -1.0
        self.total_egresos = -1.0

        # Pre-procesar colores base a tuplas RGB una sola vez
        self._income_rgb = self._parse_rgb(self.income_color)
        self._expense_rgb = self._parse_rgb(self.expense_color)

        # Construir estructura estatica de la interfaz
        self._build_static_ui()

        # Layout principal en columna para la cabecera + grafico/leyenda
        content = ft.Column(
            controls=[
                self.header,
                ft.Divider(HEADER_TEXT_COLOR,1),
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        self.chart_container,
                        self.legend_col,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
            tight=True,
        )

        super().__init__(
            content=content, 
            padding=ft.Padding.only(left=20,right=20,top=10,bottom=20), 
            alignment=ft.Alignment.CENTER
        )

    def did_mount(self):
        self._load_data_from_controllers()

    def _parse_rgb(self, color_str: str) -> tuple[int, int, int]:
        c_str = COLOR_MAP.get(color_str, color_str).lstrip("#")
        if len(c_str) == 6:
            return tuple(int(c_str[i : i + 2], 16) for i in (0, 2, 4))
        elif len(c_str) == 8:
            return tuple(int(c_str[i : i + 2], 16) for i in (2, 4, 6))
        return (128, 128, 128)

    def _build_static_ui(self):
        initial_title, initial_icon = PERIOD_CONFIG.get(
            self.period, PERIOD_CONFIG["month"]
        )

        self.icon_period = ft.Icon(initial_icon, size=20, color=HEADER_TEXT_COLOR)
        self.txt_title = ft.Text(initial_title, size=18, weight=ft.FontWeight.BOLD, color=HEADER_TEXT_COLOR)

        self.header_row = ft.Row(
            controls=[
                self.icon_period,
                self.txt_title,
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.header = ft.Container(
            content=self.header_row,
            width=float("inf"),
            on_click=self._toggle_period
        )

        chart_diameter = (self.center_space_radius + self.section_radius) * 2

        self.sec_ingresos = ftch.PieChartSection(
            value=1,
            color=self.income_color,
            title="0.00%",
            title_style=ft.TextStyle(size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            radius=self.section_radius,
        )
        self.sec_egresos = ftch.PieChartSection(
            value=1,
            color=self.expense_color,
            title="0.00%",
            title_style=ft.TextStyle(size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            radius=self.section_radius,
        )

        self.chart = ftch.PieChart(
            sections=[self.sec_ingresos, self.sec_egresos],
            sections_space=self.section_spacing,
            center_space_radius=self.center_space_radius,
            width=chart_diameter,
            height=chart_diameter,
        )

        self._shadow_glow_1 = ft.BoxShadow(spread_radius=8, blur_radius=15, offset=ft.Offset(0, 0))
        self._shadow_glow_2 = ft.BoxShadow(spread_radius=15, blur_radius=35, offset=ft.Offset(0, 0))

        self.chart_container = ft.Container(
            content=self.chart,
            shape=ft.BoxShape.CIRCLE,
            shadow=[self._shadow_glow_1, self._shadow_glow_2],
        )

        self.txt_ingresos = ft.Text("$0.00", size=16, color=ft.Colors.BLACK_87, weight=ft.FontWeight.BOLD)
        self.txt_egresos = ft.Text("$0.00", size=16, color=ft.Colors.BLACK_87, weight=ft.FontWeight.BOLD)
        self.txt_balance = ft.Text("$0.00", size=18, color=ft.Colors.AMBER_700, weight=ft.FontWeight.BOLD)

        self.legend_col = ft.Column(
            controls=[
                self._build_legend_row("Ingresos", self.txt_ingresos, self.income_color),
                self._build_legend_row("Egresos", self.txt_egresos, self.expense_color),
                ft.Container(height=2),
                ft.Column(
                    controls=[
                        ft.Text("Balance Total", size=14, color=ft.Colors.BLACK_54, weight=ft.FontWeight.W_600),
                        self.txt_balance,
                    ],
                    spacing=0,
                ),
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def _update_header_ui(self):
        title, icon_name = PERIOD_CONFIG.get(self.period, PERIOD_CONFIG["month"])
        self.txt_title.value = title
        self.icon_period.name = icon_name

    def set_period(self, new_period: str):
        if self.period != new_period and new_period in PERIOD_CONFIG:
            self.period = new_period
            self._update_header_ui()
            self.refresh()
            if self.page:
                self.update()

    def _build_legend_row(self, title: str, text_control: ft.Text, color: str) -> ft.Control:
        return ft.Row(
            controls=[
                ft.Container(width=10, height=10, border_radius=5, bgcolor=color),
                ft.Column(
                    controls=[
                        ft.Text(title, size=13, color=ft.Colors.BLACK_54, weight=ft.FontWeight.W_500),
                        text_control,
                    ],
                    spacing=0,
                ),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _load_data_from_controllers(self):
        inc_totals = self.income_ctrl.get_totals()
        exp_totals = self.expense_ctrl.get_totals()

        ingresos = inc_totals.get(self.period, {}).get("total", 0.0)
        egresos = exp_totals.get(self.period, {}).get("total", 0.0)

        self.update_data(ingresos, egresos)

    def _toggle_period(self, e=None):
        periods = list(PERIOD_CONFIG.keys())
        if self.period in periods:
            current_idx = periods.index(self.period)
            next_idx = (current_idx + 1) % len(periods)
            self.set_period(periods[next_idx])

    def refresh(self):
        self._load_data_from_controllers()

    def _blend_colors(self, ratio: float) -> str:
        r1, g1, b1 = self._income_rgb
        r2, g2, b2 = self._expense_rgb

        r = int(r1 * ratio + r2 * (1.0 - ratio))
        g = int(g1 * ratio + g2 * (1.0 - ratio))
        b = int(b1 * ratio + b2 * (1.0 - ratio))

        return f"#{r:02x}{g:02x}{b:02x}"

    def update_data(self, total_ingresos: float, total_egresos: float):
        new_ingresos = max(0.0, total_ingresos)
        new_egresos = max(0.0, total_egresos)

        # Diffing Check:
        if new_ingresos == self.total_ingresos and new_egresos == self.total_egresos:
            return

        self.total_ingresos = new_ingresos
        self.total_egresos = new_egresos
        total = self.total_ingresos + self.total_egresos

        if total > 0:
            pct_ingresos = (self.total_ingresos / total) * 100
            pct_egresos = (self.total_egresos / total) * 100
            income_ratio = self.total_ingresos / total
        else:
            pct_ingresos = 0.0
            pct_egresos = 0.0
            income_ratio = 0.5

        # Actualizar propiedades del grafico
        self.sec_ingresos.value = self.total_ingresos if total > 0 else 1
        self.sec_ingresos.title = f"{pct_ingresos:.2f}%"

        self.sec_egresos.value = self.total_egresos if total > 0 else 1
        self.sec_egresos.title = f"{pct_egresos:.2f}%"

        # Mezcla de color utilizando tuplas pre-calculadas
        blended_glow_color = self._blend_colors(income_ratio)

        self._shadow_glow_1.color = ft.Colors.with_opacity(0.9, blended_glow_color)
        self._shadow_glow_2.color = ft.Colors.with_opacity(0.6, blended_glow_color)

        balance = self.total_ingresos - self.total_egresos

        if balance > self.setpoint_high:
            balance_color = ft.Colors.GREEN_700
        elif balance < self.setpoint_low:
            balance_color = ft.Colors.RED_700
        else:
            balance_color = ft.Colors.AMBER_700

        # Actualizar controles de texto
        self.txt_ingresos.value = f"${self.total_ingresos:,.2f}"
        self.txt_egresos.value = f"${self.total_egresos:,.2f}"
        self.txt_balance.value = f"${balance:,.2f}"
        self.txt_balance.color = balance_color