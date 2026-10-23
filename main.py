from db import init_db, save_articles
from fetch import get_all_articles
from ranking import rank_articles


def run_pipeline(n=10):
    """Fetch all configured sources and save new articles."""
    init_db()
    articles = get_all_articles(n)
    ranked_articles = rank_articles(articles)
    return save_articles(ranked_articles)


if __name__ == "__main__":
    inserted_count = run_pipeline()
    print(f"Added {inserted_count} new articles.")
