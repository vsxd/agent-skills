#!/usr/bin/env python3

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
INLINE_TAG_RE = re.compile(r"(?<![\w/@])#([A-Za-z0-9_\-/\u4e00-\u9fff]+)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
WIKI_LINK_RE = re.compile(r"!?(?:\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\])")
URL_RE = re.compile(r"https?://\S+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_+-]{2,}|[\u4e00-\u9fff]{2,}")

IGNORE_DIRS = {
    ".git",
    ".agents",
    ".claude",
    ".codex",
    ".hg",
    ".svn",
    ".obsidian",
    ".trash",
    "node_modules",
    "__pycache__",
    "attachments",
    "assets",
}
STOP_WORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "but",
    "can",
    "for",
    "from",
    "has",
    "have",
    "into",
    "not",
    "that",
    "the",
    "this",
    "with",
    "you",
    "your",
}


def normalize_tag(tag: str) -> str:
    tag = tag.strip().strip("#").strip().strip('"').strip("'")
    tag = tag.replace(" ", "-")
    return tag.strip("/,")


def split_frontmatter(text: str) -> tuple[list[str], str, re.Match[str] | None]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return [], text, None
    return match.group(1).splitlines(), text[match.end() :], match


def parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [normalize_tag(part) for part in value.split(",") if normalize_tag(part)]


def frontmatter_tags(lines: list[str]) -> list[str]:
    tags: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        field = FIELD_RE.match(line)
        if not field or field.group(1).lower() != "tags":
            index += 1
            continue

        value = field.group(2).strip()
        if value:
            tags.extend(parse_inline_list(value))
            index += 1
            continue

        index += 1
        while index < len(lines):
            child = lines[index]
            if child and not child.startswith((" ", "\t", "-")):
                break
            stripped = child.strip()
            if stripped.startswith("-"):
                tag = normalize_tag(stripped[1:].strip())
                if tag:
                    tags.append(tag)
            index += 1
    return tags


def inline_tags(body: str) -> list[str]:
    tags = []
    for match in INLINE_TAG_RE.finditer(body):
        tag = normalize_tag(match.group(1))
        if not tag or tag.isdigit() or tag.startswith("^"):
            continue
        tags.append(tag)
    return tags


def extract_title(path: Path, frontmatter: list[str], body: str) -> str:
    for line in frontmatter:
        field = FIELD_RE.match(line)
        if field and field.group(1).lower() == "title" and field.group(2).strip():
            return field.group(2).strip().strip('"').strip("'")
    for line in body.splitlines():
        heading = HEADING_RE.match(line.strip())
        if heading:
            return heading.group(1).strip()
    return path.stem


def meaningful_lines(body: str) -> list[str]:
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("---", "```", "![[")):
            continue
        if URL_RE.fullmatch(stripped):
            continue
        lines.append(stripped)
    return lines


def excerpt(body: str, limit: int = 260) -> str:
    compact = " ".join(meaningful_lines(body))
    return compact if len(compact) <= limit else compact[: limit - 3] + "..."


def candidate_terms(path: Path, title: str, body: str, limit: int = 12) -> list[str]:
    text = " ".join([str(path.with_suffix("")), title, " ".join(meaningful_lines(body)[:20])])
    text = URL_RE.sub(" ", text)
    text = WIKI_LINK_RE.sub(r" \1 ", text)
    counts: Counter[str] = Counter()
    for raw in WORD_RE.findall(text):
        term = raw.strip("_-/").lower()
        if len(term) < 2 or term in STOP_WORDS or term.isdigit():
            continue
        counts[term] += 1
    return [term for term, _ in counts.most_common(limit)]


def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def iter_markdown_files(root: Path, include_dirs: list[str]) -> list[Path]:
    search_roots = [root / rel for rel in include_dirs] if include_dirs else [root]
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


def read_note(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def note_record(root: Path, path: Path) -> dict[str, Any]:
    text = read_note(path)
    frontmatter, body, _ = split_frontmatter(text)
    tags = sorted(set(frontmatter_tags(frontmatter) + inline_tags(body)))
    rel = path.relative_to(root)
    title = extract_title(rel, frontmatter, body)
    return {
        "path": str(rel),
        "title": title,
        "tags": tags,
        "has_tags": bool(tags),
        "excerpt": excerpt(body),
        "candidate_terms": candidate_terms(rel, title, body),
    }


def scan_vault(root: Path, include_dirs: list[str], top_untagged: int) -> dict[str, Any]:
    notes = [note_record(root, path) for path in iter_markdown_files(root, include_dirs)]
    tag_counts: Counter[str] = Counter(tag for note in notes for tag in note["tags"])
    untagged = [note for note in notes if not note["has_tags"]]
    if top_untagged >= 0:
        untagged = untagged[:top_untagged]
    return {
        "root": str(root),
        "total_notes": len(notes),
        "tagged_notes": sum(1 for note in notes if note["has_tags"]),
        "untagged_notes": sum(1 for note in notes if not note["has_tags"]),
        "existing_tags": [
            {"tag": tag, "count": count} for tag, count in tag_counts.most_common()
        ],
        "untagged": untagged,
    }


def load_assignments(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "assignments" in data:
        data = data["assignments"]
    if isinstance(data, dict):
        data = [{"path": key, "tags": value} for key, value in data.items()]
    if not isinstance(data, list):
        raise ValueError("Assignments must be a list, mapping, or object with an assignments list.")
    assignments = []
    for item in data:
        if not isinstance(item, dict) or "path" not in item or "tags" not in item:
            raise ValueError("Each assignment must include path and tags.")
        tags = item["tags"]
        if isinstance(tags, str):
            tags = [tags]
        clean_tags = [normalize_tag(str(tag)) for tag in tags if normalize_tag(str(tag))]
        if not clean_tags:
            raise ValueError(f"Assignment for {item['path']} has no usable tags.")
        assignments.append({"path": item["path"], "tags": sorted(set(clean_tags))})
    return assignments


def render_tags_block(tags: list[str]) -> list[str]:
    return ["tags:"] + [f"  - {tag}" for tag in tags]


def frontmatter_has_tags(lines: list[str]) -> bool:
    return any(FIELD_RE.match(line) and FIELD_RE.match(line).group(1).lower() == "tags" for line in lines)


def replace_or_add_tags(text: str, tags: list[str]) -> str:
    frontmatter, body, match = split_frontmatter(text)
    tag_block = render_tags_block(tags)
    if match:
        output: list[str] = []
        index = 0
        replaced = False
        while index < len(frontmatter):
            line = frontmatter[index]
            field = FIELD_RE.match(line)
            if field and field.group(1).lower() == "tags":
                output.extend(tag_block)
                replaced = True
                index += 1
                while index < len(frontmatter):
                    child = frontmatter[index]
                    if child and not child.startswith((" ", "\t", "-")):
                        break
                    index += 1
                continue
            output.append(line)
            index += 1
        if not replaced:
            insert_at = 1 if output and FIELD_RE.match(output[0]) and FIELD_RE.match(output[0]).group(1).lower() == "title" else len(output)
            output[insert_at:insert_at] = tag_block
        return "---\n" + "\n".join(output).rstrip() + "\n---\n" + body

    return "---\n" + "\n".join(tag_block) + "\n---\n" + text


def apply_assignments(root: Path, assignments_path: Path, write: bool, force: bool) -> dict[str, Any]:
    changes = []
    skipped = []
    for assignment in load_assignments(assignments_path):
        rel = Path(assignment["path"])
        if rel.is_absolute() or ".." in rel.parts:
            skipped.append({"path": str(rel), "reason": "path must be relative to vault root"})
            continue
        path = root / rel
        if not path.exists() or path.suffix.lower() != ".md":
            skipped.append({"path": str(rel), "reason": "markdown file not found"})
            continue
        if should_skip(rel):
            skipped.append({"path": str(rel), "reason": "ignored directory"})
            continue

        text = read_note(path)
        frontmatter, body, _ = split_frontmatter(text)
        existing = sorted(set(frontmatter_tags(frontmatter) + inline_tags(body)))
        if existing and not force:
            skipped.append({"path": str(rel), "reason": "already has tags", "tags": existing})
            continue

        new_text = replace_or_add_tags(text, assignment["tags"])
        if write and new_text != text:
            path.write_text(new_text, encoding="utf-8")
        changes.append({"path": str(rel), "tags": assignment["tags"], "written": bool(write)})
    return {"write": write, "changed": changes, "skipped": skipped}


def print_text_scan(result: dict[str, Any]) -> None:
    print(f"Root: {result['root']}")
    print(f"Notes: {result['total_notes']} total, {result['tagged_notes']} tagged, {result['untagged_notes']} untagged")
    print("\nTop existing tags:")
    for item in result["existing_tags"][:30]:
        print(f"  {item['tag']}: {item['count']}")
    print("\nUntagged notes:")
    for note in result["untagged"]:
        print(f"- {note['path']}")
        print(f"  title: {note['title']}")
        if note["candidate_terms"]:
            print(f"  terms: {', '.join(note['candidate_terms'][:10])}")
        if note["excerpt"]:
            print(f"  excerpt: {note['excerpt']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inventory and apply tags for Obsidian Markdown vaults.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Inventory existing tags and untagged notes.")
    scan.add_argument("root", help="Vault root or folder to scan.")
    scan.add_argument("--include-dir", action="append", default=[], help="Relative folder under root to scan. May be repeated.")
    scan.add_argument("--top-untagged", type=int, default=50, help="Maximum untagged notes to print. Use -1 for all.")
    scan.add_argument("--format", choices=("text", "json"), default="text", help="Output format.")

    apply = subparsers.add_parser("apply", help="Apply tag assignments from JSON.")
    apply.add_argument("root", help="Vault root.")
    apply.add_argument("assignments", help="JSON assignment file.")
    apply.add_argument("--write", action="store_true", help="Write changes. Without this flag, only dry-run.")
    apply.add_argument("--force", action="store_true", help="Retag files that already have tags.")
    apply.add_argument("--format", choices=("text", "json"), default="text", help="Output format.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()

    if args.command == "scan":
        result = scan_vault(root, args.include_dir, args.top_untagged)
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_text_scan(result)
        return 0

    result = apply_assignments(root, Path(args.assignments).expanduser().resolve(), args.write, args.force)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        mode = "write" if args.write else "dry-run"
        print(f"Mode: {mode}")
        for item in result["changed"]:
            print(f"change: {item['path']} -> {', '.join(item['tags'])}")
        for item in result["skipped"]:
            print(f"skip: {item['path']} ({item['reason']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
