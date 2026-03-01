from __future__ import annotations
import logging
from mcp_tool_web_search.providers import SearchResult,resolve_provider

logger = logging.getLogger(__name__)


def search_urls(query: str, max_results: int) -> list[SearchResult]:
    """搜索 URL"""

    provider = resolve_provider()
    logger.info(f"搜索: {query} (provider={provider.name})")
    results = provider.search(query, max_results=max_results)
    logger.info(f"获取到 {len(results)} 条搜索结果")

    return results