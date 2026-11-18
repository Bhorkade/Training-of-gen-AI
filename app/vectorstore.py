
from pathlib import Path

import chromadb

from app.chunking import chunk_records
from app.embed import embed_query, embed_texts
from app.records import load_records

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "startupsetu_collection"


# Persistent ChromaDB client
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


# Create or load collection
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


# --------------------------------------------------
# INDEX ALL DOCUMENT CHUNKS
# --------------------------------------------------

def index_documents():

    # Load original records
    records = load_records()

    # Convert records into chunks
    chunks = chunk_records(records)

    if not chunks:
        print("No chunks found.")
        return

    documents = [
        chunk["text"] for chunk in chunks
    ]

    ids = [
        chunk["id"] for chunk in chunks
    ]

    metadatas = [
        chunk["metadata"] for chunk in chunks
    ]

    # Generate embeddings
    embeddings = embed_texts(documents)

    # Store in ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Indexing completed!")
    print("Total records:", len(records))
    print("Total chunks:", len(chunks))
    print("Chroma collection:", COLLECTION_NAME)


# --------------------------------------------------
# SEMANTIC SEARCH
# --------------------------------------------------

def semantic_search(query, top_k=3):

    if not query.strip():
        return []

    # Convert user question into vector
    query_embedding = embed_query(query)

    # Search similar vectors
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    search_results = []

    for i in range(len(results["ids"][0])):

        distance = results["distances"][0][i]

        search_results.append({

            "id": results["ids"][0][i],

            "text": results["documents"][0][i],

            "metadata": results["metadatas"][0][i],

            "similarity_score": round(
                max(0.0, 1 - distance), 4
            )
        })

    return search_results


# --------------------------------------------------
# RUN INDEXING
# --------------------------------------------------

if __name__ == "__main__":

    index_documents()
