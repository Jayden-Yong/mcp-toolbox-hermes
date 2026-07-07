from mcp.server.fastmcp import FastMCP
from tools import register_all
from config import MCP_PORT

mcp = FastMCP("garden-of-memoria")
register_all(mcp)

if __name__ == "__main__":
    mcp.run(transport="sse", port=MCP_PORT)