from __future__ import annotations

import logging

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from mcp_tool_web_search.settings import settings

logger = logging.getLogger(__name__)

KEYWORDS_PROMPT = """你将用户的问题或描述提炼为适合搜索引擎使用的关键词。

要求：
- 根据用户输入提取核心关键词，用空格分隔
- 只输出关键词，不要解释
"""


def extract_keywords(llm: BaseChatModel,query: str) -> str:
    """提取关键词"""
    response = llm.invoke([
        SystemMessage(content=KEYWORDS_PROMPT),
        HumanMessage(content=query),
    ])
    keywords = response.content.strip()
    logger.info(f"用户输入: {query[:50]} -> 搜索关键词: {keywords}")
    return keywords