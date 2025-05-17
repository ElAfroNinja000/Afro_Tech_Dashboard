import re
import feedparser

TOPICS = {
    "AI": ["https://www.technologyreview.com/feed/",
           "https://feeds.feedburner.com/blogspot/gJZg"],
    "3D Graphics": ["https://3dtotal.com/rss",
                    "https://theinspirationgrid.com/feed/",
                    "https://motionographer.com/feed/"],
    "Data Engineering": ["https://towardsdatascience.com/feed"]
}

def fetch_articles():
    articles = []
    for topic, urls in TOPICS.items():
        for url in urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                image_url = "https://images.pexels.com/photos/844297/pexels-photo-844297.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
                if "media_thumbnail" in entry:
                    image_url = entry.media_thumbnail[0].get("url")
                elif "media_content" in entry:
                    image_url = entry.media_content[0].get("url")
                elif "summary" in entry and "<img" in entry.summary:
                    match = re.search(r'<img[^>]+src="([^">]+)"', entry.summary)
                    if match:
                        image_url = match.group(1)

                article = {
                    "topic": topic,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", ""),
                    "image": image_url
                }
                print(article)
                articles.append(article)
    return articles



if __name__ == "__main__":
    fetch_articles()