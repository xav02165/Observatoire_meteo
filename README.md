# 🌤️ L'Observatoire Météo — Projet Fil Rouge 

## 📌 Présentation du Projet
**L'Observatoire Météo** est une application Python complète démontrant la maîtrise du cycle de vie complet de la donnée à travers une **Clean Architecture** modulaire :
1. **Géocodage & Recherche** : Recherche dynamique de n'importe quelle ville du monde via l'API Open-Meteo Geocoding.
2. **Consommation & Validation** : Récupération météo et validation stricte des structures avec **Pydantic v2**.
3. **Persistance Relationnelle** : Stockage local dans une base **SQLite** avec gestion centralisée des connexions et des entités (`villes` et `releves`).
4. **Exposition REST API** : Backend asynchrone propulsé par **FastAPI** avec documentation interactive automatique (**Swagger UI / Redoc**).
5. **Visualisation Graphique** : Tableau de bord réactif **Streamlit** pour analyser les séries temporelles (température et vitesse du vent).
6. **Interface Interactive (CLI)** : Script en ligne de commande pour interroger et enregistrer des données à la volée.

---

## 🛠️ Stack Technique

* **Python 3.14+** : Langage principal.
* **`requests`** : Client HTTP pour interroger les APIs distantes (Géocodage & Météo).
* **Pydantic v2** : Typer strict et validation des données (champs et alias).
* **SQLite3** : Base de données relationnelle locale légère.
* **FastAPI & Uvicorn** : Backend RESTful asynchrone et documentation OpenAPI.
* **Streamlit & Pandas** : Dashboard interactif et graphiques d'évolution temporelle.

---

## 📂 Architecture Modulaire du Projet

```text
Obervatoire_Meteo/
│
├── src/                        # Code source backend (Logique métier & Data)
│   ├── __init__.py             # Package Python
│   ├── config.py               # Centralisation des constantes et chemins
│   ├── database.py             # Gestion des connexions SQLite & requêtes SQL
│   ├── models.py               # Schémas Pydantic (Ingestion & Réponses API)
│   └── services.py             # Services de géocodage et d'ingestion météo
│
├── api/                        # Couche d'exposition Web API
│   ├── __init__.py             # Package API
│   └── main.py                 # Endpoints FastAPI et documentation OpenAPI
│
├── cli.py                      # Script CLI interactif pour rechercher et enregistrer une ville
├── app_streamlit.py            # Interface utilisateur Streamlit
├── meteo_observatoire.db       # Base de données SQLite relationnelle
├── requirements.txt            # Dépendances du projet
└── README.md                   # Documentation complète
```

---

## 🚀 Guide d'Installation et d'Exécution

### 1. Préparation de l'environnement virtuel et dépendances

```powershell
# Activer l'environnement virtuel (.venv)
.venv\Scripts\Activate

# Installer les dépendances depuis le requirements.txt
pip install -r requirements.txt
```

### 2. Alimenter la base de données via le CLI interactif
Exécute le script en ligne de commande pour rechercher n'importe quelle ville dans le monde, récupérer ses coordonnées GPS et enregistrer son relevé météo en base :

```powershell
python cli.py
```
*(Le script  demandera d'entrer le nom d'une ville, ex: `Paris`, `Tokyo`, `Dunkerque`, etc.)*

### 3. Lancer l'API FastAPI (Backend REST)
Démarre le serveur Uvicorn en pointant vers le module `api.main` :

```powershell
python -m uvicorn api.main:app --reload
```

Accéder aux documentations interactives :
* 📄 **Swagger UI** : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* 📑 **Redoc** : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 4. Lancer le Tableau de Bord Streamlit (Front-End)
Dans un **second terminal** (avec l'environnement virtuel actif), exécuter :

```powershell
streamlit run app_streamlit.py
```

L'application s'ouvrira sur [http://localhost:8501](http://localhost:8501) et affichera :
* Les métriques clés en temps réel (Température & Vent).
* Le graphique d'évolution de la température.
* Le graphique d'évolution de la vitesse du vent.
* L'historique complet des relevés sous forme de tableau interactif.

---

## 📦 Exporter ses dépendances (`requirements.txt`)

Pour régénérer le fichier de dépendances lors de l'ajout de nouveaux packages :

```powershell
pip freeze > requirements.txt
```