from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 6):
    """Recherche web via DuckDuckGo."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results, safesearch="moderate"):
            results.append({
                "title": r.get("title", ""),
                "href": r.get("href", ""),
                "body": r.get("body", "")
            })
    return results