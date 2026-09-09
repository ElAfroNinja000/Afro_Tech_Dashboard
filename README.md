# Afro's Tech DashBoard

**A personal tech dasboard to stay up to date with topics I'm interested in: Data, Digital Arts and Agentic Coding. Feeds are centralized, tagged, filtered and searchable.**

## What it is

Tech watch usually means a dozen open tabs, a newsletter you stop reading after three weeks, and a social feed that decides for you what matters today.

This project is the boring alternative. A handful of RSS feeds I picked myself, pulled into one page, tagged by theme.

Feeds are refreshed on every page load, so what you see is always current.

## Feeds

| Tag | Source |
|---|---|
| **Agentic Coding** | [MIT Technology Review](https://www.technologyreview.com/feed/) |
| **Digital Arts** | [3dtotal](https://3dtotal.com/rss), [The Inspiration Grid](https://theinspirationgrid.com/feed/), [Motionographer](https://motionographer.com/feed/) |
| **Data Engineering** | [Towards Data Science](https://towardsdatascience.com/feed) |

Adding a source is a one-line change in `feeds.py`.

## How it works

```
feeds.py    →  fetches and parses every RSS source, attaches its tag
db.py       →  stores entries in SQLite
app.py      →  serves the page: tag filters + full-text search
```

## Work in progress

A personal tool that grew from a personal need, so the rough edges are the ones I have not been annoyed by yet:

- **Refreshing on every load does not scale.** Six feeds is fine. Twenty will not be. Caching with a TTL, or a background refresh, is the obvious next step.
- **More sources, better categorisation.** Three tags is a start; some entries clearly belong to two of them.
- **A blog section**, to write about what I find instead of only collecting it.
- **Not deployed anywhere yet.** It runs locally. Putting it online is the point at which the caching question above stops being optional.

## Credits

Built by [Samy Abdelazim](https://www.samy-abdelazim.com) · [LinkedIn](https://www.linkedin.com/in/samy-abdelazim-454966150/)

All feed content belongs to its respective publishers; this project only aggregates and links out.

<<Ajouter une licence : MIT est le défaut raisonnable ici.>>
