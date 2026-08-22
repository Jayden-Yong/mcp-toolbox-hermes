from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tools.litellm_usage.get_daily_usage import get_daily_usage, register


@pytest.mark.asyncio
async def test_get_daily_usage_success():
    mock_metadata = {
        "total_spend": 1.23,
        "total_prompt_tokens": 1000,
        "total_completion_tokens": 500,
        "total_tokens": 1500,
        "total_api_requests": 10,
        "total_successful_requests": 9,
        "total_failed_requests": 1,
        "total_cache_read_input_tokens": 800,
        "total_cache_creation_input_tokens": 0,
        "total_compression_saved_tokens": 0,
        "total_compression_savings_spend": 0.0,
        "total_prompt_caching_savings_spend": 0.1,
        "page": 1,
        "total_pages": 1,
        "has_more": False,
    }
    mock_response = {
        "results": [{"date": "2026-08-14", "metrics": {"spend": 1.23}}],
        "metadata": mock_metadata,
    }

    with patch("tools.litellm_usage.get_daily_usage.httpx.AsyncClient") as mock_client:
        instance = mock_client.return_value.__aenter__.return_value
        instance.get = AsyncMock(
            return_value=AsyncMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None,
            )
        )
        result = await get_daily_usage("2026-08-14", "2026-08-14")

    assert result == mock_metadata
    _, kwargs = instance.get.call_args
    assert kwargs["params"] == {"start_date": "2026-08-14", "end_date": "2026-08-14"}


@pytest.mark.asyncio
async def test_get_daily_usage_defaults_to_today():
    mock_metadata = {
        "total_spend": 0.0,
        "total_prompt_tokens": 0,
        "total_completion_tokens": 0,
        "total_tokens": 0,
        "total_api_requests": 0,
        "total_successful_requests": 0,
        "total_failed_requests": 0,
        "total_cache_read_input_tokens": 0,
        "total_cache_creation_input_tokens": 0,
        "total_compression_saved_tokens": 0,
        "total_compression_savings_spend": 0.0,
        "total_prompt_caching_savings_spend": 0.0,
        "page": 1,
        "total_pages": 1,
        "has_more": False,
    }
    mock_response = {"results": [], "metadata": mock_metadata}

    with patch("tools.litellm_usage.get_daily_usage.httpx.AsyncClient") as mock_client:
        instance = mock_client.return_value.__aenter__.return_value
        instance.get = AsyncMock(
            return_value=AsyncMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None,
            )
        )
        result = await get_daily_usage()

    assert result == mock_metadata
    _, kwargs = instance.get.call_args
    assert kwargs["params"]["start_date"] == datetime.now(UTC).date().isoformat()
    assert kwargs["params"]["end_date"] == datetime.now(UTC).date().isoformat()


@pytest.mark.asyncio
async def test_register():
    mock_mcp = MagicMock()
    register(mock_mcp)
    mock_mcp.tool.assert_called_once()
    mock_mcp.tool.return_value.assert_called_once_with(get_daily_usage)