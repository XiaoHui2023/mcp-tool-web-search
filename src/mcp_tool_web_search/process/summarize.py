"""summarize 节点 — 使用 LLM 对抓取内容进行精简总结。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import frontmatter
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from mcp_tool_web_search.settings import settings
from mcp_tool_web_search.providers import SearchResult

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
你是一个信息提炼助手。根据用户的问题和搜索到的网页内容，提取与问题最相关的关键信息。

要求：
- 用自然段落输出，不要使用 Markdown 标题、编号列表、分隔线等格式
- 不要标注来源 URL，不要出现"搜索"、"来源"、"参考"等字眼
- 保留关键数据、事实和结论
- 简洁精炼，去除无关内容
- 如果搜索内容无法回答用户问题，明确说明
""".strip()

def summarize(llm: BaseChatModel,query: str,fetched: list[SearchResult]) -> str:
    """总结"""

    if not fetched:
        return "未能获取到搜索内容。"

    parts: list[str] = []
    for item in fetched:
        parts.append(f"日期: {item.published_date}\n\n内容：{item.content}\n")
    combined = "".join(["\n\n---\n\n"+x for x in parts])

    user_content = f"用户问题：{query}\n\n搜索到的内容如下\n\n{combined}"

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ])

    return response.content
