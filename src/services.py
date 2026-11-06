#API open meteo


import requests
from src.config import OPEN_METEO_URL
from src.database import init_db, insert_releve
from src.models import WeatherResponseModel

# URL de l'API de géocodage Open-Meteo
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def get_city_coordinates(city_name: str):
  """Interroge l'API de géocodage pour trouver la latitude,

  la longitude et le nom officiel d'une ville.
  """
  params = {"name": city_name, "count": 1, "language": "fr"}
  response = requests.get(GEOCODING_URL, params=params, timeout=10)
  response.raise_for_status()

  data = response.json()
  if "results" not in data or not data["results"]:
    return None

  result = data["results"][0]
  return {
      "name": result.get("name"),
      "latitude": result.get("latitude"),
      "longitude": result.get("longitude"),
      "country": result.get("country", ""),
  }


def fetch_and_store_weather_by_city(ville_nom: str):
  """Recherche une ville, récupère sa météo actuelle et l'enregistre en base."""
  init_db()  # S'assure que les tables existent

  # 1. Récupération des coordonnées dynamiques
  coords = get_city_coordinates(ville_nom)
  if not coords:
    raise ValueError(f"Ville introuvable : '{ville_nom}'")

  nom_officiel = f"{coords['name']} ({coords['country']})" if coords['country'] else coords['name']
  lat = coords["latitude"]
  lon = coords["longitude"]

  # 2. Requête météo sur Open-Meteo avec les coordonnées trouvées
  params = {"latitude": lat, "longitude": lon, "current_weather": True}

  response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
  response.raise_for_status()

  # 3. Validation Pydantic
  data_valid = WeatherResponseModel(**response.json())
  cw = data_valid.current_weather

  # 4. Persistance en base SQLite
  insert_releve(
      ville_nom=nom_officiel,
      lat=lat,
      lon=lon,
      temp=cw.temperature,
      vent=cw.windspeed,
      date_heure=cw.time,
  )

  return nom_officiel, cw