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
                score INTEGER NOT NULL DEFAULT 0,
                fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(articles)")
        }
        if "score" not in columns:
            connection.execute(
                "ALTER TABLE articles ADD COLUMN score INTEGER NOT NULL DEFAULT 0"
            )


def save_articles(articles):
    """Save articles from any configured source and return new row count."""
    inserted_count = 0

    with sqlite3.connect(DB_NAME) as connection:
        for article in articles:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO articles
                    (title, url, source, published_at, score)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    article["title"],
                    article["url"],
                    article["source"],
                    article.get("published_at"),
                    article.get("score", 0),
                ),
            )
            inserted_count += cursor.rowcount

    return inserted_count


def get_articles():
    """Return all stored articles in dictionary format."""
    with sqlite3.connect(DB_NAME) as connection:
        rows = connection.execute(
            """
            SELECT title, url, source, published_at, score
            FROM articles
            """
        ).fetchall()

    return [
        {
            "title": row[0],
            "url": row[1],
            "source": row[2],
            "published_at": row[3],
            "score": row[4],
        }
        for row in rows
    ]
