from unittest.mock import MagicMock, patch

from tools.reddit_search import register


def _registered_search_reddit():
    mock_mcp = MagicMock()
    register(mock_mcp)
    return mock_mcp.tool.return_value.call_args[0][0]


def test_search_reddit_success():
    search_reddit = _registered_search_reddit()
    mock_response = {
        "data": {
            "children": [
                {
                    "data": {
                        "title": "Hello MCP",
                        "subreddit": "ModelContextProtocol",
                        "ups": 42,
                        "url": "https://reddit.com/r/ModelContextProtocol/1",
                        "selftext": "Body text here",
                    }
                }
            ]
        }
    }

    with patch("tools.reddit_search.httpx.get") as mock_get:
        mock_get.return_value = MagicMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None,
        )
        result = search_reddit("mcp")

    assert "Hello MCP" in result
    assert "r/ModelContextProtocol" in result


def test_search_reddit_no_results():
    search_reddit = _registered_search_reddit()

    with patch("tools.reddit_search.httpx.get") as mock_get:
        mock_get.return_value = MagicMock(
            json=lambda: {"data": {"children": []}},
            raise_for_status=lambda: None,
        )
        result = search_reddit("nonexistent-thing-xyz")

    assert result == "No results found."


def test_register():
    mock_mcp = MagicMock()
    register(mock_mcp)
    mock_mcp.tool.assert_called_once()
    mock_mcp.tool.return_value.assert_called_once()
