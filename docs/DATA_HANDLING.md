# Data Handling

The connector keeps Reddit-derived records small on purpose. It is meant to
support aggregate cultural-memory research, not account-level analysis.

## Defaults

- Store the minimum public post metadata needed for the research question.
- Do not store author profile fields.
- Do not collect or store full comment threads.
- Remove stored Reddit-derived content when the source post is deleted, removed,
  or unavailable.
- Keep any deletion audit trail minimal.

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

The record does not include usernames, profile fields, comments, private
messages, or inferred personal attributes.

## Removal Workflow

When a Reddit post is deleted, removed, or becomes unavailable:

1. Delete stored title, permalink, URL, and research labels tied to that post.
2. Keep only a minimal tombstone audit record if needed.
3. Do not keep disconnected copies of deleted Reddit content.

Example tombstone:

```json
{
  "source": "reddit",
  "post_id": "abc123",
  "status": "deleted_from_research_store",
  "reason": "deleted_or_unavailable_on_reddit"
}
```
