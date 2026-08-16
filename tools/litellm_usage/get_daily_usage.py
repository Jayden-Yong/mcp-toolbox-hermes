import os
from datetime import UTC, datetime

import httpx
from mcp.server.mcpserver import MCPServer

# http://litellm:4000
LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")


async def get_daily_usage(
    start_date: str | None = None, end_date: str | None = None
) -> dict:
    """Get LiteLLM spend/usage for a date range (YYYY-MM-DD, defaults to today)."""
    if start_date is None or end_date is None:
        today = datetime.now(UTC).date().isoformat()
        start_date = start_date or today
        end_date = end_date or today

    params = {"start_date": start_date, "end_date": end_date}

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
