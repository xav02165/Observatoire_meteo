from src.services import fetch_and_store_weather_by_city


def main():
  print("==========================================")
  print(" ------- L'OBSERVATOIRE MÉTÉO ----------- ")
  print("==========================================")

  ville = input(" Entrez le nom d'une ville : ").strip()

  if not ville:
    print(" Le nom de la ville ne peut pas être vide.")
    return

  try:
    print(f" Recherche des coordonnées pour '{ville}'...")
    nom_ville, weather = fetch_and_store_weather_by_city(ville)

    print("\n Relevé enregistré avec succès dans la base !")
    print(f" Ville : {nom_ville}")
    print(f" Température : {weather.temperature} °C")
    print(f" Vitesse du vent : {weather.windspeed} km/h")
    print(f" Date et heure : {weather.time}")

  except ValueError as ve:
    print(f" Erreur : {ve}")
  except Exception as e:
    print(f" Une erreur inattendue est survenue : {e}")


if __name__ == "__main__":
  main()