from mcp.server.fastmcp import FastMCP
from tools import register_all
from config import MCP_PORT

mcp = FastMCP("garden-of-memoria", host="0.0.0.0", port=MCP_PORT)
register_all(mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")