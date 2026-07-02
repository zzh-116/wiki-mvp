"""Text embedding service using sentence-transformers with BGE-M3.

BGE-M3:
  - Dense: 1024-dim vectors
  - Multilingual (Chinese/English + 100+ languages)
  - Supports dense + sparse + multi-vector retrieval
"""

from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None
DEFAULT_MODEL = "BAAI/bge-m3"
VECTOR_DIM = 1024


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(DEFAULT_MODEL)
    return _model


def embed_text(text: str) -> list[float]:
    """Generate embedding vector for a single text string."""
    model = get_model()
    vec = model.encode(text, normalize_embeddings=True)
    return vec.tolist()


def embed_batch(texts: list[str], batch_size: int = 32) -> list[list[float]]:
    """Generate embedding vectors for a batch of texts."""
    if not texts:
        return []
    model = get_model()
    vecs = model.encode(texts, batch_size=batch_size, normalize_embeddings=True, show_progress_bar=False)
    return vecs.tolist()
