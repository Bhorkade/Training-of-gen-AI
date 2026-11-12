
import csv
import json
from pathlib import Path

from app.models import Record

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "raw" / "startupsetu_master.csv"
JSON_FILE = BASE_DIR / "data" / "records.json"

def ingest_data(csv_file=CSV_FILE):

    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    records = []
    bad_rows = 0

    with open(
        csv_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV has no column headings")

        for row_number, row in enumerate(reader, start=1):

            try:
                if not any(row.values()):
                    continue

                record = Record.from_dict(row, row_number)
                records.append(record.to_dict())

            except (ValueError, TypeError, AttributeError) as error:
                bad_rows += 1
                print(f"Skipping row {row_number}: {error}")

    JSON_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    print("\nData ingestion completed!")
    print("Total valid records:", len(records))
    print("Bad rows:", bad_rows)
    print("Saved file:", JSON_FILE)

if __name__ == "__main__":
    ingest_data()