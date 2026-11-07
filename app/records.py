
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
JSON_FILE = BASE_DIR / "data" / "records.json"


def load_records():

    if not JSON_FILE.exists():
        raise FileNotFoundError(
            "records.json not found. Run python -m app.ingest first."
        )

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search(records, keyword):

    result = []

    for record in records:

        if keyword.lower() in str(record).lower():
            result.append(record)

    return result


def count_by(records, field):

    counts = {}

    for record in records:

        category = record.get(field, "Unknown")
        counts[category] = counts.get(category, 0) + 1

    return counts


def get_by_id(records, id):

    for record in records:

        if str(record.get("id")) == str(id):
            return record

    return None
