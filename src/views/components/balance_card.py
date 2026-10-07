# src/views/components/balance_card.py
# src/views/components/balance_card.py
import flet as ft

from src.views.components.common.pie_chart import BasePieChart
from src.views.utils.theme import (
    EXPENSE_COLOR, 
    INCOME_COLOR,
    GRADIENT_GLASS_CARD,
    GLASS_CARD_SHADOW,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ALERT_COLOR
) 


@ft.control
class BalanceCard(ft.Container):
    ingresos: float = 0.0
    egresos: float = 0.0
    punto_alerta: float = 1000
    title: str = "Resumen del Mes"
    currency_symbol: str = "$"
    title_size: int = 18
    amount_size: int = 14
    balance_text_size: int = 18
    section_radius: int = 45
    center_radius: int = 15
    section_spacing: int = 2
    legend_color_size: int = 12
    percentage_size: int = 8

    def init(self):
        # Calculo de porcentajes y balance
        total = self.ingresos + self.egresos
        pct_ingreso = (self.ingresos / total * 100) if total > 0 else 0.0
        pct_egreso = (self.egresos / total * 100) if total > 0 else 0.0
        balance = self.ingresos - self.egresos

        # Datos para la grafica
        chart_data = [
            {"nombre": "Ingresos", "porcentaje": pct_ingreso, "color": INCOME_COLOR},
            {"nombre": "Egresos", "porcentaje": pct_egreso, "color": EXPENSE_COLOR},
        ]

        # Estilos del Contenedor Principal
        self.gradient = GRADIENT_GLASS_CARD
        self.shadow = GLASS_CARD_SHADOW
        self.border_radius = 20
        self.padding = ft.Padding.all(18)
        self.border = ft.Border.all(1, color="#33FFFFFF")

        # Estructura Visual de la Tarjeta
        self.content = ft.Column(
            spacing=12,
            tight=True,
            controls=[
                # Titulo de la tarjeta
                ft.Text(
                    value=self.title,
                    size=self.title_size,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),
                # Bloque principal
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        # Grafica a la izquierda
                        BasePieChart(
                            data=chart_data,
                            section_radius=self.section_radius,
                            center_radius=self.center_radius,
                            section_spacing=self.section_spacing,
                            show_percentages=True,
                        ),
                        # Columna Derecha: Leyendas + Balance
                        ft.Column(
                            spacing=8,
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                self._build_legend_item(
                                    label="Ingreso",
                                    amount=self.ingresos,
                                    color=INCOME_COLOR,
                                ),
                                self._build_legend_item(
                                    label="Egreso",
                                    amount=self.egresos,
                                    color=EXPENSE_COLOR,
                                ),
                                ft.Container(height=2, bgcolor="#50FFFFFF"),
                                self._build_balance_item(balance=balance),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def _build_legend_item(
        self, label: str, amount: float, color: str
    ) -> ft.Control:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                # Izquierda: Dot de color + Nombre del rubro
                ft.Row(
                    spacing=6,
                    tight=True,
                    controls=[
                        ft.Container(
                            width=self.legend_color_size,
                            height=self.legend_color_size,
                            border_radius=self.legend_color_size // 2,
                            bgcolor=color,
                        ),
                        ft.Text(
                            value=label,
                            size=self.amount_size,
                            color=TEXT_PRIMARY,
                            weight=ft.FontWeight.W_500,
                        ),
                    ],
                ),
                # Derecha: Cantidad
                ft.Text(
                    value=f"{self.currency_symbol}{amount:,.2f}",
                    size=self.amount_size,
                    color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
        )

    def _build_balance_item(self, balance: float) -> ft.Control:
        color = INCOME_COLOR if balance > self.punto_alerta else ALERT_COLOR
        color = EXPENSE_COLOR if balance < 0 else color
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    value="Balance",
                    size=self.amount_size,
                    weight=ft.FontWeight.W_500,
                    color=TEXT_SECONDARY,
                ),
                ft.Text(
                    value=f"{self.currency_symbol}{balance:,.2f}",
                    size=self.balance_text_size,
                    weight=ft.FontWeight.BOLD,
                    color=color,
                ),
            ],
        )