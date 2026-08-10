from mcp.server.mcpserver import MCPServer
from tools import register_all
from config import MCP_PORT

mcp = MCPServer("garden-of-memoria")
register_all(mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=MCP_PORT)