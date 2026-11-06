#Fast API et definition des ENDpoints.

from fastapi import FastAPI, HTTPException
from src.database import get_releves_by_ville
from src.models import ReleveResponse

app = FastAPI(
    title="L'Observatoire Météo API",
    description="API REST de restitution des relevés météo enregistrés en base.",
    version="1.0.0"
)

@app.get("/", tags=["Accueil"])
def root():
    return {"message": "Bienvenue sur l'API de L'Observatoire Météo ! Rendez-vous sur /docs."}

@app.get("/meteo/{nom_ville}", response_model=list[ReleveResponse], tags=["Météo"])
def get_meteo(nom_ville: str):
    rows = get_releves_by_ville(nom_ville)
    if not rows:
        raise HTTPException(status_code=404, detail=f"Aucun relevé trouvé pour la ville '{nom_ville}'.")
    
    return [
        ReleveResponse(ville=r[0], temperature=r[1], vitesse_vent=r[2], date_heure=r[3])
        for r in rows
    ]