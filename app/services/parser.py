"""PDF document parser."""

from pathlib import Path

import fitz  # PyMuPDF


def extract_text(pdf_path: str | Path) -> str:
    """Extract all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text_parts: list[str] = []
    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text()
        if page_text.strip():
            text_parts.append(f"--- Page {page_num} ---\n{page_text}")
    doc.close()
    return "\n\n".join(text_parts)


def extract_text_by_page(pdf_path: str | Path) -> list[dict]:
    """Extract text page by page with metadata."""
    doc = fitz.open(pdf_path)
    pages: list[dict] = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            pages.append({"page": page_num, "text": text})
    doc.close()
    return pages
