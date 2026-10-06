import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from Taxi_PichkupHour import CHEMIN_MODELE, DEFAULT_DB
from taxi_duree_prediction import charger_courses, charger_modele, predire
from datetime import date, time

app = FastAPI(title="FrenchCab - prédiction durée")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:4200"],
                   allow_methods=["GET"], allow_headers=["*"])

# le modèle est chargé UNE seule fois, au démarrage
modele = charger_modele(CHEMIN_MODELE)


@app.get("/api/prediction")
def prediction_par_location(zone_depart: str, zone_arrivee: str, tpep_pickup_datetime: date , pickup_hour:time) -> dict:

    try:
        df = charger_courses(DEFAULT_DB, zone_depart, zone_arrivee, tpep_pickup_datetime, pickup_hour)

    except ValueError:
        raise HTTPException(status_code=404, detail=f"Course de {zone_depart} vers {zone_arrivee} le {tpep_pickup_datetime} à {pickup_hour} introuvable")

    df = predire(modele, df)

    c = df.iloc[0]

    depart = pd.to_datetime(c["tpep_pickup_datetime"])

    return {
        "date": f"{depart:%Y-%m-%d}",
        "start_time": f"{depart:%H:%M}",
        "duree_predite": round(float(c["duree_predite"])),
        "duree_reelle": round(float(c["trip_duration_min"])),
        "depart": zone_depart,
        "arrivee": zone_arrivee,
    }