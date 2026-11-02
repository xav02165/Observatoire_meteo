from pydantic import BaseModel, ValidationError
import requests
from requests.exceptions import RequestException

# ==========================================
# 1. DÉFINITION DES MODÈLES PYDANTIC
# ==========================================
# Open-Meteo renvoie un dictionnaire imbriqué. On structure
# nos modèles pour correspondre exactement à ce format JSON.

class CurrentWeather(BaseModel):
    time: str
    temperature_2m: float
    wind_speed_10m: float

class WeatherResponseModel(BaseModel):
    latitude: float
    longitude: float
    current: CurrentWeather


# ==========================================
# 2. FONCTION DE REQUÊTE HTTP ROBUSTE
# ==========================================
def fetch_weather_data(lat: float, lon: float) -> dict:
    """
    Interroge l'API Open-Meteo avec une gestion rigoureuse des erreurs réseau.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m"
    }

    # Utilisation d'un bloc 'with requests.Session()' pour optimiser les connexions HTTP
    try:
        with requests.Session() as session:
            # Timeout de 10 secondes pour éviter de bloquer indéfiniment
            response = session.get(url, params=params, timeout=10)
            
            # Vérifie si le code de statut indique une erreur (4xx ou 5xx)
            response.raise_for_status()
            
            # Retourne les données sous forme de dictionnaire Python brut
            return response.json()

    except requests.exceptions.Timeout:
        print(" Erreur : Le serveur Open-Meteo met trop de temps à répondre (Timeout).")
        raise
    except requests.exceptions.HTTPError as http_err:
        print(f" Erreur HTTP : {http_err} (Statut: {response.status_code})")
        raise
    except RequestException as err:
        print(f" Erreur réseau critique : {err}")
        raise


# ==========================================
# 3. EXÉCUTION DU SCRIPT (PIPELINE JOUR 1)
# ==========================================
if __name__ == "__main__":
    # Coordonnées de Dunkerque (Latitude, Longitude)
    LATITUDE = 51.0344
    LONGITUDE = 2.3767

    print(f" Interrogation de l'API Open-Meteo pour les coordonnées ({LATITUDE}, {LONGITUDE})...")

    try:
        # Étape A : Récupération des données brutes
        raw_data = fetch_weather_data(LATITUDE, LONGITUDE)
        print(" Données brutes récupérées avec succès !")

        # Étape B : Validation rigoureuse via Pydantic
        # Si une clé manque ou si un type est incorrect (ex: température en string au lieu de float),
        # Pydantic lève une exception 'ValidationError'.
        validated_weather = WeatherResponseModel(**raw_data)
        
        print("\n Données validées et structurées par Pydantic :")
        print(f"   - Latitude : {validated_weather.latitude}")
        print(f"   - Longitude : {validated_weather.longitude}")
        print(f"   - Heure du relevé : {validated_weather.current.time}")
        print(f"   - Température : {validated_weather.current.temperature_2m} °C")
        print(f"   - Vitesse du vent : {validated_weather.current.wind_speed_10m} km/h")

    except ValidationError as val_err:
        print(" Erreur de validation Pydantic : Les données reçues ne respectent pas le contrat attendu.")
        print(val_err)
    except Exception as e:
        print(f" Une erreur inattendue est survenue : {e}")