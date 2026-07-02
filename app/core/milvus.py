"""Milvus client helper."""

from pymilvus import MilvusClient
from app.core.config import settings

_client: MilvusClient | None = None


def get_client() -> MilvusClient:
    global _client
    if _client is None:
        _client = MilvusClient(host=settings.milvus_host, port=settings.milvus_port)
    return _client


def init_milvus():
    """Verify Milvus connectivity on startup."""
    mc = get_client()
    mc.list_collections()
    return mc
