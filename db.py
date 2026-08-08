import os
import sqlite3

DB_PATH = "data/feeds.db"

SCHEMA_COLUMNS = {"id", "source", "title", "link", "published", "image", "summary", "tags", "popularity", "extra"}


def _connect():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = _connect()
    c = conn.cursor()

    # migration légère : si une ancienne version de la table existe (schéma
    # "topic" d'avant la refonte), on la recrée — ce n'est qu'un cache RSS
    # reconstruit via "Refresh Feeds", aucune perte de données réelle.
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles'")
    if c.fetchone():
        existing_cols = {row[1] for row in c.execute("PRAGMA table_info(articles)")}
        if not SCHEMA_COLUMNS.issubset(existing_cols):
            c.execute("DROP TABLE articles")

    c.execute('''CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        title TEXT,
        link TEXT UNIQUE,
        published TEXT,
        image TEXT,
        summary TEXT,
        tags TEXT,
        popularity INTEGER DEFAULT 0,
        extra TEXT
    )''')
    conn.commit()
    conn.close()


def save_articles(articles: list[dict]) -> int:
    conn = _connect()
    c = conn.cursor()
    inserted = 0
    for a in articles:
        try:
            c.execute(
                """INSERT INTO articles (source, title, link, published, image, summary, tags, popularity, extra)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    a.get("source"),
                    a.get("title"),
                    a.get("link"),
                    a.get("published"),
                    a.get("image"),
                    a.get("summary", ""),
                    f",{','.join(a.get('tags', []))}," if a.get("tags") else "",
                    a.get("popularity", 0),
                    a.get("extra", ""),
                ),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            continue  # déjà en base (lien déjà vu)
    conn.commit()
    conn.close()
    return inserted


def get_articles(search: str = "", tags: list[str] | None = None, sort: str = "recent") -> list[dict]:
    conn = _connect()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    clauses, params = [], []

    if search:
        clauses.append("(title LIKE ? OR summary LIKE ? OR tags LIKE ? OR source LIKE ?)")
        needle = f"%{search}%"
        params += [needle, needle, needle, needle]

    if tags:
        clauses.append(" AND ".join(["tags LIKE ?"] * len(tags)))
        params += [f"%,{t},%" for t in tags]

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    order = "popularity DESC, published DESC" if sort == "popularity" else "published DESC"

    c.execute(f"SELECT * FROM articles {where} ORDER BY {order}", params)
    rows = [dict(row) for row in c.fetchall()]
    conn.close()

    for row in rows:
        row["tags"] = [t for t in row["tags"].split(",") if t]
    return rows


def get_all_tags() -> list[str]:
    """Retourne les tags distincts présents en base, pour peupler le filtre."""
    conn = _connect()
    c = conn.cursor()
    tag_set = set()
    for (tags_str,) in c.execute("SELECT tags FROM articles WHERE tags != ''"):
        tag_set.update(t for t in tags_str.split(",") if t)
    conn.close()
    return sorted(tag_set)
