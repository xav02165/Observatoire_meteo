#Gestion SQLite

import sqlite3
from src.config import DB_NAME

def get_connection():
    """Fournit une connexion à la base SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initialise le schéma de la base de données."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS villes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS releves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ville_id INTEGER NOT NULL,
                temperature REAL NOT NULL,
                vitesse_vent REAL NOT NULL,
                date_heure TEXT NOT NULL,
                FOREIGN KEY (ville_id) REFERENCES villes (id)
            );
        """)
        conn.commit()

def insert_releve(ville_nom: str, lat: float, lon: float, temp: float, vent: float, date_heure: str):
    """Insère ou récupère la ville, puis enregistre un nouveau relevé."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO villes (nom, latitude, longitude) VALUES (?, ?, ?)", (ville_nom, lat, lon))
        cursor.execute("SELECT id FROM villes WHERE nom = ?", (ville_nom,))
        ville_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO releves (ville_id, temperature, vitesse_vent, date_heure)
            VALUES (?, ?, ?, ?)
        """, (ville_id, temp, vent, date_heure))
        conn.commit()

def get_releves_by_ville(ville_nom: str):
    """Récupère tous les relevés d'une ville."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.nom, r.temperature, r.vitesse_vent, r.date_heure
            FROM releves r
            JOIN villes v ON r.ville_id = v.id
            WHERE v.nom COLLATE NOCASE = ?
            ORDER BY r.id DESC
        """, (ville_nom,))
        return cursor.fetchall()