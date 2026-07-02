"""PDF upload & parse API."""

import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form

from app.core.config import settings
from app.services.chunker import chunk_pages
from app.services.embedder import embed_batch
from app.services.parser import extract_text_by_page
from app.services.retriever import ensure_collection, insert_chunks

router = APIRouter(prefix="/api/upload", tags=["Upload"])


@router.post("")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF, extract text, chunk, embed, and index into Milvus."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, detail="Only PDF files are supported")

    # Save uploaded file
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    save_path = upload_dir / file.filename

    with save_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    # Extract text
    pages = extract_text_by_page(save_path)
    if not pages:
        raise HTTPException(400, detail="No text could be extracted from the PDF")

    # Chunk
    chunks = chunk_pages(pages, chunk_size=512, overlap=64, source=file.filename)
    if not chunks:
        raise HTTPException(400, detail="No chunks generated from the PDF")

    # Embed
    texts = [c["text"] for c in chunks]
    embeddings = embed_batch(texts)

    # Index into Milvus
    ensure_collection()
    ids = insert_chunks(chunks, embeddings)

    return {
        "filename": file.filename,
        "pages": len(pages),
        "chunks": len(chunks),
        "indexed_ids": ids,
    }
