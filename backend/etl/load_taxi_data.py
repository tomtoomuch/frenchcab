from __future__ import annotations

import argparse
import csv
import time
from collections import Counter
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
DEFAULT_INPUT = BASE_DIR / "data" / "query.csv"

df = pd.read_csv()