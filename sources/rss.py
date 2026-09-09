"""Flux RSS / Atom classiques (blogs + Real Python)."""
import re
import feedparser

from ._common import to_iso

# nom affiché (= "source") -> URL du flux
# (l'ex-"Blogger AI", le blog IA de Google, a été retiré : son contenu est
# quasi exclusivement lié à l'IA et serait filtré en quasi-totalité, cf.
# sources/__init__.py::is_ai_related)
RSS_FEEDS = {
    "MIT Technology Review": "https://www.technologyreview.com/feed/",
    "Motionographer": "https://motionographer.com/feed/",
    "Towards Data Science": "https://towardsdatascience.com/feed",
    "Real Python": "https://realpython.com/atom.xml",
    # security / infra
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
    "The Hacker News (security)": "https://feeds.feedburner.com/TheHackersNews",
    "The New Stack": "https://thenewstack.io/feed/",
    # dev community / web
    "Lobsters": "https://lobste.rs/rss",
    "Dev.to": "https://dev.to/feed",
    "Smashing Magazine": "https://www.smashingmagazine.com/feed/",
    "GitHub Blog": "https://github.blog/feed/",
    # design / creative
    "Awwwards": "https://www.awwwards.com/blog/feed/",
    "Codrops": "https://tympanus.net/codrops/feed/",
    "Abduzeedo": "https://abduzeedo.com/rss.xml",
    "Designboom": "https://www.designboom.com/feed/",
    # 3D / CGI / VFX
    "80 Level": "https://80.lv/feed/",
    "CG Channel": "https://www.cgchannel.com/feed/",
}


def _extract_image(entry):
    if "media_thumbnail" in entry:
        return entry.media_thumbnail[0].get("url")
    if "media_content" in entry:
        return entry.media_content[0].get("url")
    summary = entry.get("summary", "")
    if "<img" in summary:
        match = re.search(r'<img[^>]+src="([^">]+)"', summary)
        if match:
            return match.group(1)
    return None


def _clean_summary(entry):
    summary = entry.get("summary", "") or ""
    return re.sub(r"<[^>]+>", "", summary).strip()[:400]


def fetch(limit_per_feed: int = 5) -> list[dict]:
    articles = []
    for source_name, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit_per_feed]:
                articles.append({
                    "source": source_name,
                    "title": entry.get("title", "(sans titre)"),
                    "link": entry.get("link"),
                    "published": to_iso(struct_time_or_dt=entry.get("published_parsed") or entry.get("updated_parsed")),
                    "image": _extract_image(entry),
                    "summary": _clean_summary(entry),
                    "popularity": 0,
                })
        except Exception as exc:
            print(f"[rss] échec {source_name}: {exc}")
    return articles
