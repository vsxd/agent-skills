#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


URL_RE = re.compile(r"https?://[^\s)\]>]+")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$")
MD_LINK_LINE_RE = re.compile(r"^\s*\[[^\]]+\]\((https?://[^)]+)\)\s*$")
HEADING_RE = re.compile(r"^#{1,6}\s+")
TRUNCATED_END_RE = re.compile(r"(?:\.\.\.|…|[（(「『\"“‘][^）)」』\"”’]{0,80})$")
CLIPPER_MARKERS = (
    (re.compile(r"\bread original\b", re.IGNORECASE), "read-original marker"),
    (re.compile(r"\bread on\b", re.IGNORECASE), "read-on marker"),
    (re.compile(r"\bomnivore\b|omnivore\.app", re.IGNORECASE), "omnivore marker"),
    (re.compile(r"^##\s+highlights\b|\bhighlights\b", re.IGNORECASE | re.MULTILINE), "highlights section"),
    (re.compile(r"\binstapaper\b", re.IGNORECASE), "instapaper marker"),
    (re.compile(r"\bpocket\b", re.IGNORECASE), "pocket marker"),
    (re.compile(r"\braindrop(?:\.io)?\b", re.IGNORECASE), "raindrop marker"),
    (re.compile(r"matter://|\bread on matter\b|\bmatter\.com\b", re.IGNORECASE), "matter marker"),
)

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
HEALTHY_METADATA_FIELDS = {"author", "published", "description", "site_name", "domain", "created"}


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


def heading_lines(lines: list[str]) -> int:
    return sum(1 for line in lines if HEADING_RE.match(line))


def quote_lines(lines: list[str]) -> int:
    return sum(1 for line in lines if line.startswith(">"))


def clipper_markers(body: str) -> list[str]:
    return [label for pattern, label in CLIPPER_MARKERS if pattern.search(body)]


def looks_truncated(lines: list[str]) -> bool:
    if not lines:
        return False
    last_line = lines[-1]
    if TRUNCATED_END_RE.search(last_line):
        return True
    return len(last_line) >= 80 and last_line[-1] not in ".!?。！？:：)]）】\"”'’"


def metadata_key_count(fields: dict[str, str]) -> int:
    return len([key for key in fields if fields[key]])


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
    source_hints = [fields[key] for key in SOURCE_FIELDS if key in fields]
    healthy_metadata_count = sum(1 for key in HEALTHY_METADATA_FIELDS if key in fields)
    metadata_count = metadata_key_count(fields)
    headings = heading_lines(lines)
    quotes = quote_lines(lines)
    markers = clipper_markers(body)
    truncated = looks_truncated(lines)
    score = 0
    reasons: list[str] = []

    lower_parts = {part.lower() for part in path.parts}
    if lower_parts & CLIPPING_DIR_HINTS:
        score += 20
        reasons.append("clipping-like folder")

    if source_hints:
        score += 12
        reasons.append("source field in frontmatter")

    if urls:
        score += min(20, 8 + 4 * len(urls))
        reasons.append("contains source url")

    if markers:
        score += min(18, 8 + 4 * len(markers))
        reasons.extend(markers)

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

    if quotes >= 3:
        score += 8
        reasons.append("quote-heavy highlight export")

    if headings >= 1 and len(lines) <= 14:
        score += 4
        reasons.append("title-and-fragment structure")

    if metadata_count <= 2 and "title" in fields:
        score += 6
        reasons.append("minimal clip metadata")

    if len(lines) <= 3 and urls and body.strip():
        score += 10
        reasons.append("title-plus-link shape")

    if truncated:
        score += 8
        reasons.append("possibly truncated ending")

    if not source_hints and not urls and not markers:
        score -= 18
        reasons.append("no explicit source hint")
    elif not source_hints and not urls:
        score -= 8
        reasons.append("indirect source hints only")

    if len(body.strip()) >= 1200 and len(lines) >= 8:
        score -= 12
        reasons.append("body already meaningful")

    if healthy_metadata_count >= 2 and len(body.strip()) >= 1500:
        score -= 20
        reasons.append("note already looks complete")

    if len(lines) >= 20:
        score -= 14
        reasons.append("longer body, likely intentional note")

    if len(body.strip()) >= 2600:
        score -= 18
        reasons.append("body already substantial")

    confidence = "high" if score >= 45 else "medium" if score >= 34 else "review" if score >= 26 else "low"
    candidate = confidence in {"high", "medium"}
    title_guess = fields.get("title") or path.stem
    source_url = source_hints[0] if source_hints else (urls[0] if urls else "")

    return {
        "path": str(path),
        "candidate": candidate,
        "score": score,
        "confidence": confidence,
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
        results = [item for item in results if item["confidence"] != "low"]
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
        print(f"[{item['score']:>3} {item['confidence']:^6}] {item['path']}")
        print(f"      title: {item['title_guess']}")
        if item["source_url"]:
            print(f"      source: {item['source_url']}")
        print(f"      reasons: {reasons}")
        if item["excerpt"]:
            print(f"      excerpt: {item['excerpt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
