from mcp.server.fastmcp import FastMCP

# 导入你的搜索函数
from mcp_web_search.search import web_search

mcp = FastMCP("mcp-web-search", json_response=True)

@mcp.tool()
def search(query: str, max_results: int = 5) -> str:
    """
    在网络上搜索信息。
    
    Args:
        query: 搜索关键词或问题
        max_results: 返回结果的最大数量，默认 5
    """
    return web_search(query, max_results=max_results)

def run():
    mcp.run(transport="stdio")  # 默认 stdio，适合 Cursor/Claude Desktop