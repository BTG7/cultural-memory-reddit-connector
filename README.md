# Cultural Memory Reddit Connector

A small, read-only Reddit Data API connector for public internet-culture
research.

The project is intentionally modest: it authenticates with Reddit OAuth, reads
public post listings from selected subreddits, and emits sanitized JSON Lines
records for aggregate cultural-memory research. The research question is how
public internet moments age: which references remain recognizable, which fade,
and how discussion changes over time.

## What It Does

- authenticates with Reddit OAuth client credentials
- uses a descriptive User-Agent
- reads public `top` listings for selected subreddits
- keeps only limited public post metadata useful for aggregate research
- omits author profile fields
- tracks Reddit rate-limit response headers
- documents deletion and removal handling

## Boundaries

This repository is only the public Reddit access layer: authentication, listing
retrieval, post filtering, record sanitization, a CLI, tests, and compliance
notes.

It does not post, comment, vote, send messages, automate engagement, scrape
Reddit HTML, train general-purpose AI models on Reddit content, resell Reddit
data, or build user-level marketing audiences.

## Architecture

```text
Reddit OAuth -> subreddit top listings -> sanitizer -> JSON Lines records
```

The sanitizer drops self posts, galleries, image posts, removed content, and
unapproved outbound hosts. The default record is deliberately small and suited
to aggregate analysis rather than user-level study.

## Environment

Create a Reddit script app and set:

```bash
export REDDIT_CLIENT_ID="..."
export REDDIT_CLIENT_SECRET="..."
export REDDIT_USER_AGENT="python:cultural-memory-reddit-connector:v0.1.0 (by /u/<reddit_username>)"
```

The connector will not run without OAuth credentials.

## Usage

```bash
cultural-memory-reddit \
  --subreddit contagiouslaughter \
  --subreddit youtubehaiku \
  --limit 25 \
  --time-filter year \
  --include-rate-limit
```

Output is JSON Lines. Each line is one sanitized public post record:

```json
{"source":"reddit","post_id":"abc123","subreddit":"youtubehaiku","title":"Example public discussion","permalink":"https://www.reddit.com/r/youtubehaiku/comments/abc123/example/","url":"https://youtu.be/example","created_utc":"2026-06-05T14:00:00+00:00","score":120,"over_18":false,"signal_context":"public_culture_research"}
```

## Reddit App Review Summary

If asked to provide a link to source code or platform that will access the API,
use this repository. The intended app description is:

> This repository documents the read-only Reddit Data API connector used by an
> external cultural-memory research workflow. It authenticates with OAuth, uses
> a descriptive User-Agent, reads limited public post metadata from selected
> subreddits, monitors rate-limit headers, and supports deletion/removal
> handling. It does not post, comment, vote, message users, automate
> engagement, scrape Reddit HTML, train general-purpose AI models on Reddit
> content, resell Reddit data, or profile individual users.

Additional review-ready language is in
[docs/REDDIT_APP_REVIEW.md](docs/REDDIT_APP_REVIEW.md).

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

No tests call Reddit or any external network.

## License

MIT
