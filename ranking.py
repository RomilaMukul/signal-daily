import time


MAX_POPULARITY_SCORE = 100


def calculate_freshness_score(published_at, current_time=None):
    """Return freshness points based on the article age in hours."""
    if published_at is None:
        return 0

    if current_time is None:
        current_time = time.time()

    age_hours = max(0, (current_time - published_at) / 3600)

    if age_hours < 6:
        return 100
    if age_hours < 12:
        return 80
    if age_hours < 24:
        return 60
    if age_hours < 48:
        return 40
    if age_hours < 72:
        return 20
    return 0


def calculate_popularity_score(score):
    """Return a capped popularity score."""
    return min(score or 0, MAX_POPULARITY_SCORE)


def calculate_ranking_score(article, current_time=None):
    """Return freshness score plus popularity score for one article."""
    freshness_score = calculate_freshness_score(
        article.get("published_at"),
        current_time,
    )
    popularity_score = calculate_popularity_score(article.get("score"))
    return freshness_score + popularity_score


def rank_articles(articles, current_time=None):
    """Return articles sorted from highest ranking score to lowest."""
    return sorted(
        articles,
        key=lambda article: calculate_ranking_score(article, current_time),
        reverse=True,
    )
