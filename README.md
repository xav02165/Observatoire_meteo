# 🌤️ L'Observatoire Météo — Projet Fil Rouge

## 📌 Présentation du Projet
**L'Observatoire Météo** est une application Python complète démontrant la maîtrise du cycle de vie complet de la donnée :
1. **Consommation** d'une API REST externe (Open-Meteo).
2. **Validation & Structuration** des données entrantes avec **Pydantic**.
3. **Persistance** relationnelle locale dans une base **SQLite**.
4. **Exposition** d'une API web moderne et documentée via **FastAPI** et **Swagger UI / Redoc**.
5. **Visualisation** à travers un tableau de bord graphique interactif propulsé par **Streamlit**.

---

## 🛠️ Stack Technique & Concepts Clés

* **Python 3.14+** : Langage principal du projet.
* **`requests`** : Client HTTP pour interroger l'API distante avec gestion d'erreurs (`timeout`, `raise_for_status`, sessions).
* **Pydantic** : Validation stricte des types et conversion automatique des données JSON brutes.
* **SQLite & `sqlite3`** : Stockage relationnel léger (`villes` et `releves` liés par clé étrangère).
* **FastAPI & Uvicorn** : Framework web asynchrone ultra-rapide générant automatiquement la documentation OpenAPI.
* **Swagger UI / Redoc** : Interfaces interactives d'exploration et de test de notre propre API (`/docs` et `/redoc`).
* **Streamlit & Pandas** : Interface utilisateur et création de graphiques interactifs en temps réel.

---

## 📂 Architecture des Fichiers

```text
Obervatoire_Meteo/
│
├── observatoire_db.py    # Jour 1 & 2 : Client HTTP, Modèles Pydantic & Stockage DB SQLite
├── main.py               # Jour 3     : API FastAPI exposant les données stockées
├── app_streamlit.py      # Bonus      : Dashboard graphique Streamlit connecté à FastAPI
├── meteo_observatoire.db # Base de données SQLite (générée automatiquement)
└── README.md             # Documentation complète du projet
```

---

## 📅 Décomposition par Journée

### 🔹 Jour 1 : Client HTTP & Validation Pydantic
* Exploration des endpoints d'Open-Meteo (Query Parameters).
* Écriture d'un client HTTP résilient (`requests.Session`, `timeout`, gestion des exceptions 4xx/5xx).
* Création des modèles Pydantic (`WeatherResponseModel`, `CurrentWeather`) pour garantir le typage strict (`float`, `str`).

### 🔹 Jour 2 : Persistance des Données avec SQLite
* Modélisation de la base avec deux tables relationnelles :
  * `villes` (`id`, `nom`, `latitude`, `longitude`)
  * `releves` (`id`, `ville_id`, `temperature`, `vitesse_vent`, `date_heure`)
* Création du pipeline automatique : `API` ➔ `Pydantic` ➔ `SQLite (INSERT)`.
* Écriture de requêtes SQL de lecture et d'agrégation de relevés.

### 🔹 Jour 3 : Exposition via FastAPI & Documentation Swagger
* Instanciation de l'application FastAPI.
* Définition d'un modèle de réponse Pydantic (`ReleveResponse`).
* Création des endpoints :
  * `GET /` : Page d'accueil et présentation.
  * `GET /meteo/{nom_ville}` : Récupération de l'historique d'une ville (avec gestion d'erreur HTTP 404).
* Exploration de la documentation interactive sur `/docs` (Swagger UI) et `/redoc`.

### 🔹 Bonus : Tableau de Bord Visuel Streamlit
* Interface graphique utilisateur avec barres de recherche, cartes d'indicateurs métriques et graphique d'évolution temporelle de la température (`st.line_chart`).

---

## 🚀 Guide d'Installation et Exécution

### 1. Préparation de l'environnement virtuel
```powershell
# Activer l'environnement virtuel (.venv)
.venv\Scripts\Activate

# Installer toutes les dépendances requises
pip install requests pydantic fastapi uvicorn streamlit pandas
```

### 2. Alimenter la base de données (Jour 1 & 2)
Exécute le script principal pour interroger Open-Meteo, valider et insérer un relevé dans SQLite :
```powershell
python api_meteo.py
```

### 3. Lancer l'API FastAPI (Jour 3)
Démarre le serveur web local Uvicorn :
```powershell
python -m uvicorn main:app --reload
```
Accède ensuite aux documentations dans ton navigateur :
* 📄 **Swagger UI** : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* 📑 **Redoc** : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 4. Lancer le Tableau de Bord Streamlit (Bonus)
Laisse le serveur FastAPI tourner, ouvre un **second terminal** (avec l'environnement virtuel actif) et exécute :
```powershell
streamlit run app_streamlit.py
```
L'application visuelle s'ouvrira automatiquement sur [http://localhost:8501](http://localhost:8501).

---

## 🎯 Résultats Obtenus
* **Architecture découplée** : Le front-end (Streamlit) consomme exclusivement notre propre API (FastAPI), qui elle-même interroge notre base de données (SQLite).
* **Robustesse** : Gestion fine des pannes du réseau distant et typage strict des données à chaque niveau.
* **Documentation auto-générée** : Spécification OpenAPI / Swagger mise à jour automatiquement par FastAPI.