import logging
from typing import Any

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        try:
            _model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
        except Exception:
            logger.info("Local model cache not found. Loading 'all-MiniLM-L6-v2'...")
            _model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=False)
    return _model


def __getattr__(name: str) -> Any:
    if name == "model":
        return get_model()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    model = get_model()
    embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embedding.tolist()
