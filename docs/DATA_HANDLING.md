# Data Handling

## Principles

- Collect the minimum public Reddit metadata needed for aggregate research.
- Avoid user-level analysis.
- Do not store author profile fields by default.
- Do not store full comment threads by default.
- Remove stored Reddit-derived content when it is deleted or becomes unavailable.
- Keep audit records minimal after deletion.

## Default Record

```json
{
  "source": "reddit",
  "post_id": "abc123",
  "subreddit": "youtubehaiku",
  "title": "Example public discussion",
  "permalink": "https://www.reddit.com/r/youtubehaiku/comments/abc123/example/",
  "url": "https://youtu.be/example",
  "created_utc": "2026-06-05T14:00:00+00:00",
  "score": 120,
  "over_18": false,
  "signal_context": "public_culture_research"
}
```

## Removal Workflow

When a Reddit post is deleted, removed, or becomes unavailable:

1. Delete stored title, permalink, URL, and research labels tied to that post.
2. Keep only a minimal tombstone audit record if needed.
3. Do not retain disassociated copies of deleted user content.

Example tombstone:

```json
{
  "source": "reddit",
  "post_id": "abc123",
  "status": "deleted_from_research_store",
  "reason": "deleted_or_unavailable_on_reddit"
}
```
