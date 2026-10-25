from db import get_articles, init_db, save_articles
from fetch import get_all_articles
from ranking import rank_articles
from site_generator import generate_html


def run_pipeline(n=10):
    """Fetch, store, rank, and generate the static site."""
    init_db()
    new_articles = get_all_articles(n)
    inserted_count = save_articles(new_articles)
    stored_articles = get_articles()
    ranked_articles = rank_articles(stored_articles)
    generate_html(ranked_articles)
    return inserted_count


if __name__ == "__main__":
    inserted_count = run_pipeline()
    print(f"Added {inserted_count} new articles and generated index.html.")
