# Phase 1: Prepare Article Data for Enrichment

## Goal

Prepare Signal's article data for future topic classification, duplicate-story
clustering, summaries, and personalization without adding AI processing yet.

## Completed work

### 1. Added article descriptions

[`fetch.py`](./fetch.py) now includes a `description` field in every article
dictionary:

- Hacker News uses the item's `text` field when available.
- RSS sources use the feed entry's `summary` field when available.
- Missing descriptions are stored as `None`.

The article format now includes:

```python
{
    "title": "...",
    "url": "...",
    "source": "...",
    "published_at": 1234567890,
    "score": 0,
    "description": "Original source description",
}
```

### 2. Expanded the SQLite schema

[`db.py`](./db.py) now supports these enrichment fields:

| Column | Purpose |
| --- | --- |
| `description` | Original article description |
| `summary` | Future generated summary |
| `topics` | Future stored topic labels |
| `content_hash` | Future normalized-content hash |
| `cluster_id` | Future duplicate-story cluster |
| `processed_at` | Future enrichment timestamp |

The existing fields remain:

```text
id
title
url
source
published_at
score
fetched_at
```

### 3. Added safe database migration

`init_db()` checks the existing `articles` table with:

```sql
PRAGMA table_info(articles)
```

Missing columns are added with `ALTER TABLE`. This preserves existing article
rows and avoids deleting `signal.db`.

The migration was verified to preserve 400 existing rows while adding all six
new enrichment columns.

### 4. Updated database writes

`save_articles()` now stores the fetched `description`.

The future enrichment fields are not modified during normal fetching. This
prevents later summaries, topics, hashes, clusters, or processing timestamps
from being accidentally overwritten.

### 5. Updated database reads

`get_articles()` now returns the original fields and all enrichment fields so
future processing code can use one consistent article structure.

## Validation completed

- Python syntax validation passed for `db.py`.
- Existing database rows were preserved during migration.
- All new columns were confirmed in SQLite.
- `get_articles()` was confirmed to return the expanded article structure.
- Phase 1 changes were committed and pushed in commit `a14f6a1`.

## Not included in Phase 1

The following features are intentionally deferred:

- Topic classification
- URL normalization
- Semantic similarity
- Duplicate-story clustering
- AI-generated summaries
- User profiles and personalization

## Phase 1 result

Signal now preserves richer source data and has database fields ready for
future enrichment while keeping the existing fetch, storage, ranking, and
static-site pipeline intact.

## Next phase

Phase 2 will implement URL normalization and improved exact duplicate
detection.
