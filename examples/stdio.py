import asyncio
import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def load_mcp_config(config_path: str = "mcp.json") -> dict:
    """加载 mcp.json"""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"找不到 {config_path}，请在项目根目录运行")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_server_config(config: dict, server_name: str = "mcp-tool-web-search") -> dict:
    """从 mcp.json 提取指定服务器配置"""
    servers = config.get("mcpServers", config)
    if server_name not in servers:
        # 若未指定名称，取第一个
        server_name = next(iter(servers)) if servers else None
    if not server_name:
        raise ValueError("mcp.json 中未找到 mcpServers 配置")
    return servers[server_name]


async def test_search(query: str = "Python MCP"):
    """连接 MCP 服务器并调用 search 工具"""
    config = load_mcp_config()
    server_cfg = get_server_config(config)

    command = server_cfg["command"]
    args = server_cfg.get("args", [])
    env = server_cfg.get("env")

    params = StdioServerParameters(command=command, args=args, env=env)

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # 列出工具
            tools_resp = await session.list_tools()
            print("可用工具:", [t.name for t in tools_resp.tools])

            # 调用 search
            result = await session.call_tool("search", {"query": query})

            if getattr(result, "isError", False):
                print("错误:", result.content)
            else:
                for block in result.content:
                    if hasattr(block, "text"):
                        print("搜索结果:\n", block.text)


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "怎么看待AI技术的发展"
    asyncio.run(test_search(query))