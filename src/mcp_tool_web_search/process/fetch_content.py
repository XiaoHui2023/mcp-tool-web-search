from __future__ import annotations
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from mcp_tool_web_search.providers import SearchResult
from dataclasses import replace

logger = logging.getLogger(__name__)

def _scrape_url(url: str, timeout: int) -> str | None:
    """爬取 URL 并返回 HTML 内容。三种方式并行，谁先成功用谁。"""

    try:
        from curl_cffi import requests
        resp = requests.get(url, impersonate="chrome120", timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception:
        logger.warning(f"爬取 {url} 失败")
        return None

def _fetch_one(url: str, timeout: int) -> str | None:
    """抓取单个 URL 并提取正文为 Markdown。失败返回 None。"""
    try:
        from trafilatura import extract

        html = _scrape_url(url, timeout)
        if not html:
            return None

        markdown = extract(html, output_format="markdown")
        if not markdown:
            return None

        return markdown
    except Exception as e:
        logger.warning(f"抓取失败 {url}: {e}")
        return None


def fetch_content(results: list[SearchResult], timeout: int, max_workers: int, max_chars: int) -> list[SearchResult]:
    """抓取内容"""

    if not results:
        return []
    fetched: list[str] = []

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_fetch_one, result.url, timeout): result
            for result in results
        }
        try:
            for future in as_completed(futures, timeout=timeout + 5):
                content = future.result()
                result = futures[future]
                if content:
                    new_result = replace(result, content=content[:max_chars])
                    fetched.append(new_result)
        except TimeoutError:
            logger.warning(f"全局抓取超时，已获取 {len(fetched)} 页")

    logger.info(f"成功抓取 {len(fetched)}/{len(results)} 页")
    return fetched