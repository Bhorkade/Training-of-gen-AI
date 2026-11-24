
import logging
from pathlib import Path
from typing import Any

import chromadb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.chunking import chunk_records
from app.embed import embed_query, embed_texts
from app.records import load_records

logger = logging.getLogger(__name__)

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
# SEMANTIC SEARCH (Dense Vector + Resilient Fallback)
# --------------------------------------------------

_cached_chunks = None
_cached_vectorizer = None
_cached_doc_vectors = None


def _get_chunk_index():
    global _cached_chunks, _cached_vectorizer, _cached_doc_vectors
    if _cached_chunks is None:
        try:
            records = load_records()
            _cached_chunks = chunk_records(records)
            docs = [c["text"] for c in _cached_chunks]
            _cached_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            _cached_doc_vectors = _cached_vectorizer.fit_transform(docs)
        except Exception as e:
            logger.warning(f"Error building chunk index: {e}")
            _cached_chunks = []
    return _cached_chunks, _cached_vectorizer, _cached_doc_vectors


def tfidf_chunk_search(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Zero-memory resilient chunk retriever for low-memory environments."""
    chunks, vectorizer, doc_vectors = _get_chunk_index()
    if not chunks or vectorizer is None:
        return []

    try:
        q_vec = vectorizer.transform([query])
        scores = cosine_similarity(q_vec, doc_vectors).flatten()
        top_indices = scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(scores[idx])
            if score > 0:
                # Scale slightly so keyword matches align with min_score threshold
                normalized_score = round(min(1.0, score * 1.25), 4)
                results.append({
                    "id": chunks[idx]["id"],
                    "text": chunks[idx]["text"],
                    "metadata": chunks[idx]["metadata"],
                    "similarity_score": normalized_score
                })
        return results
    except Exception as e:
        logger.warning(f"TF-IDF search error: {e}")
        return []


def semantic_search(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """
    Search chunks using ChromaDB dense embeddings, with graceful fallback
    to TF-IDF chunk retrieval if dense embeddings or ChromaDB are unavailable.
    """
    if not query or not query.strip():
        return []

    # 1. Attempt dense search via ChromaDB
    try:
        query_embedding = embed_query(query)
        if query_embedding:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=[
                    "documents",
                    "metadatas",
                    "distances"
                ]
            )
            if results and results.get("ids") and len(results["ids"][0]) > 0:
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
    except Exception as e:
        logger.warning(f"ChromaDB search encountered an issue ({e}). Using resilient TF-IDF retriever.")

    # 2. Resilient ultra-fast fallback (works with 0 MB neural memory)
    return tfidf_chunk_search(query, top_k=top_k)


# --------------------------------------------------
# RUN INDEXING
# --------------------------------------------------

if __name__ == "__main__":

    index_documents()
