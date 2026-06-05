# Reddit App Review Notes

## Link to Source Code or Platform

Use the public repository URL for this project:

Suggested field answer:

> This repository documents the read-only Reddit Data API connector used by an
> external cultural-memory research workflow. It authenticates with OAuth, uses
> a descriptive User-Agent, reads limited public post metadata from selected
> subreddits, monitors rate-limit headers, and supports deletion/removal
> handling. It does not post, comment, vote, message users, automate
> engagement, scrape Reddit HTML, train general-purpose AI models on Reddit
> content, resell Reddit data, or profile individual users.

## App Purpose

The app supports research into how public internet culture changes over time:
which older viral moments, memes, public media moments, jokes, and online trends
remain recognizable in public discussion, and which ones fade.

The research focuses on aggregate cultural signals such as continued relevance,
resurfacing trends, sentiment shifts, and nostalgia references across selected
public communities.

## Reddit Platform Behavior

The connector reads public post listings and basic metadata from selected
subreddits related to internet culture, nostalgia, memes, creator culture,
public media moments, online communities, and trend discussion.

The connector is read-only. It does not:

- post
- comment
- vote
- message users
- automate engagement
- manipulate rankings
- interfere with community discussions
- scrape Reddit HTML
- collect full comment threads
- store author profile fields

## Data Collected

Expected stored fields:

- post ID
- subreddit
- title
- permalink
- outbound public URL
- timestamp
- public score metadata
- over-18 flag
- coarse aggregate research labels downstream

The connector omits author profile fields and stores only the minimum public
post metadata needed for aggregate research and auditability.

## Compliance Commitments

The implementation is built around:

- OAuth authentication
- descriptive User-Agent
- rate-limit monitoring
- limited data retention
- source attribution
- deletion/removal workflows
- aggregate research outputs

The project does not use Reddit content to train general-purpose AI models,
resell Reddit data, profile individual users, infer sensitive personal
attributes, or build user-level marketing audiences.

## Why Not Devvit

Devvit is primarily designed for Reddit-native applications that live inside
Reddit communities, such as subreddit tools, moderator utilities, interactive
posts, games, and community-facing experiences.

This use case is an external, read-only research pipeline for aggregate
cultural trend analysis. It needs scheduled external ingestion, longitudinal
storage, cross-platform comparison, audit logging, and downstream analytics in
an external environment. It does not need a Reddit-native UI.
