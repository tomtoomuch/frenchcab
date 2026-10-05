from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import joblib
import pandas as pd


from Taxi_PichkupHour import (CHEMIN_MODELE, DEFAULT_DB, NOMS_ZONES,
                              TABLE_TRAJETS, TABLE_ZONES, construire_variables)

def charger_modele(chemin: Path) -> object:
    if not chemin.exists():
        raise FileNotFoundError(f"modèle introuvable {chemin} "
                                f"(lancer modele_duree_trajet.py avant)")
    return joblib.load(chemin)


def charger_courses(db_path: Path, zone_depart: str, zone_arrivee: str) -> pd.DataFrame:
    # lit les courses demandées + la table des zones
    if not db_path.exists():
        raise FileNotFoundError(f"Base introuvable  {db_path}")

    with sqlite3.connect(db_path) as conn:
        courses = pd.read_sql_query(f"""
             SELECT trajets.uid_trajet,
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
                    localisations_pu.zone AS zone_depart,
                    localisations_do.zone AS zone_arrivee
             FROM trajets

            LEFT JOIN localisations AS localisations_pu
                ON trajets.pu_locationID = localisations_pu.locationID

            LEFT JOIN localisations AS localisations_do
                ON trajets.do_locationID = localisations_do.locationID

            WHERE localisations_pu.zone = ?
              AND localisations_do.zone = ?
        """, conn, params=(zone_depart, zone_arrivee))

        if courses.empty:
            raise ValueError(f"Aucune course trouvée de {zone_depart} vers {zone_arrivee}")

        return courses
    
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
        print(f"la course uid_trajet {c['uid_trajet']} "
              f"à {depart:%Y-%m-%d} "
              f"start time {depart:%H:%M} "
              f"a durée {c['duree_predite']:.0f} min "
              f"(réelle {c['trip_duration_min']:.0f} min) "
              f"à localisation {c['quartier_dep']}/{c['zone_dep']}/{c['zone_service_dep']} "
              f"-> {c['quartier_arr']}/{c['zone_arr']}/{c['zone_service_arr']}")


def prediction(pu_locationID: int, do_locationID: int, db_path: Path = DEFAULT_DB) -> float:
    # prédit la durée de la course id_trajet et affiche le résultat
    modele = charger_modele(CHEMIN_MODELE)
    df = charger_courses(db_path, [pu_locationID], [do_locationID])
    df = predire(modele, df)
    afficher(df)
    return float(df["duree_predite"].iloc[0])


if __name__ == "__main__":
    prediction(20)
