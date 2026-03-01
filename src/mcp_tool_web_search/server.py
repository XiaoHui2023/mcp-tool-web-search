from mcp.server.fastmcp import FastMCP
from mcp_tool_web_search.process import web_search

mcp = FastMCP("mcp-tool-web-search", json_response=True)

@mcp.tool()
def search(query: str, max_results: int = 10) -> str:
    """
    在网络上搜索信息。
    
    Args:
        query: 搜索关键词或问题
        max_results: 返回结果的最大数量
    """
    return web_search(query, max_results=max_results)

def run():
    mcp.run(transport="stdio")