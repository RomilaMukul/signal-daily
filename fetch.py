import calendar

import feedparser
import requests

BASE = "https://hacker-news.firebaseio.com/v0"


RSS_FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
}


def get_top_stories(n=10):
    ids = requests.get(f"{BASE}/topstories.json", timeout=10).json()[:n]
    stories = []
    for i in ids:
        item = requests.get(f"{BASE}/item/{i}.json", timeout=10).json()
        if item and "title" in item:
            stories.append({
                "title": item["title"],
                "url": item.get("url", f"https://news.ycombinator.com/item?id={i}"),
                "source": "Hacker News",
                "published_at": item.get("time"),
                "score": item.get("score", 0),
            })
    return stories


def get_rss_articles(feed_url, source):
    """Fetch one RSS feed and return articles in our standard format."""
    response = requests.get(feed_url, timeout=10)
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    articles = []

    for entry in feed.entries:
        if not entry.get("title") or not entry.get("link"):
            continue

        published_at = None
        if entry.get("published_parsed"):
            published_at = calendar.timegm(entry.published_parsed)
        elif entry.get("updated_parsed"):
            published_at = calendar.timegm(entry.updated_parsed)

        articles.append({
            "title": entry["title"],
            "url": entry["link"],
            "source": source,
            "published_at": published_at,
            "score": 0,
        })

    return articles


def get_all_articles(n=10):
    """Fetch Hacker News, technology, and finance articles."""
    articles = get_top_stories(n)

    for source, feed_url in RSS_FEEDS.items():
        articles.extend(get_rss_articles(feed_url, source))

    return articles


if __name__ == "__main__":
    for s in get_all_articles():
        print(s["title"], "|", s.get("url", "no url"))