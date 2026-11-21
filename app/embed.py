import logging

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Load embedding model from local cache if available; otherwise download (e.g. in CI/Docker)
try:
    model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
except Exception:
    logger.info("Local model cache not found. Downloading 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=False)



def embed_texts(texts):

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings.tolist()


def embed_query(query):

    embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding.tolist()
