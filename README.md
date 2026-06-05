# Cultural Memory Reddit Connector

Read-only Reddit Data API connector for public internet-culture research.

This repository documents the small access layer used by an external research
pipeline studying the cultural half-life of public internet moments: which
older viral moments remain recognizable, which fade, and how public discussion
changes over time.

The connector is intentionally narrow:

- authenticates with Reddit OAuth
- uses a descriptive User-Agent
- reads public post listings from selected subreddits
- stores only limited public metadata needed for aggregate research
- excludes author profile fields by default
- monitors Reddit rate-limit response headers
- provides deletion/removal handling guidance
- never posts, comments, votes, messages users, or automates engagement
- never scrapes Reddit HTML as a substitute for the Data API
- never trains general-purpose AI models on Reddit content
- never resells Reddit data or builds user-level marketing audiences

## Repository Scope

This is not the full downstream analytics system. It is the public source for
the Reddit API access layer: authentication, listing retrieval, post filtering,
record sanitization, and compliance documentation.

## Environment

Create a Reddit script app and set:

```bash
export REDDIT_CLIENT_ID="..."
export REDDIT_CLIENT_SECRET="..."
export REDDIT_USER_AGENT="python:cultural-memory-reddit-connector:v0.1.0 (by /u/<reddit_username>)"
```

The connector will not run without OAuth credentials.

## Example

```bash
python -m cultural_memory_reddit \
  --subreddit contagiouslaughter \
  --subreddit youtubehaiku \
  --limit 25
```

Output is JSON Lines with sanitized records:

```json
{"source":"reddit","post_id":"abc123","subreddit":"youtubehaiku","title":"Example public discussion","permalink":"https://www.reddit.com/r/youtubehaiku/comments/abc123/example/","url":"https://youtu.be/example","created_utc":"2026-06-05T14:00:00+00:00","score":120,"over_18":false,"signal_context":"public_culture_research"}
```

## Reddit App Review Summary

If asked to provide a link to source code or platform that will access the API,
use this repository. The intended app description is:

> This repository documents the read-only Reddit Data API connector used by an
> external cultural-memory research pipeline. The connector authenticates with
> OAuth, uses a descriptive User-Agent, collects limited public post metadata
> from selected subreddits, respects rate limits and deletion requirements, and
> feeds aggregate research/classification workflows. It does not post, comment,
> vote, message users, scrape Reddit HTML, train AI models, resell Reddit data,
> or profile individual users.

Additional review-ready language is in
[docs/REDDIT_APP_REVIEW.md](docs/REDDIT_APP_REVIEW.md).

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

No tests call Reddit or any external network.
