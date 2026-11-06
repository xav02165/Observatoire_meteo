#Centralisation des variables

from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "meteo_observatoire.db"

# URLs des services externes
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"