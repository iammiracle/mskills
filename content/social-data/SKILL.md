---
name: social-data
description: Pull data from Instagram, TikTok, YouTube, Pinterest, Threads or X for the user's apps and channels. Use for an account's stats, its top posts, what a viral video says, what's working in a niche, competitor or reference accounts, or a snapshot of every account a channel runs. Uses ScrapeCreators via ~/Documents/workspace/contents/shared/tools/social.py.
---

# Social data

One tool for every platform: `shared/tools/social.py`, run from `~/Documents/workspace/contents/`. Each call costs 1 ScrapeCreators credit; the response's `credits_remaining` shows the balance.

## A channel's accounts

A channel can run any number of accounts. They're listed in `contents/<name>/profile.yaml` under `accounts:`, keyed by a short id, each with `platform`, `handle`, and optionally `language` and `formats`. Accounts worth learning from go under `references:`, with a `why`.

```bash
python3 -I shared/tools/social.py accounts <name>          # every account the channel posts from
python3 -I shared/tools/social.py accounts <name> --refs   # plus its reference accounts
```

This prints followers and best views per account and saves the full snapshot (top posts included) to `contents/<name>/data/<date>.json`. Compare it with earlier snapshots in that folder to see growth. When the user creates a new account, add it to `accounts:`.

## One account, post or search

```bash
python3 -I shared/tools/social.py <platform> profile <handle>
python3 -I shared/tools/social.py <platform> top <handle> [n]      # most viewed first: views, likes, comments, url, hook
python3 -I shared/tools/social.py <platform> transcript <url>      # what a video says, with timestamps
python3 -I shared/tools/social.py tiktok|instagram post <url>      # one post: stats, caption, transcript, video and slide URLs
python3 -I shared/tools/social.py <platform> search "<query>"
python3 -I shared/tools/social.py pinterest pin|board <url>  /  pinterest boards <handle>
```

Platforms: `instagram`, `tiktok`, `youtube` (Shorts), `pinterest`, `threads`, `twitter`. For an endpoint the tool doesn't cover (comments, hashtags, trending, Facebook, LinkedIn, Reddit…), the full list is at https://docs.scrapecreators.com/openapi.json; add a route to `ROUTES` in `social.py` rather than calling curl by hand.

## Turning data into ideas

- **Rank by views relative to followers, not raw views.** A 1M-view reel on a 5k account is a format worth copying; on a 5M account it's just reach.
- **For the top 3 posts:** get the transcript, then break down the hook, the beats, the punchline and the call to action. Save strong breakdowns to `shared/library/<account>-<topic>.md`, as in `deadliftdividends-format.md`.
- **Compare openings:** hooks built on a belief ("X doesn't work") usually beat topic labels ("5 facts about X").
- **Add the ideas** to the channel's `ideas.md`, each with the reference post's URL.

## Rules

- Read-only. Never post, comment, follow or message from these tools.
- Data shown to the user is a sample of public posts, not analytics. Say so when drawing conclusions.
