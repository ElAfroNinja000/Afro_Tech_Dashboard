"""Hacker News — page d'accueil via l'API publique Algolia (1 seul appel HTTP,
inclut déjà le score et le nombre de commentaires, donc pas besoin d'interroger
l'API Firebase item par item)."""
import requests

from ._common import to_iso

API_URL = "https://hn.algolia.com/api/v1/search"
SOURCE_NAME = "Hacker News"


def fetch(limit: int = 25) -> list[dict]:
    try:
        resp = requests.get(
            API_URL,
            params={"tags": "front_page", "hitsPerPage": limit},
            timeout=10,
        )
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
    except Exception as exc:
        print(f"[hackernews] échec: {exc}")
        return []

    articles = []
    for hit in hits:
        object_id = hit.get("objectID")
        title = hit.get("title") or hit.get("story_title")
        if not title:
            continue
        link = hit.get("url") or hit.get("story_url") or f"https://news.ycombinator.com/item?id={object_id}"
        articles.append({
            "source": SOURCE_NAME,
            "title": title,
            "link": link,
            "published": to_iso(iso_string=hit.get("created_at")),
            "image": None,
            "summary": (hit.get("story_text") or hit.get("comment_text") or "")[:400],
            "popularity": hit.get("points") or 0,
            "extra": f"{hit.get('num_comments') or 0} comments",
        })
    return articles
