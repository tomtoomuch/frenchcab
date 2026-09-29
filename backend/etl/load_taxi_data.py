from __future__ import annotations

import argparse
import csv
import time
from collections import Counter
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
DEFAULT_INPUT = BASE_DIR / "data" / "clean" / "yellow_tripdata_2023.csv"

df = pd.read_csv()