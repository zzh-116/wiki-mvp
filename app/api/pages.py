from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.wiki import WikiPage
from app.schemas.page import (
    WikiPageCreate,
    WikiPageUpdate,
    WikiPageResponse,
    WikiPageListResponse,
)

router = APIRouter(prefix="/api/pages", tags=["Pages"])


@router.post("", response_model=WikiPageResponse, status_code=201)
async def create_page(body: WikiPageCreate, db: AsyncSession = Depends(get_db)):
    """Create a new wiki page."""
    existing = await db.execute(select(WikiPage).where(WikiPage.title == body.title))
    if existing.scalar_one_or_none():
        raise HTTPException(409, detail=f"Page '{body.title}' already exists")

    page = WikiPage(title=body.title, content=body.content)
    db.add(page)
    await db.commit()
    await db.refresh(page)
    return page


@router.get("", response_model=list[WikiPageListResponse])
async def list_pages(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """List all wiki pages."""
    result = await db.execute(
        select(WikiPage).order_by(WikiPage.updated_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/{page_id}", response_model=WikiPageResponse)
async def get_page(page_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single wiki page by ID."""
    page = await db.get(WikiPage, page_id)
    if not page:
        raise HTTPException(404, detail="Page not found")
    return page


@router.put("/{page_id}", response_model=WikiPageResponse)
async def update_page(
    page_id: int, body: WikiPageUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a wiki page."""
    page = await db.get(WikiPage, page_id)
    if not page:
        raise HTTPException(404, detail="Page not found")

    if body.title is not None:
        existing = await db.execute(
            select(WikiPage).where(WikiPage.title == body.title, WikiPage.id != page_id)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(409, detail=f"Page '{body.title}' already exists")
        page.title = body.title
    if body.content is not None:
        page.content = body.content

    await db.commit()
    await db.refresh(page)
    return page


@router.delete("/{page_id}", status_code=204)
async def delete_page(page_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a wiki page."""
    page = await db.get(WikiPage, page_id)
    if not page:
        raise HTTPException(404, detail="Page not found")
    await db.delete(page)
    await db.commit()
