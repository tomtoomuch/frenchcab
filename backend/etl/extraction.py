from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
DEFAULT_INPUT = BASE_DIR / "data" / "query.csv"
DEFAULT_OUTPUT = BASE_DIR / "data" / "clean"

# Noms CSV (minuscules) -> noms officiels TLC
RENAME = {
    "vendorid": "VendorID",
    "tpep_pickup_datetime": "tpep_pickup_datetime",
    "tpep_dropoff_datetime": "tpep_dropoff_datetime",
    "passenger_count": "passenger_count",
    "trip_distance": "trip_distance",
    "ratecodeid": "RatecodeID",
    "store_and_fwd_flag": "store_and_fwd_flag",
    "pulocationid": "PULocationID",
    "dolocationid": "DOLocationID",
    "payment_type": "payment_type",
    "fare_amount": "fare_amount",
    "extra": "extra",
    "mta_tax": "mta_tax",
    "tip_amount": "tip_amount",
    "tolls_amount": "tolls_amount",
    "improvement_surcharge": "improvement_surcharge",
    "total_amount": "total_amount",
    "congestion_surcharge": "congestion_surcharge",
    "airport_fee": "airport_fee",
    "cbd_congestion_fee": "cbd_congestion_fee",
}

INT_COLS = ["VendorID", "passenger_count", "RatecodeID",
            "PULocationID", "DOLocationID", "payment_type"]
MONEY_COLS = ["fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount",
              "improvement_surcharge", "total_amount", "congestion_surcharge",
              "airport_fee", "cbd_congestion_fee"]

VALID_VENDORS = {1, 2, 6, 7}
VALID_RATECODES = {1, 2, 3, 4, 5, 6, 99}
VALID_PAYMENTS = {0, 1, 2, 3, 4, 5, 6}


def transform(df: pd.DataFrame) -> pd.DataFrame:
    # renommage + typage + colonnes dérivées
    df = df.rename(columns=RENAME)

    for c in ("tpep_pickup_datetime", "tpep_dropoff_datetime"):
        df[c] = pd.to_datetime(df[c], format="%Y-%m-%dT%H:%M:%S.%f", errors="coerce")

    for c in INT_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce").round().astype("Int64")

    for c in ["trip_distance"] + [m for m in MONEY_COLS if m in df.columns]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")

    if "cbd_congestion_fee" not in df.columns:
        df["cbd_congestion_fee"] = 0.0

    df["store_and_fwd_flag"] = df["store_and_fwd_flag"].astype("string")

    # Colonnes dérivées utiles pour l'analyse
    df["trip_duration_min"] = (
        (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60
    ).round(2)
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour.astype("Int64")
    df["pickup_weekday"] = df["tpep_pickup_datetime"].dt.dayofweek.astype("Int64")
    return df


def filter_rows(df: pd.DataFrame, year: int | None, stats: Counter) -> pd.DataFrame:

    rules = {
        "date_invalide": df["tpep_pickup_datetime"].isna() | df["tpep_dropoff_datetime"].isna(),
        "hors_annee": (df["tpep_pickup_datetime"].dt.year != year) if year else pd.Series(False, index=df.index),
        "duree_negative_ou_nulle": df["trip_duration_min"] <= 0,
        "duree_sup_6h": df["trip_duration_min"] > 360,
        "distance_nulle_ou_aberrante": (df["trip_distance"] <= 0) | (df["trip_distance"] > 200),
        "montant_negatif_ou_nul": (df["fare_amount"] <= 0) | (df["total_amount"] <= 0),
        "montant_aberrant": df["total_amount"] > 1000,
        "vendor_inconnu": ~df["VendorID"].isin(VALID_VENDORS),
        "ratecode_invalide": ~df["RatecodeID"].isin(VALID_RATECODES),
        "payment_type_invalide": ~df["payment_type"].isin(VALID_PAYMENTS),
    }
    rejected = pd.Series(False, index=df.index)
    for reason, mask in rules.items():
        mask = mask.fillna(True) & ~rejected
        stats[reason] += int(mask.sum())
        rejected |= mask

    df = df[~rejected].copy()

    # passenger_count = 0 -> inconnu,on garde la course
    df.loc[df["passenger_count"] == 0, "passenger_count"] = pd.NA
    # ratecodeID 99 -> inconnu
    df.loc[df["RatecodeID"] == 99, "RatecodeID"] = pd.NA

    before = len(df)
    df = df.drop_duplicates(subset=[c for c in df.columns if c not in ("trip_duration_min",)])
    stats["doublon"] += before - len(df)
    return df


def run(input_path: Path, output_dir: Path, year: int | None, chunksize: int,
        nrows: int | None, apply_filter: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"_{year}" if year else ""
    out_file = output_dir / f"yellow_tripdata{suffix}.csv"

    # On ne lit pas les colonnes techniques Socrata (":id", ":version", ...)
    header = pd.read_csv(input_path, nrows=0).columns
    usecols = [c for c in header if not c.startswith(":")]
    print(f"Colonnes lues ({len(usecols)}) : {usecols}")

    stats: Counter = Counter()
    total_in = total_out = 0
    t0 = time.time()

    reader = pd.read_csv(input_path, usecols=usecols, dtype=str,
                         chunksize=chunksize, nrows=nrows)
    for i, chunk in enumerate(reader, 1):
        total_in += len(chunk)
        df = transform(chunk)
        if apply_filter:
            df = filter_rows(df, year, stats)
        total_out += len(df)

        # 1er morceau : crée le fichier avec l'en-tête ; ensuite : ajoute à la fin
        df.to_csv(out_file, index=False, mode="w" if i == 1 else "a",
                  header=(i == 1), date_format="%Y-%m-%d %H:%M:%S")

        print(f"  chunk {i:>4} | lues {total_in:>12,} | gardées {total_out:>12,} "
              f"| {time.time() - t0:6.0f}s", flush=True)

    report = {
        "fichier_source": str(input_path),
        "fichier_sortie": str(out_file),
        "annee_filtre": year,
        "lignes_lues": total_in,
        "lignes_gardees": total_out,
        "lignes_rejetees": total_in - total_out,
        "taux_rejet_pct": round(100 * (total_in - total_out) / total_in, 2) if total_in else 0,
        "rejets_par_motif": dict(stats),
        "duree_s": round(time.time() - t0, 1),
    }



def main() -> None:
    p = argparse.ArgumentParser(description="extraction nyc yellow taxi csv -> csv propre")
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--year", type=int, default=2023, help="0 = pas de filtre sur l'année")
    p.add_argument("--chunksize", type=int, default=500_000)
    p.add_argument("--nrows", type=int, default=None, help="limiter pour un test")
    p.add_argument("--no-filter", action="store_true", help="ne pas filtrer les anomalies")
    a = p.parse_args()
    run(a.input, a.output, a.year or None, a.chunksize, a.nrows, not a.no_filter)


if __name__ == "__main__":
    main()