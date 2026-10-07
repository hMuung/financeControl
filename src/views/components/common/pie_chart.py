# src/views/components/common/pie_chart.py
import flet as ft
from dataclasses import field
from typing import Any

import flet_charts as ftch


@ft.control
class BasePieChart(ft.Container):
    """
    Acepta una lista de diccionarios con el formato:
    [
        {"nombre": "Comida", "porcentaje": 45, "color": "#9D4EDD"},
        {"nombre": "Transporte", "porcentaje": 55, "color": "#C77DFF"},
    ]
    """

    data: dict[str, dict[str, Any]] = field(default_factory=dict)
    section_radius: int = 45
    center_radius: int = 10
    section_spacing: int = 3
    show_percentages: bool = False
    percentage_size: int = 12
    percentage_color: ft.Colors = ft.Colors.WHITE
    percentage_weight: ft.FontWeight = ft.FontWeight.BOLD

    def init(self):
        # Calculo del tamaño del contenedor
        total_radius = self.center_radius + self.section_radius
        exact_size = total_radius * 2

        self.width = exact_size
        self.height = exact_size
        self.padding = 0
        self.border_radius = 0
        self.bgcolor = ft.Colors.TRANSPARENT
        self.alignment = ft.Alignment.CENTER

        sections = [
            ftch.PieChartSection(
                value=100,
                color="#9D4EDD",
                radius=self.section_radius,
            )
        ]

        if self.data:
            sections = list()

            sections = [
                ftch.PieChartSection(
                    value=item.get("porcentaje", 0),
                    color=item.get("color", "#9D4EDD"),
                    radius=self.section_radius,
                    title_style=ft.TextStyle(
                        size=self.percentage_size,
                        color=self.percentage_color,
                        weight=self.percentage_weight
                    ),
                    title= f"{item.get("porcentaje", 0):.2f}%" if self.show_percentages else "", 
                )
                for item in self.data
            ]
        self.content = ftch.PieChart(
            sections=sections,
            sections_space=self.section_spacing,
            center_space_radius=self.center_radius,
            expand=True,
        )