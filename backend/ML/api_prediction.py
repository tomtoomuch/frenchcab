import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from Taxi_PichkupHour import CHEMIN_MODELE, DEFAULT_DB
from taxi_duree_prediction import construire_course_prediction, charger_modele, predire
from datetime import date, time

app = FastAPI(title="FrenchCab - prédiction durée")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:4200"],
                   allow_methods=["GET"], allow_headers=["*"])

# le modèle est chargé UNE seule fois, au démarrage
modele = charger_modele(CHEMIN_MODELE)


@app.get("/api/prediction")
def prediction_par_location(zone_depart: str, zone_arrivee: str, date_depart: date, heure_depart: time) -> dict:

    try:
        df = construire_course_prediction(DEFAULT_DB, zone_depart, zone_arrivee, date_depart, heure_depart)

    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))

    df = predire(modele, df)

    c = df.iloc[0]

    depart = pd.to_datetime(c["tpep_pickup_datetime"])

    return {
        "depart": zone_depart,
        "arrivee": zone_arrivee,
        "date": f"{depart:%Y-%m-%d}",
        "heure_depart": f"{depart:%H:%M}",
        "distance_moyenne_miles": round(float(c["trip_distance"]),2),
        "duree_predite": round(float(c["duree_predite"]))
    }