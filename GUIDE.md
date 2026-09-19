# Algorithm Notebook Guide

## Daily workflow

Create a directory named with the local date and place today's source files in it:

```text
daily/2026-09-19/
├── a.cpp
└── b.py
```

Use this metadata block at the beginning of each solution:

```cpp
/*
@url https://codeforces.com/contest/1900/problem/A
@primary simulation
@topics greedy-construction
@note
Write the reasoning, mistakes and points worth reviewing here.
Multiple lines are supported.
@endnote
*/
```

- `@url` is required.
- `@primary` is the most specific main topic and controls the physical folder.
- `@topics` is an optional comma-separated list of additional topics.
- `@note ... @endnote` is optional and may contain multiple lines.
- Use stable English topic IDs from `data/taxonomy.yaml`.

Process one date:

```bash
python scripts/manage.py process --date 2026-09-19
```

Or process the computer's current local date:

```bash
python scripts/manage.py today
```

The command validates the whole batch before moving any file. It then organizes
the source files, updates `data/problems.json`, regenerates `README.md`, and
rebuilds the data used by the website.

## Platform-specific overrides

Platform metadata is fetched when a supported source is available. These
optional fields override fetched data or fill a missing value:

```text
Codeforces: @rating 1400, @division div2
LeetCode:   @difficulty medium
AtCoder:    @rating 850
Any site:   @title Exact Problem Title
```

Use `--no-fetch` when offline. Missing difficulty remains empty and can be
filled later by editing the record or reprocessing with an override.

## Rebuilding and validation

```bash
python scripts/manage.py build
python scripts/manage.py validate
```

`README.md`, `docs/data/problems.json`, and `docs/data/taxonomy.json` are
generated files. Edit source comments, `data/problems.json`, or
`data/taxonomy.yaml`, then rebuild instead of editing generated output manually.

## GitHub Pages

The included workflow publishes the `docs` directory after every push to the
`main` branch. In a new GitHub repository, open **Settings → Pages** once and
select **GitHub Actions** as the source. The next push deploys the searchable
notebook automatically.

Install either snippet from `sublime/` through Sublime Text's `Packages/User`
directory. Type `algo` and press Tab to insert the metadata template.
