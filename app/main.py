from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import pages, qa, upload
from app.core.config import settings
from app.core.database import init_db
from app.core.milvus import init_milvus


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    try:
        init_milvus()
        print("  [Milvus] Connected")
    except Exception as e:
        print(f"  [Milvus] Not available ({e}) — skipping")
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(pages.router)
app.include_router(upload.router)
app.include_router(qa.router)


@app.get("/")
async def root():
    return {"message": f"{settings.app_name} is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
