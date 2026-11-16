
def chunk_text(text, chunk_size=120, overlap=20):
    """
    Split text into word-based chunks.
    overlap keeps some words from the previous chunk.
    """
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def record_to_text(record):
    """
    Convert one startup record into searchable text.
    """
    fields = [
        "title",
        "description",
        "eligibility",
        "benefits",
        "application_process",
        "funding_amount",
        "entity_type",
    ]

    parts = []

    for field in fields:
        value = record.get(field)

        if value:
            parts.append(f"{field}: {value}")

    return "\n".join(parts)


def chunk_records(records):
    """
    Convert all records into chunks with metadata.
    """
    all_chunks = []

    for record in records:
        text = record_to_text(record)
        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{record['id']}-chunk-{index}",
                "text": chunk,
                "metadata": {
                    "record_id": str(record["id"]),
                    "title": str(record.get("title", "")),
                    "category": str(record.get("category", "")),
                    "source": str(record.get("source", "")),
                    "government_level": str(
                        record.get("government_level", "")
                    ),
                    "chunk_index": index,
                }
            })

def chunk_records(records, chunk_size=500, overlap=100):

    chunks = []

    for record in records:

        # Combine important record fields
        text = f"""
Title: {record.get('title', '')}

Category: {record.get('category', '')}

Description: {record.get('description', '')}

Eligibility: {record.get('eligibility', '')}

Benefits: {record.get('benefits', '')}

Application Process: {record.get('application_process', '')}
"""

        text = text.strip()

        if not text:
            continue

        # Split text into smaller chunks
        start = 0
        chunk_index = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "id": f"{record.get('id', 'unknown')}_{chunk_index}",

                    "text": chunk_text,

                    "metadata": {
                        "record_id": str(record.get("id", "")),
                        "title": str(record.get("title", "")),
                        "category": str(record.get("category", "")),
                        "source": str(record.get("source", "")),
                        "chunk_index": chunk_index
                    }
                })

                chunk_index += 1

            # Move forward with overlap
            start += chunk_size - overlap

    return chunks

    return all_chunks
