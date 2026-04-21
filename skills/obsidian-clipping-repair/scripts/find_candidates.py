#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


URL_RE = re.compile(r"https?://[^\s)\]>]+")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$")
MD_LINK_LINE_RE = re.compile(r"^\s*\[[^\]]+\]\((https?://[^)]+)\)\s*$")

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".obsidian",
    ".trash",
    "node_modules",
    "__pycache__",
    "attachments",
}
CLIPPING_DIR_HINTS = {"clippings", "clipping", "clips", "webclips", "clipper"}
SOURCE_FIELDS = {"source", "url", "link", "href", "canonical_url", "original_url"}


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = FIELD_RE.match(line)
        if field:
            fields[field.group(1).strip().lower()] = field.group(2).strip().strip('"').strip("'")
    return fields, text[match.end() :]


def nonempty_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def link_only_lines(lines: list[str]) -> int:
    count = 0
    for line in lines:
        if URL_RE.fullmatch(line) or MD_LINK_LINE_RE.fullmatch(line):
            count += 1
    return count


def excerpt(text: str, limit: int = 180) -> str:
    compact = " ".join(nonempty_lines(text))
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def score_note(path: Path, text: str) -> dict[str, object]:
    fields, body = split_frontmatter(text)
    lines = nonempty_lines(body)
    urls = URL_RE.findall(body)
    score = 0
    reasons: list[str] = []

    lower_parts = {part.lower() for part in path.parts}
    if lower_parts & CLIPPING_DIR_HINTS:
        score += 20
        reasons.append("clipping-like folder")

    if any(key in fields for key in SOURCE_FIELDS):
        score += 12
        reasons.append("source field in frontmatter")

    if urls:
        score += min(20, 8 + 4 * len(urls))
        reasons.append("contains source url")

    if len(lines) <= 6:
        score += 18
        reasons.append("very short body")
    elif len(lines) <= 12:
        score += 10
        reasons.append("short body")

    if len(body.strip()) <= 900:
        score += 14
        reasons.append("small body size")

    link_lines = link_only_lines(lines)
    if lines and link_lines / len(lines) >= 0.5:
        score += 20
        reasons.append("link-dominant body")

    if len(lines) <= 3 and urls and body.strip():
        score += 10
        reasons.append("title-plus-link shape")

    if len(lines) >= 20:
        score -= 14
        reasons.append("longer body, likely intentional note")

    if len(body.strip()) >= 2600:
        score -= 18
        reasons.append("body already substantial")

    candidate = score >= 35
    title_guess = fields.get("title") or path.stem
    source_url = next((fields[key] for key in SOURCE_FIELDS if key in fields), urls[0] if urls else "")

    return {
        "path": str(path),
        "candidate": candidate,
        "score": score,
        "title_guess": title_guess,
        "source_url": source_url,
        "reasons": reasons,
        "excerpt": excerpt(body),
        "line_count": len(lines),
        "url_count": len(urls),
    }


def iter_markdown_files(root: Path, include_dirs: list[str]) -> list[Path]:
    if include_dirs:
        search_roots = [root / rel for rel in include_dirs]
    else:
        search_roots = [root]

    files: list[Path] = []
    for search_root in search_roots:
        if not search_root.exists():
            continue
        for path in search_root.rglob("*.md"):
            rel = path.relative_to(root)
            if should_skip(rel):
                continue
            files.append(path)
    return sorted(set(files))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank likely broken clipping notes in an Obsidian vault.")
    parser.add_argument("root", help="Vault root or folder to scan.")
    parser.add_argument(
        "--include-dir",
        action="append",
        default=[],
        help="Relative folder under the root to scan. May be repeated.",
    )
    parser.add_argument("--top", type=int, default=50, help="Maximum number of results to print.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include low-scoring notes instead of filtering to likely candidates.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    results = []
    for path in iter_markdown_files(root, args.include_dir):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        results.append(score_note(path.relative_to(root), text))

    results.sort(key=lambda item: int(item["score"]), reverse=True)
    if not args.all:
        results = [item for item in results if item["candidate"]]
    if args.top >= 0:
        results = results[: args.top]

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("No likely clipping-repair candidates found.")
        return 0

    for item in results:
        reasons = ", ".join(item["reasons"])
        print(f"[{item['score']:>3}] {item['path']}")
        print(f"      title: {item['title_guess']}")
        if item["source_url"]:
            print(f"      source: {item['source_url']}")
        print(f"      reasons: {reasons}")
        if item["excerpt"]:
            print(f"      excerpt: {item['excerpt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
