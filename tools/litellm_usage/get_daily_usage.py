import os
from datetime import UTC, datetime
from typing import Annotated

import httpx
from mcp.server.mcpserver import MCPServer
from pydantic import Field

# http://litellm:4000
LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")


async def get_daily_usage(
    start_date: Annotated[
        str | None,
        Field(
            description="Start date inclusive, YYYY-MM-DD. Defaults to today UTC if omitted. Example: 2026-08-23"
        ),
    ] = None,
    end_date: Annotated[
        str | None,
        Field(
            description="End date inclusive, YYYY-MM-DD. Defaults to same as start_date. Must be >= start_date"
        ),
    ] = None,
    model: Annotated[
        str | None,
        Field(
            description="Internal LiteLLM model name filter. Example: deepseek/deepseek-v4-flash | openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"
        ),
    ] = None,
) -> dict:
    """Get LiteLLM spend/usage for a date range (YYYY-MM-DD, defaults to today), filterable by LiteLLM model name."""
    if start_date is None or end_date is None:
        today = datetime.now(UTC).date().isoformat()
        start_date = start_date or today
        end_date = end_date or today

    params = {
        k: v
        for k, v in {
            "start_date": start_date,
            "end_date": end_date,
            "model": model,
        }.items()
        if v is not None
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{LITELLM_BASE_URL}/user/daily/activity/aggregated",
            headers={"Authorization": f"Bearer {LITELLM_API_KEY}"},
            params=params,
        )
        resp.raise_for_status()
        results = resp.json()

        return results["metadata"]


def register(mcp: MCPServer):
    mcp.tool()(get_daily_usage)
