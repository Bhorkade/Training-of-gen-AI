import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

JSON_FILE = BASE_DIR / "data" / "records.json"

df = pd.read_json(JSON_FILE)

print("\n--- STARTUPSETU DATA ANALYSIS ---")

# Fact 1: Total records
print("\n1. Total records:", len(df))

# Fact 2: Category distribution
print("\n2. Records by category:")
print(df["category"].value_counts())

# Fact 3: Missing values
print("\n3. Missing values in each column:")
print(df.isnull().sum())