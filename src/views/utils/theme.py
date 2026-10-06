import flet as ft

# BASE DEL SISTEMA (FONDO Y SUPERFICIES)
COLOR_BG_MAIN = "#09070F"  # Fondo principal negro violaceo profundo
COLOR_SURFACE_CARD = "#151026"  # Superficie elevada para tarjetas base y contenedores
COLOR_ACCENT_PRIMARY = "#9D4EDD"  # Acento primario morado neon
COLOR_ACCENT_BRIGHT = "#C77DFF"  # Acento brillante para elementos activos o destacados

# TARJETA CRISTALINA (GLASSMORPHISM)
# Gradiente traslucido de fondo para el efecto de cristal
GRADIENT_GLASS_CARD = ft.LinearGradient(
    begin=ft.Alignment.TOP_LEFT,
    end=ft.Alignment.BOTTOM_RIGHT,
    colors=["#14FFFFFF", "#0D9D4EDD"],  # Blanco 8% a Morado 5% de opacidad (Formato ARGB)
)

COLOR_GLASS_BORDER_TOP = "#33FFFFFF"  # Borde superior e izquierdo (reflejo de luz, 20% opacidad)
COLOR_GLASS_BORDER_BOTTOM = "#269D4EDD"  # Borde inferior y derecho (sombra de color, 15% opacidad)

# TIPOGRAFIA (TEXTOS Y TITULOS)
TEXT_PRIMARY = "#FFFFFF"  # Titulos principales, balances e informacion critica
TEXT_SECONDARY = "#E2D9F3"  # Textos de cuerpo, subtitulos y lecturas largas
TEXT_MUTED = "#8E82A0"  # Etiquetas secundarias, placeholders y textos tenues
TEXT_DISABLED = "#4D435D"  # Estado deshabilitado o elementos inactivos

# CAMPOS DE TEXTO E INPUTS
INPUT_BG_IDLE = "#0AFFFFFF"  # Fondo del campo de texto en reposo (4% opacidad)
INPUT_BORDER_IDLE = "#1AFFFFFF"  # Borde del campo de texto en reposo (10% opacidad)
INPUT_BORDER_FOCUS = "#9D4EDD"  # Borde activo cuando el campo recibe foco

# BOTONES Y ACCIONES
# Gradiente para boton de accion principal
GRADIENT_BTN_PRIMARY = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    colors=["#7B2CBF", "#9D4EDD"],
)

# Gradiente del boton principal al interactuar (Hover/Press)
GRADIENT_BTN_PRIMARY_HOVER = ft.LinearGradient(
    begin=ft.Alignment.TOP_LEFT,
    end=ft.Alignment.BOTTOM_RIGHT,
    colors=["#9D4EDD", "#C77DFF"],
)

COLOR_BTN_SECONDARY_BG = "#0FFFFFFF"  # Fondo de boton secundario estilo cristal
COLOR_BTN_SECONDARY_BORDER = "#4DC77DFF"  # Borde acentuado para boton secundario
COLOR_BTN_SECONDARY_TEXT = "#E0AAFF"  # Texto vibrante para boton secundario
COLOR_BTN_TERTIARY_TEXT = "#8E82A0"  # Texto de boton terciario o accion de cancelar