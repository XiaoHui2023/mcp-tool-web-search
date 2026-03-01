from __future__ import annotations

import logging

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from mcp_tool_web_search.providers import resolve_provider
from mcp_tool_web_search.settings import settings

from .extract_keywords import extract_keywords
from .fetch_content import fetch_content
from .search_urls import search_urls
from .summarize import summarize

logger = logging.getLogger(__name__)

def web_search(
    query: str,
    max_results: int = 10,
    timeout: int = 3,
    max_workers: int = 10,
    max_chars: int = 10000,
) -> str:
    """
    执行完整搜索流程：关键词提取 → 搜索 URL → 抓取内容 → LLM 总结。

    Args:
        query: 用户问题或搜索关键词
        max_results: 搜索结果数量
        timeout: 单页抓取超时（秒）
        max_workers: 最大并发抓取数
        max_chars: 最大抓取字符数

    Returns:
        总结后的文本，失败时返回提示信息
    """
    logger.info(f"[run] 使用模型: {settings.llm_model}")
    llm = ChatOpenAI(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        temperature=0,
        streaming=False,
    )

    keywords = extract_keywords(llm, query)
    results = search_urls(keywords, max_results=max_results)
    fetched = fetch_content(results, timeout=timeout, max_workers=max_workers, max_chars=max_chars)
    summary = summarize(llm, query, fetched)
    
    return summary

__all__ = [
    "web_search",
]