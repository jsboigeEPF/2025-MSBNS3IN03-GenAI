"""
Service SearxNG — Enrichissement des rapports avec données web en temps réel
"""
import aiohttp
from config import settings
from typing import Optional


async def search_web(query: str, num_results: int = 5, category: str = "general") -> list[dict]:
    """Recherche sur SearxNG et retourne les résultats."""
    params = {
        "q": query,
        "format": "json",
        "categories": category,
        "language": "fr",
        "safesearch": "1",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.SEARXNG_URL}/search",
                params=params,
                timeout=aiohttp.ClientTimeout(total=8),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    results = data.get("results", [])[:num_results]
                    return [
                        {
                            "title": r.get("title", ""),
                            "url": r.get("url", ""),
                            "content": r.get("content", "")[:300],
                            "published": r.get("publishedDate", ""),
                        }
                        for r in results
                    ]
    except Exception as e:
        print(f"⚠️ SearxNG non disponible: {e}")

    return []


async def build_context_for_report(report_type: str, report_name: str, data: dict) -> str:
    """Construit un contexte enrichi avec des données web récentes."""

    # Construire une requête pertinente selon le type
    queries = {
        "financial": f"analyse financière tendances {report_name} 2024",
        "technical": f"meilleures pratiques DevOps SRE performance système 2024",
        "medical": f"directives cliniques étude {report_name} 2024",
        "generic": f"analyse données rapport {report_name}",
    }

    query = queries.get(report_type, queries["generic"])
    results = await search_web(query, num_results=4)

    if not results:
        return ""

    context_lines = ["### Sources web récentes :\n"]
    for i, r in enumerate(results, 1):
        if r["content"]:
            context_lines.append(f"**{i}. {r['title']}**")
            context_lines.append(f"> {r['content']}")
            if r["published"]:
                context_lines.append(f"*Publié: {r['published']}*")
            context_lines.append("")

    return "\n".join(context_lines)


async def get_market_data(keywords: list[str]) -> str:
    """Recherche des données de marché spécifiques."""
    if not keywords:
        return ""

    query = " ".join(keywords[:3]) + " données marché statistiques"
    results = await search_web(query, num_results=3, category="news")

    if not results:
        return ""

    lines = []
    for r in results:
        if r["content"]:
            lines.append(f"• {r['title']}: {r['content'][:200]}")

    return "\n".join(lines)
