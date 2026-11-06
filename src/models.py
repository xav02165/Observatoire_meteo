#Validation Pydantic

from pydantic import BaseModel, Field

# --- Modèles ---
class CurrentWeather(BaseModel):
    temperature: float
    windspeed: float = Field(..., alias="windspeed")
    time: str

class WeatherResponseModel(BaseModel):
    latitude: float
    longitude: float
    current_weather: CurrentWeather

# --- Modèles FastAPI ---
class ReleveResponse(BaseModel):
    ville: str
    temperature: float
    vitesse_vent: float
    date_heure: str

    class Config:
        from_attributes = True