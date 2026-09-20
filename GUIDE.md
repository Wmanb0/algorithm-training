# Algorithm Notebook Guide

## Daily workflow

Create a directory named with the local date and place today's source files in it:

```text
daily/2026-09-19/
├── a.cpp
└── b.py
```

Use the dedicated GPT project to generate a complete metadata block, then paste
it at the beginning of the solution:

```cpp
/*
@url https://codeforces.com/contest/1900/problem/A
@primary simulation
@topics array, general-greedy
@rating 1400
@division div2
@note
Simulate the required operations and apply the greedy choice at each step.
Time: O(N)
Space: O(N)
@endnote
*/
```

- `@url` is required.
- `@primary` is the most specific main topic and controls the physical folder.
- `@topics` is an optional comma-separated list of additional topics.
- `@rating`, `@division`, and `@difficulty` are platform-specific and optional.
- `@note ... @endnote` is optional and may contain multiple lines.
- `manage.py` validates every GPT-generated topic against `data/taxonomy.yaml`.
  Unknown topics and parent-only categories are rejected before files move.

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

Platform metadata is fetched when a supported source is available:

- Codeforces rating comes from the official Codeforces API.
- AtCoder rating is the estimated difficulty published by AtCoder Problems.
- LeetCode uses `Easy`, `Medium`, or `Hard`; it does not use a numeric rating.

These optional fields override fetched data or fill a missing value:

```text
Codeforces: @rating 1400, @division div2
LeetCode:   @difficulty medium
AtCoder:    @rating 850
Any site:   @title Exact Problem Title
```

The rating merge order is:

1. `@rating` in the current source file.
2. A rating fetched from the platform dataset.
3. The rating already stored in `data/problems.json`.
4. Empty when none of the above is available.

This means an API failure never erases a rating you already recorded. Use
`--no-fetch` when offline. You normally do not need to write `@rating`; add it
only when a problem is unrated, the estimate is missing, or you want to correct
the fetched value.

Example Codeforces metadata:

```cpp
/*
@url https://codeforces.com/contest/1900/problem/A
@primary simulation
@topics greedy-construction
@rating 1400
@division div2
@note
Reasoning and mistakes.
@endnote
*/
```

Example AtCoder metadata:

```python
# @url https://atcoder.jp/contests/abc350/tasks/abc350_c
# @primary simulation
# @topics array, greedy-construction
# @rating 800
# @note
# Reasoning and mistakes.
# @endnote
```

`@rating` is optional in both examples. The generated README and website keep
`Level` (such as `Div.2 · A`, `ABC · C`, or `Medium`) separate from the numeric
`Rating`.

Ratings remain platform-specific and are never treated as one common scale:

- `CF 1400` means a Codeforces problem rating.
- `AtCoder ≈800` means an AtCoder Problems difficulty estimate.
- One value must not be compared directly with the other.

The website enables rating ranges and rating sorting only after selecting
`Codeforces` or `AtCoder` in the platform filter. Changing platforms clears the
old rating range so a Codeforces filter can never be applied to AtCoder data.

## File organization and name collisions

Solutions use this path format:

```text
solutions/<topic-path>/<platform>-<problem-id>/<date>.<extension>
```

For example, two Codeforces problems solved on the same date with the same
primary topic are stored separately:

```text
solutions/.../codeforces-1900A/2026-09-20.cpp
solutions/.../codeforces-1900B/2026-09-20.cpp
```

The platform prefix also prevents a Codeforces problem ID from colliding with
an ID from another platform. If the exact same problem is recorded more than
once on the same date with the same language, the later files are named
`2026-09-20-2.cpp`, `2026-09-20-3.cpp`, and so on. Existing files are never
overwritten.

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
