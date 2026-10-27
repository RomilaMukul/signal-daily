import calendar
import logging

import feedparser
import requests

BASE = "https://hacker-news.firebaseio.com/v0"
logger = logging.getLogger(__name__)


RSS_FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
}


def _classify_failure(error):
    """Return a stable failure type string for reports/logging."""
    if isinstance(error, requests.Timeout):
        return "timeout"
    if isinstance(error, requests.HTTPError):
        return "http_error"
    if isinstance(error, requests.ConnectionError):
        return "connection_error"
    if isinstance(error, requests.RequestException):
        return "request_error"
    if isinstance(error, ValueError):
        return "data_error"
    return "unknown_error"


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
    """Fetch all sources and return only articles (legacy behavior)."""
    articles, _failure_report = get_all_articles_with_report(n)
    return articles


def get_all_articles_with_report(n=10):
    """Fetch all sources and return (articles, failure_report)."""
    articles = []
    successful_sources = 0
    failure_report = []

    try:
        source_articles = get_top_stories(n)
        articles.extend(source_articles)
        successful_sources += 1
        failure_report.append({
            "source": "Hacker News",
            "status": "ok",
            "article_count": len(source_articles),
            "failure_type": None,
            "error": None,
        })
    except (requests.RequestException, ValueError) as error:
        failure_type = _classify_failure(error)
        logger.warning("Hacker News failed (%s): %s", failure_type, error)
        failure_report.append({
            "source": "Hacker News",
            "status": "failed",
            "article_count": 0,
            "failure_type": failure_type,
            "error": str(error),
        })

    for source, feed_url in RSS_FEEDS.items():
        try:
            source_articles = get_rss_articles(feed_url, source)
            articles.extend(source_articles)
            successful_sources += 1
            failure_report.append({
                "source": source,
                "status": "ok",
                "article_count": len(source_articles),
                "failure_type": None,
                "error": None,
            })
        except (requests.RequestException, ValueError) as error:
            failure_type = _classify_failure(error)
            logger.warning("%s failed (%s): %s", source, failure_type, error)
            failure_report.append({
                "source": source,
                "status": "failed",
                "article_count": 0,
                "failure_type": failure_type,
                "error": str(error),
            })

    if successful_sources == 0:
        raise RuntimeError("All news sources failed")

    return articles, failure_report


if __name__ == "__main__":
    fetched_articles, report = get_all_articles_with_report()
    for s in fetched_articles:
        print(s["title"], "|", s.get("url", "no url"))
    print("\nSource status:")
    for source_result in report:
        print(source_result)