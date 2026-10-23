import sqlite3


DB_NAME = "signal.db"


def init_db():
    """Create the articles table if it does not already exist."""
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                source TEXT NOT NULL,
                published_at INTEGER,
                fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_articles(articles):
    """Save articles and return the number of newly inserted rows."""
    inserted_count = 0

    with sqlite3.connect(DB_NAME) as connection:
        for article in articles:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO articles
                    (title, url, source, published_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    article["title"],
                    article["url"],
                    article["source"],
                    article.get("published_at"),
                ),
            )
            inserted_count += cursor.rowcount

    return inserted_count
