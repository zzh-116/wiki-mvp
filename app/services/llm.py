"""LLM client — OpenAI-compatible chat completions.

Configurable via .env:
  LLM_API_BASE=https://api.openai.com/v1
  LLM_API_KEY=sk-...
  LLM_MODEL=gpt-4o
"""

from httpx import AsyncClient, Timeout
from pydantic import BaseModel

from app.core.config import settings


class LLMConfig(BaseModel):
    api_base: str = "https://api.openai.com/v1"
    api_key: str = ""
    model: str = "gpt-4o"
    temperature: float = 0.1
    max_tokens: int = 2048


def get_llm_config() -> LLMConfig:
    return LLMConfig(
        api_base=settings.llm_api_base,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )


SYSTEM_PROMPT = """你是一个基于知识库的问答助手。请根据提供的参考材料回答问题。

规则：
1. 只基于参考材料回答问题，不要编造信息
2. 如果参考材料不足以回答问题，请明确说明
3. 引用来源时标注页码（如适用）
4. 用中文回答
"""


async def ask_llm(
    question: str,
    context_chunks: list[dict],
    llm_config: LLMConfig | None = None,
) -> str:
    """Send question + context chunks to LLM and return answer."""
    cfg = llm_config or get_llm_config()

    # Build context text from chunks
    context_parts = []
    for i, chunk in enumerate(context_chunks):
        source = chunk.get("source", "unknown")
        page = chunk.get("page")
        page_info = f" (第 {page} 页)" if page else ""
        context_parts.append(f"[来源 {i+1}]{page_info}: {chunk['text']}")
    context_text = "\n\n".join(context_parts)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"参考材料：\n{context_text}\n\n问题：{question}"},
    ]

    async with AsyncClient(timeout=Timeout(60.0)) as client:
        resp = await client.post(
            f"{cfg.api_base.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {cfg.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": cfg.model,
                "messages": messages,
                "temperature": cfg.temperature,
                "max_tokens": cfg.max_tokens,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
