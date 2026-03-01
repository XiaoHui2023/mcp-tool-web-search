from mcp_tool_web_search import web_search, setup_logging

if __name__ == "__main__":
    query = "怎么看待AI技术的发展"
    setup_logging()
    print(web_search(query))