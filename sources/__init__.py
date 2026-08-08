"""Point d'entrée unique pour récupérer les articles de toutes les sources."""
from tags import generate_tags, is_ai_related

from . import rss, hackernews

FETCHERS = [rss.fetch, hackernews.fetch]

# quand le titre/résumé ne matche aucun mot-clé (sources au contenu peu
# descriptif, ex. portfolios visuels), on retombe sur un tag propre à la source
# plutôt que de laisser l'article sans aucun tag.
SOURCE_FALLBACK_TAG = {
    "Motionographer": "3D / Graphics",
    "Real Python": "Python",
    "Awwwards": "Design",
    "Codrops": "Design",
    "Abduzeedo": "Design",
    "Designboom": "Design",
    "80 Level": "3D / Graphics",
    "CG Channel": "3D / Graphics",
}


def fetch_all_articles() -> list[dict]:
    articles = []
    for fetch in FETCHERS:
        articles.extend(fetch())

    kept = []
    for article in articles:
        article.setdefault("extra", "")
        article.setdefault("image", None)
        text = f"{article['title']} {article.get('summary', '')}"

        if is_ai_related(text):
            continue  # AI/GenAI content is excluded from this dashboard entirely

        tags = generate_tags(text)
        if not tags:
            fallback = SOURCE_FALLBACK_TAG.get(article["source"])
            if fallback:
                tags = [fallback]
        article["tags"] = tags
        kept.append(article)

    return kept
