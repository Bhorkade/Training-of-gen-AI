import logging
from typing import Any

try:
    from sentence_transformers import SentenceTransformer
except (ImportError, ModuleNotFoundError):
    SentenceTransformer = None

logger = logging.getLogger(__name__)

_model: Any = None


def get_model() -> Any:
    global _model
    if SentenceTransformer is None:
        return None
    if _model is None:
        try:
            _model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
        except Exception:
            try:
                logger.info("Local model cache not found. Attempting to load 'all-MiniLM-L6-v2'...")
                _model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=False)
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer ({e}). Fallback search will be used.")
                return None
    return _model


def __getattr__(name: str) -> Any:
    if name == "model":
        return get_model()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    if model is None:
        return []
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    model = get_model()
    if model is None:
        return []
    embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embedding.tolist()
