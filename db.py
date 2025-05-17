import sqlite3
import os

def init_db():
    os.makedirs("data", exist_ok=True)  # ← crée le dossier s'il n'existe pas
    conn = sqlite3.connect("data/feeds.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        title TEXT,
        link TEXT UNIQUE,
        published TEXT,
        image TEXT
    )''')
    conn.commit()
    conn.close()


def save_articles(articles):
    conn = sqlite3.connect("data/feeds.db")
    c = conn.cursor()
    for article in articles:
        try:
            c.execute("INSERT INTO articles (topic, title, link, published, image) VALUES (?, ?, ?, ?, ?)",
                      (article["topic"], article["title"], article["link"], article["published"], article["image"]))

        except sqlite3.IntegrityError:
            continue
    conn.commit()
    conn.close()

def get_articles_by_topic():
    conn = sqlite3.connect("data/feeds.db")
    c = conn.cursor()
    c.execute("SELECT topic, title, link, published, image FROM articles ORDER BY published DESC")
    rows = c.fetchall()
    conn.close()

    grouped = {}
    for topic, title, link, published, image in rows:
        grouped.setdefault(topic, []).append((topic, title, link, published, image))
    return grouped
