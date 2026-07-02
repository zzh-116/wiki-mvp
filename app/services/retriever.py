"""Milvus vector store for document chunks."""

from pymilvus import MilvusClient

from app.core.config import settings
from app.services.embedder import VECTOR_DIM

COLLECTION_NAME = "wiki_chunks"


def get_client() -> MilvusClient:
    return MilvusClient(host=settings.milvus_host, port=settings.milvus_port)


def ensure_collection():
    """Create the collection if it doesn't exist, with correct dimension."""
    mc = get_client()
    if COLLECTION_NAME not in mc.list_collections():
        mc.create_collection(
            collection_name=COLLECTION_NAME,
            dimension=VECTOR_DIM,
            auto_id=True,
            enable_dynamic_field=True,
        )
    return mc


def insert_chunks(chunks: list[dict], embeddings: list[list[float]]) -> list[int]:
    """Insert chunk texts + vectors into Milvus.

    Each chunk dict should have: text, page, source, chunk_index
    """
    mc = get_client()
    data = []
    for chunk, vec in zip(chunks, embeddings):
        data.append({
            "vector": vec,
            "text": chunk["text"],
            "page": chunk.get("page"),
            "source": chunk.get("source"),
            "chunk_index": chunk.get("chunk_index"),
        })
    res = mc.insert(collection_name=COLLECTION_NAME, data=data)
    return res.get("ids", [])


def search_chunks(query_vector: list[float], top_k: int = 5) -> list[dict]:
    """Search for similar chunks by vector similarity."""
    mc = get_client()
    results = mc.search(
        collection_name=COLLECTION_NAME,
        data=[query_vector],
        limit=top_k,
        output_fields=["text", "page", "source", "chunk_index"],
    )
    hits = []
    for hit in results[0]:
        hits.append({
            "id": hit["id"],
            "score": hit["distance"],
            "text": hit["entity"]["text"],
            "page": hit["entity"].get("page"),
            "source": hit["entity"].get("source"),
            "chunk_index": hit["entity"].get("chunk_index"),
        })
    return hits
