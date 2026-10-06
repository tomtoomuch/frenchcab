from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import joblib
import pandas as pd
from datetime import date, time, datetime
from pathlib import Path


from Taxi_PichkupHour import (CHEMIN_MODELE, DEFAULT_DB, NOMS_ZONES,
                              TABLE_TRAJETS, TABLE_ZONES, construire_variables)

def charger_modele(chemin: Path) -> object:
    if not chemin.exists():
        raise FileNotFoundError(f"modèle introuvable {chemin} "
                                f"(lancer modele_duree_trajet.py avant)")
    return joblib.load(chemin)



def charger_courses(db_path: Path, zone_depart: str, zone_arrivee: str, tpep_pickup_datetime: date, pickup_hour: time) -> pd.DataFrame:

    if not db_path.exists():
        raise FileNotFoundError(f"Base introuvable : {db_path}")

    date_str = tpep_pickup_datetime.strftime("%Y-%m-%d")
    pickup_hour_str = pickup_hour.strftime("%H:%M:%S")

    with sqlite3.connect(db_path) as conn:

        courses = pd.read_sql_query("""
            SELECT
                trajets.uid_trajet,
                trajets.tpep_pickup_datetime,
                trajets.trip_duration_min,
                trajets.trip_distance,
                trajets.pickup_hour,
                trajets.pickup_weekday,
                trajets.passenger_count,
                trajets.RateCodeID,
                trajets.vendorID,
                trajets.pu_locationID,
                trajets.do_locationID,

                localisations_pu.quartier AS quartier_dep,
                localisations_pu.zone AS zone_dep,
                localisations_pu.zone_service AS zone_service_dep,

                localisations_do.quartier AS quartier_arr,
                localisations_do.zone AS zone_arr,
                localisations_do.zone_service AS zone_service_arr

            FROM trajets

            LEFT JOIN localisations AS localisations_pu
                ON trajets.pu_locationID = localisations_pu.locationID

            LEFT JOIN localisations AS localisations_do
                ON trajets.do_locationID = localisations_do.locationID

            WHERE localisations_pu.zone = ?
              AND localisations_do.zone = ?
              AND DATE(trajets.tpep_pickup_datetime) = ?
              AND trajets.pickup_hour = ?

        """, conn, params=(zone_depart, zone_arrivee, date_str, pickup_hour_str)
        )

    if courses.empty:
        raise ValueError(
            f"Aucune course trouvée de {zone_depart} vers {zone_arrivee} "
            f"le {date_str} à {pickup_hour_str}"
        )

    return courses



def construire_course_prediction(db_path: Path, zone_depart: str, zone_arrivee: str, date_depart: date, heure_depart: time) -> pd.DataFrame:

    if not db_path.exists():
        raise FileNotFoundError(f"Base introuvable : {db_path}")

    with sqlite3.connect(db_path) as conn:

        depart = pd.read_sql_query(
            """
            SELECT
                locationID,
                quartier,
                zone,
                zone_service
            FROM localisations
            WHERE zone = ?
            LIMIT 1
            """,
            conn,
            params=(zone_depart,)
        )

        arrivee = pd.read_sql_query(
            """
            SELECT
                locationID,
                quartier,
                zone,
                zone_service
            FROM localisations
            WHERE zone = ?
            LIMIT 1
            """,
            conn,
            params=(zone_arrivee,)
        )

    if depart.empty:
        raise ValueError(f"Zone de départ '{zone_depart}' introuvable")

    if arrivee.empty:
        raise ValueError(f"Zone d'arrivée '{zone_arrivee}' introuvable")

    dep = depart.iloc[0]
    arr = arrivee.iloc[0]

    datetime_depart = datetime.combine( date_depart, heure_depart)

    df = pd.DataFrame([{
        "tpep_pickup_datetime": datetime_depart,

        "pickup_hour": heure_depart.strftime("%H:%M:%S"),
        "pickup_weekday": date_depart.weekday(),

        "pu_locationID": int(dep["locationID"]),
        "do_locationID": int(arr["locationID"]),

        "quartier_dep": dep["quartier"],
        "zone_dep": dep["zone"],
        "zone_service_dep": dep["zone_service"],

        "quartier_arr": arr["quartier"],
        "zone_arr": arr["zone"],
        "zone_service_arr": arr["zone_service"],
    }])

    return df

def predire(modele, df: pd.DataFrame) -> pd.DataFrame:
    # mêmes transformations que pendant l'entraînement
    X = construire_variables(df.copy())
    # le modèle se souvient des colonnes qu'il a vues pendant l'entraînement
    X = X[list(modele.feature_names_in_)]
    df["duree_predite"] = modele.predict(X)
    return df


def afficher(df: pd.DataFrame) -> None:
    for _, c in df.iterrows():
        depart = pd.to_datetime(c["tpep_pickup_datetime"])

        print(
            f"Course prévue le {depart:%Y-%m-%d} "
            f"à {depart:%H:%M} "
            f"de {c['quartier_dep']}/{c['zone_dep']}/{c['zone_service_dep']} "
            f"vers {c['quartier_arr']}/{c['zone_arr']}/{c['zone_service_arr']} "
            f"- durée prédite : {c['duree_predite']:.0f} min"
        )


def prediction(zone_depart: str, zone_arrivee: str, tpep_pickup_datetime: date , pickup_hour:time, db_path: Path = DEFAULT_DB) -> float:
    # prédit la durée de la course id_trajet et affiche le résultat
    modele = charger_modele(CHEMIN_MODELE)
    df = charger_courses(db_path, zone_depart, zone_arrivee, tpep_pickup_datetime, pickup_hour)
    df = predire(modele, df)
    afficher(df)
    return float(df["duree_predite"].iloc[0])


if __name__ == "__main__":
    prediction(20)
