from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tools.litellm_usage.get_daily_usage import get_daily_usage, register


@pytest.mark.asyncio
async def test_get_daily_usage_success():
    mock_response = {"results": [{"date": "2026-08-14", "spend": 1.23}]}

    with patch("tools.litellm_usage.get_daily_usage.httpx.AsyncClient") as mock_client:
        instance = mock_client.return_value.__aenter__.return_value
        instance.get = AsyncMock(
            return_value=AsyncMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None,
            )
        )
        result = await get_daily_usage("2026-08-14", "2026-08-14")

    assert result == mock_response
    _, kwargs = instance.get.call_args
    assert kwargs["params"] == {"start_date": "2026-08-14", "end_date": "2026-08-14"}


@pytest.mark.asyncio
async def test_get_daily_usage_defaults_to_today():
    mock_response = {"results": []}

    with patch("tools.litellm_usage.get_daily_usage.httpx.AsyncClient") as mock_client:
        instance = mock_client.return_value.__aenter__.return_value
        instance.get = AsyncMock(
            return_value=AsyncMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None,
            )
        )
        result = await get_daily_usage()

    assert result == mock_response
    _, kwargs = instance.get.call_args
    assert kwargs["params"]["start_date"] == datetime.now(UTC).date().isoformat()
    assert kwargs["params"]["end_date"] == datetime.now(UTC).date().isoformat()


@pytest.mark.asyncio
async def test_register():
    mock_mcp = MagicMock()
    register(mock_mcp)
    mock_mcp.tool.assert_called_once()
    mock_mcp.tool.return_value.assert_called_once_with(get_daily_usage)
