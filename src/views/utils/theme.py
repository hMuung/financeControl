# src/views/utils/theme.py
from flet import Alignment, LinearGradient, BoxShadow, Offset

# BASE DEL SISTEMA (FONDO Y SUPERFICIES)
COLOR_BG_MAIN = "#21193A"  # Fondo principal negro violaceo profundo
COLOR_SURFACE_CARD = "#151026"  # Superficie elevada para tarjetas base y contenedores
COLOR_ACCENT_PRIMARY = "#9D4EDD"  # Acento primario morado neon
COLOR_ACCENT_BRIGHT = "#C77DFF"  # Acento brillante para elementos activos o destacados


# GRADIENTE DE FONDO
BACKGROUND_GRADIENT = LinearGradient(
    begin=Alignment.TOP_LEFT,
    end=Alignment.BOTTOM_RIGHT,
    colors=[COLOR_BG_MAIN, COLOR_SURFACE_CARD],
)

# TARJETA CRISTALINA (GLASSMORPHISM)
# Gradiente traslucido de fondo para el efecto de cristal
GRADIENT_GLASS_CARD = LinearGradient(
    begin=Alignment.TOP_LEFT,
    end=Alignment.BOTTOM_RIGHT,
    colors=["#14FFFFFF", "#0D9D4EDD"],  # Blanco 8% a Morado 5% de opacidad (Formato ARGB)
)

# Resplandor morado para el cristal
GLASS_CARD_SHADOW = BoxShadow(
    spread_radius=1,
    blur_radius=20,
    color="#4D9D4EDD",  # Glow morado con 30% de opacidad
    offset=Offset(0, 8),
)

COLOR_GLASS_BORDER_TOP = "#FFFFFF"  # Borde superior e izquierdo (reflejo de luz, 20% opacidad)
COLOR_GLASS_BORDER_BOTTOM = "#9D4EDD"  # Borde inferior y derecho (sombra de color, 15% opacidad)

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
GRADIENT_BTN_PRIMARY = LinearGradient(
    begin=Alignment.TOP_LEFT,
    end=Alignment.BOTTOM_RIGHT,
    colors=["#7B2CBF", "#9D4EDD"],
)

# Gradiente del boton principal al interactuar (Hover/Press)
GRADIENT_BTN_PRIMARY_HOVER = LinearGradient(
    begin=Alignment.TOP_LEFT,
    end=Alignment.BOTTOM_RIGHT,
    colors=["#9D4EDD", "#C77DFF"],
)

FLOATING_BUTTON_SHADOW = BoxShadow(
    spread_radius=1,
    blur_radius=12,
    color="#66000000",
    offset=Offset(0, 4),
)

COLOR_BTN_SECONDARY_BG = "#0FFFFFFF"  # Fondo de boton secundario estilo cristal
COLOR_BTN_SECONDARY_BORDER = "#4DC77DFF"  # Borde acentuado para boton secundario
COLOR_BTN_SECONDARY_TEXT = "#E0AAFF"  # Texto vibrante para boton secundario
COLOR_BTN_TERTIARY_TEXT = "#8E82A0"  # Texto de boton terciario o accion de cancelar

# INCOME Y EXPENSE
INCOME_COLOR = "#25DCC4"  # Turquesa neón
EXPENSE_COLOR = "#FF007F"  # Magenta
ALERT_COLOR = "#FFB703"
BALANCE_COLOR = "#3A86FF"  # Azul neón
