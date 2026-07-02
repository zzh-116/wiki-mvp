from pymilvus import MilvusClient
from app.core.config import settings

client: MilvusClient | None = None

COLLECTION_NAME = "wiki_chunks"
VECTOR_DIM = 768


def get_client() -> MilvusClient:
    global client
    if client is None:
        client = MilvusClient(host=settings.milvus_host, port=settings.milvus_port)
    return client


def init_milvus():
    mc = get_client()
    if COLLECTION_NAME not in mc.list_collections():
        mc.create_collection(
            collection_name=COLLECTION_NAME,
            dimension=VECTOR_DIM,
            auto_id=True,
            enable_dynamic_field=True,
        )
    return mc
