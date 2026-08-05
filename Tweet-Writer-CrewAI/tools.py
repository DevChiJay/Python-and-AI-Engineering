from crewai.tools import BaseTool
from ddgs import DDGS


class DuckDuckGoTool(BaseTool):
    name: str = "DuckDuckGo Search"
    description: str = "Search the web for recent information about a topic."

    def _run(self, query: str) -> str:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
        return "\n".join(f"{r['title']}: {r['body']}" for r in results)


duckduckgo_search = DuckDuckGoTool()