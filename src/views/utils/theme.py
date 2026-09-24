# src/views/utils/theme.py
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

CANCEL_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment(-1, 0),
    end=ft.Alignment(1, 0),
    colors=["#B91515", "#FB3838"],
)

ACCEPT_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment(-1, 0),
    end=ft.Alignment(1, 0),
    colors=["#37A93E", "#58DB88"],
)

MODAL_SHADOW = ft.BoxShadow(
    blur_radius=30,
    color=ft.Colors.BLACK_45,
    offset=ft.Offset(0, 10),
)

# Valores del header
HEADER_TEXT_COLOR = "#2D3748"

# Valores para el efecto Cristal / Espejo
GLASS_BG_COLOR = ft.Colors.with_opacity(0.4, ft.Colors.WHITE)
GLASS_BORDER_COLOR = ft.Colors.with_opacity(0.6, ft.Colors.WHITE)
GLASS_BORDER_RADIUS = 20

# Transparencia e iconos inactivos
INACTIVE_ICON_COLOR = ft.Colors.with_opacity(0.7, "#3D2A54")
TRANSPARENT_GRADIENT = ft.LinearGradient(
    colors=[ft.Colors.TRANSPARENT, ft.Colors.TRANSPARENT]
)

# Colores para los Toasts por tipo
TOAST_COLORS = {
    "success": {
        "primary": ft.Colors.GREEN_700,
        "secondary": ft.Colors.GREEN_500,
    },
    "error": {
        "primary": ft.Colors.RED_700,
        "secondary": ft.Colors.RED_500,
    },
    "warning": {
        "primary": ft.Colors.AMBER_800,
        "secondary": ft.Colors.AMBER_500,
    },
    "info": {
        "primary": ft.Colors.BLUE_700,
        "secondary": ft.Colors.BLUE_500,
    },
}