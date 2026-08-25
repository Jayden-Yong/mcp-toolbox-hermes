import os
from typing import Annotated

import httpx
from mcp.server.mcpserver import MCPServer
from pydantic import Field

LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")


async def get_litellm_model_name(
    model: Annotated[
        str,
        Field(description="The public model name of the current or requested model"),
    ],
) -> list[str]:
    """Get LiteLLM upstream model name using the currently known public model name."""
    params = {"model": model}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{LITELLM_BASE_URL}/v2/model/info",
            headers={"Authorization": f"Bearer {LITELLM_API_KEY}"},
            params=params,
        )
        response.raise_for_status()
        result = response.json()

        return [m["litellm_params"]["model"] for m in result["data"]]


def register(mcp: MCPServer):
    mcp.tool()(get_litellm_model_name)
