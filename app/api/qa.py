"""Q&A API — semantic search + LLM answer."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.embedder import embed_text
from app.services.llm import ask_llm
from app.services.retriever import search_chunks

router = APIRouter(prefix="/api/qa", tags=["Q&A"])


class QARequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")
    top_k: int = Field(5, ge=1, le=20, description="Number of context chunks to retrieve")


class SourceItem(BaseModel):
    id: int
    score: float
    text: str
    page: int | None = None
    source: str | None = None


class QAResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceItem]


@router.post("", response_model=QAResponse)
async def ask_question(body: QARequest):
    """Ask a question and get an answer with source citations."""
    # 1. Embed the question
    query_vec = embed_text(body.question)

    # 2. Search Milvus for relevant chunks
    chunks = search_chunks(query_vec, top_k=body.top_k)
    if not chunks:
        raise HTTPException(404, detail="No relevant documents found")

    # 3. Ask LLM with context
    try:
        answer = await ask_llm(body.question, chunks)
    except Exception as e:
        raise HTTPException(502, detail=f"LLM call failed: {e}")

    return QAResponse(
        question=body.question,
        answer=answer,
        sources=[SourceItem(**c) for c in chunks],
    )
