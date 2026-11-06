from data.sample_records import RECORDS


def load_records():
    return RECORDS


def search(records, keyword):
    results = []

    for record in records:
        if keyword.lower() in str(record).lower():
            results.append(record)

    return results


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