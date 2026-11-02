import sqlite3
from contextlib import closing

from url_utils import normalize_url


DB_NAME = "signal.db"

ARTICLE_COLUMNS = {
    "description": "TEXT",
    "summary": "TEXT",
    "topics": "TEXT",
    "content_hash": "TEXT",
    "cluster_id": "INTEGER",
    "processed_at": "TEXT",
}


def init_db():
    """Create the articles table if it does not already exist."""
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    source TEXT NOT NULL,
                    published_at INTEGER,
                    score INTEGER NOT NULL DEFAULT 0,
                    description TEXT,
                    summary TEXT,
                    topics TEXT,
                    content_hash TEXT,
                    cluster_id INTEGER,
                    processed_at TEXT,
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
            for column_name, column_type in ARTICLE_COLUMNS.items():
                if column_name not in columns:
                    connection.execute(
                        f"ALTER TABLE articles ADD COLUMN {column_name} {column_type}"
                    )


def save_articles(articles):
    """Save articles from any configured source and return new row count."""
    inserted_count = 0

    with closing(sqlite3.connect(DB_NAME)) as connection:
        with connection:
            for article in articles:
                normalized_url = normalize_url(article["url"])
                cursor = connection.execute(
                    """
                    INSERT OR IGNORE INTO articles
                        (title, url, source, published_at, score, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        article["title"],
                        normalized_url,
                        article["source"],
                        article.get("published_at"),
                        article.get("score", 0),
                        article.get("description"),
                    ),
                )
                inserted_count += cursor.rowcount

    return inserted_count


def get_articles():
    """Return all stored articles in dictionary format."""
    with closing(sqlite3.connect(DB_NAME)) as connection:
        rows = connection.execute(
            """
            SELECT title, url, source, published_at, score
                , description, summary, topics, content_hash, cluster_id, processed_at
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
            "description": row[5],
            "summary": row[6],
            "topics": row[7],
            "content_hash": row[8],
            "cluster_id": row[9],
            "processed_at": row[10],
        }
        for row in rows
    ]
