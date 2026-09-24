# src/config.py
from pathlib import Path

# Directorio raiz
BASE_DIR = Path(__file__).resolve().parent

# Localizar carpeta de assets
if (BASE_DIR / "assets").exists():
    ASSETS_DIR = BASE_DIR / "assets"
else:
    ASSETS_DIR = BASE_DIR.parent / "assets"

# Rutas especificas
ICONS_DIR = ASSETS_DIR / "icon"
APP_LOGO_PATH = ICONS_DIR / "icon.png"
APP_ICON_PATH = ICONS_DIR / "appIcon.png"


DB_NAME = "finance_control.db"

print("New Start")