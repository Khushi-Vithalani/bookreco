import requests
from typing import Any, Dict, List

BASE = "https://openlibrary.org/search.json"

def search_openlibrary(query: str, limit: int = 200) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    page = 1

    while len(results) < limit:
        r = requests.get(BASE, params={"q": query, "page": page}, timeout=20)
        r.raise_for_status()
        data = r.json()
        docs = data.get("docs", [])
        if not docs:
            break
        results.extend(docs)
        page += 1

    return results[:limit]