from __future__ import annotations

import sqlite3 as sqlite
from collections import Counter
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
DEFAULT_INPUT = BASE_DIR / "data" / "clean" / "yellow_tripdata_2023.csv"
BDD_OUTPUT = BASE_DIR / "data" / "frenchcab.db"

BDD_OUTPUT


try:
    df = pd.read_csv(DEFAULT_INPUT,sep=",",encoding="utf-8-sig")
    #print(df)

    connexion = sqlite.connect(BDD_OUTPUT)

    df.to_sql(
        "trajets",
        connexion,
        if_exists="replace",
        index=False
    )
    connexion.close()

    print(f"Données enregistréeés dans {BDD_OUTPUT}")