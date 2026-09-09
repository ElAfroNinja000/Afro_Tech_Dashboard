# Afro's Tech DashBoard

**A personal tech dasboard to stay up to date with topics I'm interested in: Data, Digital Arts and Agentic Coding. Feeds are centralized, tagged, filtered and searchable.**

## What it is

Tech watch usually means a dozen open tabs, a newsletter you stop reading after three weeks, and a social feed that decides for you what matters today.

This project is the boring alternative. A handful of RSS feeds I picked myself, pulled into one page, tagged by theme.

Feeds are refreshed on every page load.

## Feeds

| Tag | Source |
|---|---|
| **Agentic Coding** | [MIT Technology Review](https://www.technologyreview.com/feed/) |
| **Digital Arts** | [3dtotal](https://3dtotal.com/rss), [The Inspiration Grid](https://theinspirationgrid.com/feed/), [Motionographer](https://motionographer.com/feed/) |
| **Data Engineering** | [Towards Data Science](https://towardsdatascience.com/feed) |

## How it works

```
feeds.py    →  fetches and parses every RSS source, attaches its tag
db.py       →  stores entries in SQLite
app.py      →  serves the page: tag filters + full-text search
```

## Work in progress

- Improving refresh performance
- Adding more sources & better categorisation
- Adding a blog section

Built by [Samy Abdelazim](https://www.samy-abdelazim.com)
