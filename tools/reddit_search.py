# tools/reddit_search.py
import httpx
from mcp.server.mcpserver import MCPServer

def register(mcp: MCPServer):
    @mcp.tool()
    def search_reddit(query: str, subreddit: str = "") -> str:
        """Search Reddit posts. Use this instead of web_search for Reddit-specific queries since Firecrawl gets blocked on Reddit."""
        if subreddit:
            url = f"https://www.reddit.com/r/{subreddit}/search.json"
            params = {"q": query, "restrict_sr": "true", "limit": 10, "sort": "relevance"}
        else:
            url = "https://www.reddit.com/search.json"
            params = {"q": query, "limit": 10, "sort": "relevance"}

        headers = {"User-Agent": "hermes-jayden-toolbox/1.0"}
        r = httpx.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()

        results = []
        for post in data.get("data", {}).get("children", []):
            p = post["data"]
            results.append(f"**{p['title']}** (r/{p['subreddit']}, {p['ups']} upvotes)\n{p['url']}\n{p.get('selftext', '')[:300]}")

        return "\n\n".join(results) if results else "No results found."