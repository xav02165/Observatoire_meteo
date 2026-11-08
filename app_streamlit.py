import pandas as pd
import requests
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="L'Observatoire Météo", page_icon="", layout="centered"
)

st.title(" L'Observatoire Météo par Xavier")
st.markdown("Tableau de bord interactif connecté à notre propre API FastAPI.")

# Barre de recherche de ville
ville_saisie = st.text_input(
    "Entrez le nom d'une ville (ex: Dunkerque)", "Dunkerque"
)

if st.button(" Charger la météo"):
  try:
    # On interroge notre propre API FastAPI créée au Jour 3
    url = f"http://127.0.0.1:8000/meteo/{ville_saisie}"
    response = requests.get(url)

    if response.status_code == 200:
      data = response.json()
      df = pd.DataFrame(data)

      # Affichage des indicateurs clés (dernière valeur)
      dernier = df.iloc[0]
      col1, col2 = st.columns(2)
      with col1:
        st.metric(
            label=" Température actuelle",
            value=f"{dernier['temperature']} °C",
        )
      with col2:
        st.metric(
            label=" Vitesse du vent", value=f"{dernier['vitesse_vent']} km/h"
        )

      st.markdown("---")
      st.subheader(f" Historique des relevés pour : {ville_saisie}")

      
      # Préparation des données pour les graphiques
      df["date_heure"] = pd.to_datetime(df["date_heure"])
      df = df.sort_values("date_heure")

      # Affichage du graphique de température
      st.subheader(" Évolution de la température et de la vitesse du vent")
      st.line_chart(df.set_index("date_heure")[["temperature", "vitesse_vent"]])
      

      # Affichage du tableau de données complet
      with st.expander(" Voir les détails bruts en tableau"):
        st.dataframe(df)
      

    else:
      st.warning(f"Aucune donnée trouvée pour la ville : '{ville_saisie}'.")

  except requests.exceptions.ConnectionError:
    st.error(
        " Impossible de se connecter à l'API FastAPI. Vérifie que ton serveur"
        " Uvicorn est bien lancé !"
    )