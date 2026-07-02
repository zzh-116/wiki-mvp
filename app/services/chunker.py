"""Document text chunker with configurable overlap."""


def chunk_text(
    text: str,
    chunk_size: int = 512,
    overlap: int = 64,
    page: int | None = None,
    source: str | None = None,
) -> list[dict]:
    """Split text into overlapping chunks.

    Args:
        text: Input text to chunk.
        chunk_size: Max characters per chunk.
        overlap: Overlap characters between adjacent chunks.
        page: Optional page number for metadata.
        source: Optional source filename for metadata.

    Returns:
        List of dicts with 'text', 'page', 'source', 'chunk_index'.
    """
    chunks: list[dict] = []
    start = 0
    index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Try to break at a sentence boundary near the end
        if end < len(text):
            cut = text.rfind("\n", start + chunk_size // 2, end)
            if cut == -1:
                cut = text.rfind(".", start + chunk_size // 2, end)
            if cut == -1:
                cut = text.rfind(" ", start + chunk_size // 2, end)
            if cut != -1:
                end = cut + 1

        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({
                "text": chunk_text,
                "page": page,
                "source": source,
                "chunk_index": index,
            })

        # Advance position (with overlap)
        next_start = end - overlap
        if next_start <= start:
            next_start = end
        start = next_start
        index += 1

    return chunks


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 512,
    overlap: int = 64,
    source: str | None = None,
) -> list[dict]:
    """Chunk text from multiple pages, keeping page metadata."""
    all_chunks: list[dict] = []
    for page in pages:
        chunks = chunk_text(
            text=page["text"],
            chunk_size=chunk_size,
            overlap=overlap,
            page=page.get("page"),
            source=source,
        )
        all_chunks.extend(chunks)
    return all_chunks
