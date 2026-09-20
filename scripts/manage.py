#!/usr/bin/env python3
"""Organize daily solutions and rebuild the notebook views.

The source file is the human-editable record.  The JSON files, README and web
payload are generated views and can always be rebuilt from the canonical data.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import math
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - message is tested indirectly
    raise SystemExit("PyYAML is required. Run: pip install -r requirements.txt") from exc


SUPPORTED_EXTENSIONS = {
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cxx": "C++",
    ".py": "Python",
    ".java": "Java",
    ".kt": "Kotlin",
    ".rs": "Rust",
    ".go": "Go",
    ".js": "JavaScript",
    ".ts": "TypeScript",
}

ATCODER_MODELS_URL = "https://kenkoooo.com/atcoder/resources/problem-models.json"
_ATCODER_MODELS_CACHE: dict[str, Any] | None = None


class NotebookError(RuntimeError):
    pass


def normalize_token(value: str) -> str:
    value = value.strip().lower().replace("_", " ")
    value = re.sub(r"[^a-z0-9+*]+", "-", value)
    return value.strip("-")


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, newline="\n"
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def atomic_write_json(path: Path, payload: Any) -> None:
    atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def restore_snapshot(snapshots: dict[Path, bytes | None]) -> None:
    for path, content in snapshots.items():
        if content is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as handle:
                handle.write(content)
                temporary = Path(handle.name)
            os.replace(temporary, path)


@dataclass(frozen=True)
class Topic:
    topic_id: str
    name: str
    path: tuple[str, ...]
    parent: str | None
    aliases: tuple[str, ...]
    selectable: bool


class Taxonomy:
    def __init__(self, path: Path):
        self.path = path
        with path.open("r", encoding="utf-8") as handle:
            raw = yaml.safe_load(handle) or {}
        if raw.get("version") != 1 or not isinstance(raw.get("groups"), dict):
            raise NotebookError(f"Invalid taxonomy schema: {path}")

        self.topics: dict[str, Topic] = {}
        self.lookup: dict[str, str] = {}
        for topic_id, node in raw["groups"].items():
            self._walk(topic_id, node, (), None)

    def _walk(
        self,
        topic_id: str,
        node: dict[str, Any],
        parent_path: tuple[str, ...],
        parent: str | None,
    ) -> None:
        canonical = normalize_token(topic_id)
        if canonical != topic_id:
            raise NotebookError(f"Taxonomy ID must already be normalized: {topic_id}")
        if canonical in self.topics:
            raise NotebookError(f"Duplicate taxonomy ID: {canonical}")

        children = node.get("children") or {}
        if not isinstance(children, dict):
            raise NotebookError(f"children must be a mapping for {canonical}")
        aliases = tuple(normalize_token(str(x)) for x in node.get("aliases", []))
        path = parent_path + (canonical,)
        topic = Topic(
            topic_id=canonical,
            name=str(node.get("name") or canonical),
            path=path,
            parent=parent,
            aliases=aliases,
            selectable=not children,
        )
        self.topics[canonical] = topic
        self._register(canonical, canonical)
        for alias in aliases:
            self._register(alias, canonical)
        for child_id, child_node in children.items():
            self._walk(child_id, child_node, path, canonical)

    def _register(self, key: str, topic_id: str) -> None:
        if key in self.lookup and self.lookup[key] != topic_id:
            raise NotebookError(
                f"Taxonomy alias '{key}' points to both "
                f"{self.lookup[key]} and {topic_id}"
            )
        self.lookup[key] = topic_id

    def resolve(self, raw_value: str, selectable_only: bool = True) -> str:
        key = normalize_token(raw_value)
        topic_id = self.lookup.get(key)
        if not topic_id:
            suggestions = difflib.get_close_matches(key, self.lookup.keys(), n=4, cutoff=0.55)
            detail = ""
            if suggestions:
                canonical = list(dict.fromkeys(self.lookup[item] for item in suggestions))
                detail = f" Did you mean: {', '.join(canonical)}?"
            raise NotebookError(f"Unknown topic '{raw_value}'.{detail}")
        topic = self.topics[topic_id]
        if selectable_only and not topic.selectable:
            children = [item.topic_id for item in self.topics.values() if item.parent == topic_id]
            raise NotebookError(
                f"Topic '{raw_value}' is a group. Choose a more specific topic, "
                f"for example: {', '.join(children[:8])}"
            )
        return topic_id

    def ancestors(self, topic_id: str) -> list[str]:
        result: list[str] = []
        current: str | None = topic_id
        while current:
            result.append(current)
            current = self.topics[current].parent
        return list(reversed(result))

    def public_payload(self) -> dict[str, Any]:
        return {
            "version": 1,
            "topics": [
                {
                    "id": item.topic_id,
                    "name": item.name,
                    "parent": item.parent,
                    "path": list(item.path),
                    "selectable": item.selectable,
                }
                for item in self.topics.values()
            ],
        }


def clean_metadata_line(line: str) -> str:
    value = line.strip()
    value = re.sub(r"^(?://+|#+|/\*+|\*+)\s?", "", value)
    value = re.sub(r"\s*\*/\s*$", "", value)
    return value.rstrip()


def parse_metadata(source: Path) -> dict[str, str]:
    text = source.read_text(encoding="utf-8-sig")
    metadata: dict[str, str] = {}
    note_lines: list[str] = []
    in_note = False

    for raw_line in text.splitlines():
        line = clean_metadata_line(raw_line)
        if in_note:
            if re.match(r"^@endnote\s*$", line, flags=re.IGNORECASE):
                metadata["note"] = "\n".join(note_lines).strip()
                in_note = False
                continue
            note_lines.append(line)
            continue

        match = re.match(r"^@([a-zA-Z][\w-]*)(?:\s*:\s*|\s+)?(.*)$", line)
        if not match:
            continue
        key = match.group(1).lower().replace("_", "-")
        value = match.group(2).strip()
        if key == "note":
            if value:
                metadata["note"] = value
            else:
                in_note = True
                note_lines = []
        elif key != "endnote":
            metadata[key] = value

    if in_note:
        raise NotebookError(f"{source}: @note is missing @endnote")
    return metadata


def title_from_slug(slug: str) -> str:
    small_words = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to"}
    words = slug.replace("_", "-").split("-")
    output = []
    for index, word in enumerate(words):
        lower = word.lower()
        if index and lower in small_words:
            output.append(lower)
        else:
            output.append(lower.capitalize())
    return " ".join(output)


def parse_problem_url(url: str, metadata: dict[str, str]) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.rstrip("/")

    cf = re.search(r"/(?:contest|problemset/problem)/(\d+)/(?:problem/)?([A-Za-z0-9]+)$", path)
    if host.endswith("codeforces.com") and cf:
        contest_id, index = cf.groups()
        return {
            "id": f"codeforces:{contest_id}:{index.upper()}",
            "platform": "codeforces",
            "problem_id": f"{contest_id}{index.upper()}",
            "title": f"Codeforces {contest_id}{index.upper()}",
            "platform_meta": {
                "contest_id": int(contest_id),
                "problem_index": index.upper(),
                "rating": None,
                "divisions": [],
            },
        }

    lc = re.search(r"/problems/([^/]+)", path)
    if host.endswith("leetcode.com") and lc:
        slug = lc.group(1)
        return {
            "id": f"leetcode:{slug}",
            "platform": "leetcode",
            "problem_id": slug,
            "title": title_from_slug(slug),
            "platform_meta": {"slug": slug, "difficulty": None},
        }

    ac = re.search(r"/contests/([^/]+)/tasks/([^/]+)$", path)
    if host.endswith("atcoder.jp") and ac:
        contest_id, task_id = ac.groups()
        index = task_id.rsplit("_", 1)[-1].upper()
        series_match = re.match(r"([a-zA-Z]+)", contest_id)
        series = series_match.group(1).upper() if series_match else contest_id.upper()
        return {
            "id": f"atcoder:{task_id.lower()}",
            "platform": "atcoder",
            "problem_id": task_id.upper(),
            "title": f"AtCoder {contest_id.upper()} {index}",
            "platform_meta": {
                "contest_id": contest_id.lower(),
                "contest_series": series,
                "problem_index": index,
                "task_id": task_id.lower(),
                "difficulty_rating": None,
            },
        }

    platform = normalize_token(metadata.get("platform") or host.split(".")[0] or "other")
    problem_id = metadata.get("id") or path.split("/")[-1] or parsed.netloc
    return {
        "id": f"{platform}:{normalize_token(problem_id)}",
        "platform": platform,
        "problem_id": problem_id,
        "title": metadata.get("title") or title_from_slug(problem_id),
        "platform_meta": {},
    }


def http_json(request: urllib.request.Request, timeout: float = 8.0) -> Any:
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_codeforces_metadata(problem: dict[str, Any]) -> dict[str, Any]:
    meta = problem["platform_meta"]
    contest_id = meta["contest_id"]
    url = (
        "https://codeforces.com/api/contest.standings?"
        + urllib.parse.urlencode({"contestId": contest_id, "from": 1, "count": 1})
    )
    payload = http_json(urllib.request.Request(url, headers={"User-Agent": "AlgorithmNotebook/1.0"}))
    if payload.get("status") != "OK":
        raise NotebookError(f"Codeforces API error: {payload.get('comment', 'unknown error')}")

    result = payload["result"]
    contest_name = result.get("contest", {}).get("name", "")
    divisions = [f"div{value}" for value in re.findall(r"Div\.?\s*([1-4])", contest_name, re.I)]
    target = next(
        (item for item in result.get("problems", []) if item.get("index") == meta["problem_index"]),
        None,
    )
    if not target:
        raise NotebookError("Problem was not returned by the Codeforces API")
    return {
        "title": target.get("name") or problem["title"],
        "platform_meta": {
            **meta,
            "rating": target.get("rating"),
            "rating_source": "codeforces" if target.get("rating") is not None else None,
            "divisions": list(dict.fromkeys(divisions)),
            "contest_name": contest_name or None,
        },
    }


def display_atcoder_rating(difficulty: float) -> int:
    """Convert an AtCoder Problems model value to its displayed rating."""
    displayed = difficulty if difficulty >= 400 else 400 / math.exp(1 - difficulty / 400)
    return int(math.floor(displayed + 0.5))


def fetch_atcoder_metadata(problem: dict[str, Any]) -> dict[str, Any]:
    global _ATCODER_MODELS_CACHE

    if _ATCODER_MODELS_CACHE is None:
        payload = http_json(
            urllib.request.Request(
                ATCODER_MODELS_URL,
                headers={"User-Agent": "AlgorithmNotebook/1.0"},
            )
        )
        if not isinstance(payload, dict):
            raise NotebookError("AtCoder Problems returned an invalid difficulty dataset")
        _ATCODER_MODELS_CACHE = payload

    meta = problem["platform_meta"]
    task_id = str(meta.get("task_id") or problem["id"].removeprefix("atcoder:")).lower()
    model = _ATCODER_MODELS_CACHE.get(task_id)
    if not isinstance(model, dict) or model.get("difficulty") is None:
        raise NotebookError(f"AtCoder Problems has no estimated rating for {task_id}")
    try:
        raw_difficulty = float(model["difficulty"])
    except (TypeError, ValueError) as exc:
        raise NotebookError(f"AtCoder Problems returned an invalid rating for {task_id}") from exc

    return {
        "platform_meta": {
            **meta,
            "difficulty_rating": display_atcoder_rating(raw_difficulty),
            "difficulty_raw": raw_difficulty,
            "rating_source": "atcoder-problems",
        }
    }


def fetch_leetcode_metadata(problem: dict[str, Any]) -> dict[str, Any]:
    query = """
      query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
          questionFrontendId
          title
          difficulty
        }
      }
    """
    body = json.dumps(
        {"query": query, "variables": {"titleSlug": problem["platform_meta"]["slug"]}}
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "AlgorithmNotebook/1.0"},
        method="POST",
    )
    payload = http_json(request)
    question = (payload.get("data") or {}).get("question")
    if not question:
        raise NotebookError("LeetCode did not return problem metadata")
    return {
        "title": question.get("title") or problem["title"],
        "problem_id": question.get("questionFrontendId") or problem["problem_id"],
        "platform_meta": {
            **problem["platform_meta"],
            "difficulty": str(question.get("difficulty") or "").lower() or None,
        },
    }


def apply_manual_metadata(problem: dict[str, Any], metadata: dict[str, str]) -> None:
    if metadata.get("title"):
        problem["title"] = metadata["title"]
    platform = problem["platform"]
    meta = problem["platform_meta"]
    if platform == "codeforces":
        if metadata.get("rating"):
            try:
                meta["rating"] = int(metadata["rating"])
            except ValueError as exc:
                raise NotebookError("@rating must be an integer") from exc
            meta["rating_source"] = "manual"
        if metadata.get("division"):
            divisions = []
            for item in split_csv(metadata["division"]):
                normalized = normalize_token(item).replace("-", "")
                match = re.fullmatch(r"(?:div)?([1-4])", normalized)
                if not match:
                    raise NotebookError(f"Invalid Codeforces division: {item}")
                divisions.append(f"div{match.group(1)}")
            meta["divisions"] = list(dict.fromkeys(divisions))
    elif platform == "leetcode" and metadata.get("difficulty"):
        level = normalize_token(metadata["difficulty"])
        if level not in {"easy", "medium", "hard"}:
            raise NotebookError("LeetCode @difficulty must be easy, medium or hard")
        meta["difficulty"] = level
    elif platform == "atcoder":
        rating = metadata.get("rating") or metadata.get("difficulty-rating")
        if rating:
            try:
                meta["difficulty_rating"] = int(rating)
            except ValueError as exc:
                raise NotebookError("AtCoder @rating must be an integer") from exc
            meta["rating_source"] = "manual"


def enrich_problem(problem: dict[str, Any], metadata: dict[str, str], fetch: bool) -> list[str]:
    warnings: list[str] = []
    if fetch:
        try:
            if problem["platform"] == "codeforces":
                problem.update(fetch_codeforces_metadata(problem))
            elif problem["platform"] == "leetcode":
                problem.update(fetch_leetcode_metadata(problem))
            elif problem["platform"] == "atcoder":
                problem.update(fetch_atcoder_metadata(problem))
        except (NotebookError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            warnings.append(f"Could not fetch metadata for {problem['id']}: {exc}")
    apply_manual_metadata(problem, metadata)
    return warnings


def problem_rating(problem: dict[str, Any]) -> int | None:
    meta = problem.get("platform_meta") or {}
    if problem.get("platform") == "codeforces":
        return meta.get("rating")
    if problem.get("platform") == "atcoder":
        return meta.get("difficulty_rating")
    return None


def problem_rating_system(problem: dict[str, Any]) -> str | None:
    if problem.get("platform") == "codeforces":
        return "codeforces"
    if problem.get("platform") == "atcoder":
        return "atcoder-problems"
    return None


def rating_label(problem: dict[str, Any]) -> str:
    rating = problem_rating(problem)
    if rating is None:
        return "—"
    system = problem_rating_system(problem)
    if system == "codeforces":
        return f"CF {rating}"
    if system == "atcoder-problems":
        return f"AtCoder ≈{rating}"
    return str(rating)


def level_label(problem: dict[str, Any]) -> str:
    platform = problem["platform"]
    meta = problem.get("platform_meta") or {}
    if platform == "codeforces":
        parts = [item.replace("div", "Div.") for item in meta.get("divisions", [])]
        if meta.get("problem_index"):
            parts.append(str(meta["problem_index"]))
        return " · ".join(parts) or "—"
    if platform == "leetcode":
        value = meta.get("difficulty")
        return str(value).title() if value else "—"
    if platform == "atcoder":
        parts = []
        if meta.get("contest_series"):
            parts.append(str(meta["contest_series"]))
        if meta.get("problem_index"):
            parts.append(str(meta["problem_index"]))
        return " · ".join(parts) or "—"
    return str(meta.get("difficulty") or "—")


def difficulty_label(problem: dict[str, Any]) -> str:
    """Backward-compatible name for the platform-specific level label."""
    return level_label(problem)


def load_database(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "problems": []}
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("schema_version") != 1 or not isinstance(payload.get("problems"), list):
        raise NotebookError(f"Unsupported database schema: {path}")
    return payload


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def platform_name(value: str) -> str:
    known = {"codeforces": "Codeforces", "leetcode": "LeetCode", "atcoder": "AtCoder"}
    return known.get(value, title_from_slug(value))


def all_attempts(database: dict[str, Any]) -> Iterable[tuple[dict[str, Any], dict[str, Any]]]:
    for problem in database["problems"]:
        for attempt in problem.get("attempts", []):
            yield problem, attempt


def generate_readme(database: dict[str, Any], taxonomy: Taxonomy) -> str:
    problems = database["problems"]
    attempts = list(all_attempts(database))
    dates = sorted({attempt["date"] for _, attempt in attempts})
    platforms = Counter(problem["platform"] for problem in problems)
    topic_counts: Counter[str] = Counter()
    for problem in problems:
        topic_counts.update(set(problem.get("topics", [])))

    lines = [
        "# Algorithm Training",
        "",
        "<!-- Generated by scripts/manage.py. Edit source comments or taxonomy.yaml instead. -->",
        "",
        "## Statistics",
        "",
        f"- Training days: **{len(dates)}**",
        f"- Problems solved: **{len(problems)}**",
        f"- Training attempts: **{len(attempts)}**",
        f"- Platforms: **{len(platforms)}**",
        f"- Topics used: **{len(topic_counts)}**",
        "",
        "### By Platform",
        "",
        "| Platform | Problems |",
        "|---|---:|",
    ]
    if platforms:
        for platform, count in sorted(platforms.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {platform_name(platform)} | {count} |")
    else:
        lines.append("| — | 0 |")

    lines.extend(["", "### By Topic", "", "| Topic | Problems |", "|---|---:|"])
    if topic_counts:
        for topic_id, count in sorted(
            topic_counts.items(),
            key=lambda item: (-item[1], taxonomy.topics[item[0]].name.lower()),
        ):
            lines.append(f"| {taxonomy.topics[topic_id].name} | {count} |")
    else:
        lines.append("| — | 0 |")

    lines.extend(["", "## Daily Log", ""])
    by_date: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    for problem, attempt in attempts:
        by_date[attempt["date"]].append((problem, attempt))

    if not by_date:
        lines.append("No training records yet.")
    else:
        for date in sorted(by_date, reverse=True):
            lines.extend(
                [
                    f"### {date}",
                    "",
                    "| Problem | Platform | Level | Rating | Topics |",
                    "|---|---|---|---:|---|",
                ]
            )
            for problem, _attempt in sorted(by_date[date], key=lambda pair: pair[0]["title"]):
                topic_names = ", ".join(
                    taxonomy.topics[topic_id].name for topic_id in problem.get("topics", [])
                )
                title = markdown_escape(problem["title"])
                lines.append(
                    f"| [{title}]({problem['url']}) | {platform_name(problem['platform'])} | "
                    f"{markdown_escape(level_label(problem))} | "
                    f"{rating_label(problem)} | {markdown_escape(topic_names)} |"
                )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_web_payload(root: Path, database: dict[str, Any], taxonomy: Taxonomy) -> dict[str, Any]:
    problems: list[dict[str, Any]] = []
    for problem in database["problems"]:
        item = json.loads(json.dumps(problem))
        item["level_label"] = level_label(problem)
        item["difficulty_label"] = item["level_label"]
        item["rating"] = problem_rating(problem)
        item["rating_system"] = problem_rating_system(problem)
        item["rating_label"] = rating_label(problem)
        item["rating_source"] = (problem.get("platform_meta") or {}).get("rating_source")
        item["topic_paths"] = {
            topic_id: taxonomy.ancestors(topic_id) for topic_id in problem.get("topics", [])
        }
        for attempt in item.get("attempts", []):
            source_path = root / attempt["source_file"]
            attempt["code"] = source_path.read_text(encoding="utf-8-sig") if source_path.exists() else ""
        problems.append(item)
    return {"schema_version": 1, "problems": problems}


def build_outputs(root: Path, database: dict[str, Any], taxonomy: Taxonomy) -> None:
    atomic_write_text(root / "README.md", generate_readme(database, taxonomy))
    atomic_write_json(root / "docs/data/problems.json", build_web_payload(root, database, taxonomy))
    atomic_write_json(root / "docs/data/taxonomy.json", taxonomy.public_payload())


def destination_for(
    root: Path,
    taxonomy: Taxonomy,
    primary_topic: str,
    problem: dict[str, Any],
    date: str,
    extension: str,
    reserved: set[Path],
) -> Path:
    topic_path = taxonomy.topics[primary_topic].path
    safe_problem_id = re.sub(r"[^A-Za-z0-9._-]+", "-", problem["problem_id"]).strip("-")
    directory = root / "solutions" / Path(*topic_path) / f"{problem['platform']}-{safe_problem_id}"
    candidate = directory / f"{date}{extension.lower()}"
    index = 2
    while candidate.exists() or candidate in reserved:
        candidate = directory / f"{date}-{index}{extension.lower()}"
        index += 1
    reserved.add(candidate)
    return candidate


def process_daily(root: Path, date: str, fetch: bool) -> tuple[int, list[str]]:
    try:
        dt.date.fromisoformat(date)
    except ValueError as exc:
        raise NotebookError("Date must use YYYY-MM-DD") from exc

    daily = root / "daily" / date
    if not daily.exists():
        raise NotebookError(f"Daily directory does not exist: {daily}")
    files = sorted(
        item for item in daily.rglob("*") if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not files:
        build_outputs(root, load_database(root / "data/problems.json"), Taxonomy(root / "data/taxonomy.yaml"))
        return 0, [f"No supported source files found in {daily}"]

    taxonomy = Taxonomy(root / "data/taxonomy.yaml")
    database_path = root / "data/problems.json"
    database = load_database(database_path)
    problems_by_id = {item["id"]: item for item in database["problems"]}
    plans: list[dict[str, Any]] = []
    warnings: list[str] = []
    reserved: set[Path] = set()

    # Validate every file before moving any of them.
    for source in files:
        metadata = parse_metadata(source)
        url = metadata.get("url")
        if not url:
            raise NotebookError(f"{source}: missing @url")
        raw_topics = split_csv(metadata.get("topics"))
        raw_primary = metadata.get("primary") or (raw_topics[0] if raw_topics else None)
        if not raw_primary:
            raise NotebookError(f"{source}: add @primary or at least one @topics value")
        primary = taxonomy.resolve(raw_primary)
        topics: list[str] = [primary]
        for raw_topic in raw_topics:
            topic_id = taxonomy.resolve(raw_topic)
            if topic_id not in topics:
                topics.append(topic_id)

        problem_data = parse_problem_url(url, metadata)
        warnings.extend(enrich_problem(problem_data, metadata, fetch))
        existing = problems_by_id.get(problem_data["id"])
        problem = json.loads(json.dumps(existing or problem_data))
        if existing:
            problem["url"] = url
            candidate_title = problem_data.get("title")
            is_generic_cf_title = (
                problem_data["platform"] == "codeforces"
                and candidate_title == f"Codeforces {problem_data['problem_id']}"
            )
            if metadata.get("title"):
                problem["title"] = metadata["title"]
            elif candidate_title and not is_generic_cf_title:
                problem["title"] = candidate_title

            merged_meta = dict(problem.get("platform_meta") or {})
            for key, value in (problem_data.get("platform_meta") or {}).items():
                if value not in (None, "", []):
                    merged_meta[key] = value
            problem["platform_meta"] = merged_meta

            candidate_id = problem_data.get("problem_id")
            if problem_data["platform"] != "leetcode" or candidate_id != problem_data["platform_meta"].get("slug"):
                problem["problem_id"] = candidate_id or problem["problem_id"]
        else:
            problem["url"] = url
            problem["attempts"] = []

        problem["primary_topic"] = primary
        problem["topics"] = list(dict.fromkeys([*problem.get("topics", []), *topics]))
        destination = destination_for(
            root, taxonomy, primary, problem, date, source.suffix, reserved
        )
        attempt = {
            "date": date,
            "language": SUPPORTED_EXTENSIONS[source.suffix.lower()],
            "source_file": destination.relative_to(root).as_posix(),
            "note": metadata.get("note", ""),
        }
        plans.append(
            {
                "source": source,
                "destination": destination,
                "problem": problem,
                "attempt": attempt,
            }
        )
        problems_by_id[problem["id"]] = problem

    generated_paths = [
        database_path,
        root / "README.md",
        root / "docs/data/problems.json",
        root / "docs/data/taxonomy.json",
    ]
    snapshots = {path: path.read_bytes() if path.exists() else None for path in generated_paths}
    moved: list[tuple[Path, Path]] = []
    try:
        for plan in plans:
            destination = plan["destination"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(plan["source"]), str(destination))
            moved.append((destination, plan["source"]))

        for plan in plans:
            problem = plan["problem"]
            attempt = plan["attempt"]
            stored = problems_by_id[problem["id"]]
            stored.update(problem)
            stored.setdefault("attempts", []).append(attempt)
            stored["attempts"].sort(key=lambda item: (item["date"], item["source_file"]))

        database["problems"] = sorted(problems_by_id.values(), key=lambda item: item["id"])
        atomic_write_json(database_path, database)
        build_outputs(root, database, taxonomy)
    except Exception:
        restore_snapshot(snapshots)
        for destination, original in reversed(moved):
            if destination.exists() and not original.exists():
                original.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(original))
        raise

    return len(plans), warnings


def validate_repository(root: Path) -> list[str]:
    taxonomy = Taxonomy(root / "data/taxonomy.yaml")
    database = load_database(root / "data/problems.json")
    errors: list[str] = []
    seen_problem_ids: set[str] = set()
    for problem in database["problems"]:
        if problem.get("id") in seen_problem_ids:
            errors.append(f"Duplicate problem ID: {problem.get('id')}")
        seen_problem_ids.add(problem.get("id"))
        for topic_id in problem.get("topics", []):
            if topic_id not in taxonomy.topics or not taxonomy.topics[topic_id].selectable:
                errors.append(f"{problem.get('id')}: invalid topic {topic_id}")
        for attempt in problem.get("attempts", []):
            path = root / attempt.get("source_file", "")
            if not path.is_file():
                errors.append(f"{problem.get('id')}: missing source file {path}")
    return errors


def default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain the algorithm training notebook")
    parser.add_argument("--root", type=Path, default=default_root(), help=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest="command", required=True)

    process = subparsers.add_parser("process", help="Process one daily directory")
    process.add_argument("--date", default=dt.datetime.now().astimezone().date().isoformat())
    process.add_argument("--no-fetch", action="store_true", help="Do not request platform metadata")

    today = subparsers.add_parser("today", help="Process today's daily directory")
    today.add_argument("--no-fetch", action="store_true", help="Do not request platform metadata")

    subparsers.add_parser("build", help="Regenerate README and frontend data")
    subparsers.add_parser("validate", help="Validate taxonomy, records and source paths")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = create_parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command in {"process", "today"}:
            date = (
                args.date
                if args.command == "process"
                else dt.datetime.now().astimezone().date().isoformat()
            )
            count, warnings = process_daily(root, date, fetch=not args.no_fetch)
            for warning in warnings:
                print(f"warning: {warning}", file=sys.stderr)
            print(f"Processed {count} solution(s) for {date}.")
            return 0

        taxonomy = Taxonomy(root / "data/taxonomy.yaml")
        database = load_database(root / "data/problems.json")
        if args.command == "build":
            build_outputs(root, database, taxonomy)
            print("README and frontend data rebuilt.")
            return 0

        errors = validate_repository(root)
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        print("Repository validation passed.")
        return 0
    except (NotebookError, OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
