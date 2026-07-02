"""Text embedding service using fastembed (ONNX, lightweight)."""

from fastembed import TextEmbedding

_model: TextEmbedding | None = None
DEFAULT_MODEL = "BAAI/bge-small-zh-v1.5"  # 512-dim, good for Chinese/English
VECTOR_DIM = 512


def get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding(model_name=DEFAULT_MODEL)
    return _model


def embed_text(text: str) -> list[float]:
    """Generate embedding vector for a single text string."""
    model = get_model()
    vec = next(model.embed([text]))
    return vec.tolist()


def embed_batch(texts: list[str], batch_size: int = 32) -> list[list[float]]:
    """Generate embedding vectors for a batch of texts."""
    if not texts:
        return []
    model = get_model()
    vecs = list(model.embed(texts, batch_size=batch_size))
    return [v.tolist() for v in vecs]
