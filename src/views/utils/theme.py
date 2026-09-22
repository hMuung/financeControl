# src/views/components/utils/theme.py
import flet as ft

BACKGROUND_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment(-1, -1),
    end=ft.Alignment(1, 1),
    colors=["#75E2CD", "#B69CDA", "#EC99BD"],
    stops=[0.0, 0.5, 1.0],
)

BUTTON_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment(-1, 0),
    end=ft.Alignment(1, 0),
    colors=["#FFA07A", "#FF7F50"],
)

# Valores para el efecto Cristal / Espejo
GLASS_BG_COLOR = ft.Colors.with_opacity(0.4, ft.Colors.WHITE)
GLASS_BORDER_COLOR = ft.Colors.with_opacity(0.6, ft.Colors.WHITE)
GLASS_BORDER_RADIUS = 20

# Transparencia e iconos inactivos
INACTIVE_ICON_COLOR = ft.Colors.with_opacity(0.7, "#3D2A54")
TRANSPARENT_GRADIENT = ft.LinearGradient(
    colors=[ft.Colors.TRANSPARENT, ft.Colors.TRANSPARENT]
)