
import csv
import json
from pathlib import Path


# Project folder location
BASE_DIR = Path(__file__).resolve().parent.parent

# CSV input file
CSV_FILE = BASE_DIR / "data" / "raw" / "gov-data-final.csv"

# JSON output file
JSON_FILE = BASE_DIR / "data" / "records.json"


def clean_value(value):
    """Remove unnecessary spaces from values."""

    if value is None:
        return ""

    return str(value).strip()


def get_value(row, possible_names):
    """Find a value using possible column names."""

    for key, value in row.items():

        if key.lower().strip().replace(" ", "_") in possible_names:
            if value:
                return clean_value(value)

    return ""


def clean_record(row, row_number):
    """Convert one CSV row into a StartupSetu record."""

    cleaned_row = {}

    for key, value in row.items():

        if key is not None and key.strip():
            cleaned_row[key.strip()] = clean_value(value)

    # Skip completely empty rows
    if not any(cleaned_row.values()):
        return None

    record_id = get_value(
        cleaned_row,
        {"id", "record_id", "serial_no", "sr_no"}
    )

    title = get_value(
        cleaned_row,
        {
            "title",
            "name",
            "scheme_name",
            "startup_name",
            "company_name"
        }
    )

    category = get_value(
        cleaned_row,
        {
            "category",
            "sector",
            "industry",
            "state",
            "type"
        }
    )

    eligibility = get_value(
        cleaned_row,
        {
            "eligibility",
            "eligibility_criteria",
            "criteria"
        }
    )

    source = get_value(
        cleaned_row,
        {
            "source",
            "source_url",
            "url",
            "link"
        }
    )

    # Use the first available value as the title
    if not title:
        title = next(
            (value for value in cleaned_row.values() if value),
            "Untitled Record"
        )

    # Preserve all original CSV information
    description = " | ".join(
        f"{key}: {value}"
        for key, value in cleaned_row.items()
        if value
    )

    return {
        "id": record_id or str(row_number),
        "title": title,
        "category": category or "General",
        "description": description,
        "eligibility": eligibility,
        "source": source or "gov-data-final.csv"
    }


def ingest_data():

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_FILE}"
        )

    records = []
    bad_rows = 0

    with open(
        CSV_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file has no column headings.")

        for row_number, row in enumerate(reader, start=1):

            try:
                record = clean_record(row, row_number)

                if record is not None:
                    records.append(record)

            except (ValueError, TypeError, AttributeError) as error:
                bad_rows += 1
                print(f"Skipping row {row_number}: {error}")

    # Save cleaned records as JSON
    with open(JSON_FILE, "w", encoding="utf-8") as file:

        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nData ingestion completed!")
    print("Total valid records:", len(records))
    print("Bad rows:", bad_rows)
    print("Saved file:", JSON_FILE)


if __name__ == "__main__":
    ingest_data()
