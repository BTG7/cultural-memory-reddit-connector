# Reddit App Review Notes

## Link to Source Code or Platform

Use the public repository URL for this project.

Suggested field answer:

> This repository documents the read-only Reddit Data API connector used by an
> external cultural-memory research pipeline. The connector authenticates with
> OAuth, uses a descriptive User-Agent, collects limited public post metadata
> from selected subreddits, respects rate limits and deletion requirements, and
> feeds aggregate research/classification workflows. It does not post, comment,
> vote, message users, scrape Reddit HTML, train AI models, resell Reddit data,
> or profile individual users.

## App Purpose

The app supports research into how public internet culture changes over time,
specifically whether older viral moments, memes, videos, public figures,
controversies, jokes, and online trends still remain recognizable, relevant, or
engaging in modern public discussion.

The purpose is to study the cultural half-life of viral content: how quickly
collective attention fades, which types of moments continue to resonate, and
how public discussion changes across communities over time.

## Reddit Platform Behavior

The connector periodically reads public post listings and basic metadata from
selected subreddits related to internet culture, nostalgia, memes, creator
culture, public media moments, online communities, and trend discussion.

At launch, the connector is read-only. It does not:

- post
- comment
- vote
- message users
- automate engagement
- manipulate rankings
- interfere with community discussions
- scrape Reddit HTML
- collect full comment threads by default
- store author profile fields by default

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
- coarse internal research labels downstream

The connector excludes author profile fields by default and stores only the
minimum data needed for aggregate research and auditability.

## Compliance Commitments

The implementation is designed around:

- OAuth authentication
- descriptive User-Agent
- rate-limit monitoring
- limited data retention
- source attribution
- deletion/removal workflows
- aggregate research outputs

The project will not use Reddit content to train a general-purpose AI model,
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

