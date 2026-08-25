from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from tools.litellm_usage.get_litellm_model_name import (
    LITELLM_API_KEY,
    get_litellm_model_name,
    register,
)


@pytest.mark.asyncio
async def test_get_litellm_model_name_success():
    mock_response = {
        "data": [
            {
                "model_name": "gpt-4o",
                "litellm_params": {"model": "openai/gpt-4o-2024-11-20"},
                "model_info": {"id": "dep-1"},
            }
        ],
        "total_count": 1,
        "total_pages": 1,
    }

    with patch(
        "tools.litellm_usage.get_litellm_model_name.httpx.AsyncClient"
    ) as mock_client:
        instance = mock_client.return_value.__aenter__.return_value
        instance.get = AsyncMock(
            return_value=AsyncMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None,
            )
        )
        result = await get_litellm_model_name("gpt-4o")

    assert result == ["openai/gpt-4o-2024-11-20"]
    args, kwargs = instance.get.call_args
    assert args[0].endswith("/v2/model/info")
    assert kwargs["headers"] == {"Authorization": f"Bearer {LITELLM_API_KEY}"}
    assert kwargs["params"] == {"model": "gpt-4o"}


@pytest.mark.asyncio
async def test_get_litellm_model_name_multiple_deployments():
    mock_response = {
        "data": [
            {
                "model_name": "gpt-4o",
                "litellm_params": {"model": "openai/gpt-4o-2024-11-20"},
            },
            {
                "model_name": "gpt-4o",
                "litellm_params": {"model": "azure/gpt-4o-fallback"},
            },
        ],
        "total_count": 2,
        "total_pages": 1,
    }

    with patch(
        "tools.litellm_usage.get_litellm_model_name.httpx.AsyncClient"
    ) as mock_client:
        instance = mock_client.return_value.__aenter__.return_value
        instance.get = AsyncMock(
            return_value=AsyncMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None,
            )
        )
        result = await get_litellm_model_name("gpt-4o")

    assert result == ["openai/gpt-4o-2024-11-20", "azure/gpt-4o-fallback"]


@pytest.mark.asyncio
async def test_get_litellm_model_name_no_matches():
    mock_response = {"data": [], "total_count": 0, "total_pages": 0}

    with patch(
        "tools.litellm_usage.get_litellm_model_name.httpx.AsyncClient"
    ) as mock_client:
        instance = mock_client.return_value.__aenter__.return_value
        instance.get = AsyncMock(
            return_value=AsyncMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None,
            )
        )
        result = await get_litellm_model_name("nonexistent-model")

    assert result == []


@pytest.mark.asyncio
async def test_get_litellm_model_name_http_error_propagates():
    error = httpx.HTTPStatusError(
        "404 Not Found",
        request=httpx.Request("GET", "/v2/model/info"),
        response=httpx.Response(404),
    )

    with patch(
        "tools.litellm_usage.get_litellm_model_name.httpx.AsyncClient"
    ) as mock_client:
        instance = mock_client.return_value.__aenter__.return_value
        error_response = MagicMock()
        error_response.raise_for_status.side_effect = error
        instance.get = AsyncMock(return_value=error_response)

        with pytest.raises(httpx.HTTPStatusError):
            await get_litellm_model_name("nonexistent-model")


def test_register():
    mock_mcp = MagicMock()
    register(mock_mcp)
    mock_mcp.tool.assert_called_once()
    mock_mcp.tool.return_value.assert_called_once_with(get_litellm_model_name)
