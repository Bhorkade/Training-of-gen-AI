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
        "category",
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
            parts.append(f"{field.replace('_', ' ').title()}: {value}")

    return "\n\n".join(parts)


def chunk_records(records, chunk_size=500, overlap=100):
    """
    Convert all records into chunks with metadata.
    Ensures 'source', 'page', and 'title' are kept on every chunk.
    """
    chunks = []

    for record in records:
        text = record_to_text(record)
        text = text.strip()

        if not text:
            continue

        record_id = str(record.get("id", "unknown"))
        title = str(record.get("title", ""))
        source = str(record.get("source", ""))
        category = str(record.get("category", ""))
        government_level = str(record.get("government_level", ""))
        page = int(record.get("page", 1))

        # Split text into smaller chunks
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_content = text[start:end].strip()

            if chunk_content:
                chunk_id = f"{record_id}_{chunk_index}"
                chunk_item = {
                    "id": chunk_id,
                    "text": chunk_content,
                    "title": title,
                    "source": source,
                    "page": page,
                    "metadata": {
                        "record_id": record_id,
                        "title": title,
                        "source": source,
                        "page": page,
                        "category": category,
                        "government_level": government_level,
                        "chunk_index": chunk_index,
                    },
                }
                chunks.append(chunk_item)
                chunk_index += 1

            start += chunk_size - overlap

    return chunks
