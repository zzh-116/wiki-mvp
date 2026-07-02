from datetime import datetime
from pydantic import BaseModel, Field


class WikiPageCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Page title")
    content: str = Field(default="", description="Page content in markdown")


class WikiPageUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255, description="New title")
    content: str | None = Field(default=None, description="New content")


class WikiPageResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WikiPageListResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
