# signal-daily

## Current pipeline

Running `main.py` now does the following:

1. Fetches articles from Hacker News, TechCrunch, and CoinDesk
2. Saves new articles into SQLite (`signal.db`) with URL-based deduplication
3. Reads all stored articles
4. Ranks them using `freshness_score + popularity_score`
5. Generates `index.html`

## Run

```bash
python main.py
```