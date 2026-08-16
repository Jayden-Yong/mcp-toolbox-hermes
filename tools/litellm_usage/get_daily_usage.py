import os

import httpx
from mcp.server.mcpserver import MCPServer

# http://litellm:4000
LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")


async def get_daily_usage(current_date: str | None = None) -> dict:
    """Get LiteLLM spend/usage for the current day (YYYY-MM-DD)."""
    params = {}
    if current_date:
        params["current_date"] = current_date

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{LITELLM_BASE_URL}/user/daily/activity",
            headers={"Authorization": f"Bearer {LITELLM_API_KEY}"},
            params=params,
        )
        resp.raise_for_status()
        return resp.json()


def register(mcp: MCPServer):
    mcp.tool()(get_daily_usage)
