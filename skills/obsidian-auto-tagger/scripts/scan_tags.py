#!/usr/bin/env python3

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
INLINE_TAG_RE = re.compile(r"(?:^|\s)#([a-zA-Z0-9_-]+)")
IGNORE_DIRS = {
    ".git", ".hg", ".svn", ".obsidian", ".trash",
    ".claude", ".codex", ".agents", "node_modules", "__pycache__", "attachments",
}


def parse_frontmatter_tags(text: str) -> list[str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return []
    tags = []
    in_tags = False
    for line in match.group(1).splitlines():
        if re.match(r"^tags:\s*$", line):
            in_tags = True
            continue
        if in_tags:
            m = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if m:
                tags.append(m.group(1).strip().strip('"').strip("'"))
            elif not line.startswith(" "):
                in_tags = False
    return tags


def parse_inline_tags(text: str) -> list[str]:
    match = FRONTMATTER_RE.match(text)
    body = text[match.end():] if match else text
    return INLINE_TAG_RE.findall(body)


def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def scan_vault(root: Path, include_inline: bool = False) -> dict:
    tag_counter: Counter = Counter()
    total = tagged = 0
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if should_skip(rel):
            continue
        total += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        fm_tags = parse_frontmatter_tags(text)
        if fm_tags:
            tagged += 1
            tag_counter.update(fm_tags)
        if include_inline:
            tag_counter.update(parse_inline_tags(text))
    return {
        "tags": [{"name": t, "count": c} for t, c in tag_counter.most_common()],
        "total_files": total,
        "tagged_files": tagged,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan Obsidian vault tag taxonomy.")
    parser.add_argument("root", help="Vault root directory.")
    parser.add_argument("--include-inline", action="store_true")
    parser.add_argument("--format", choices=("text", "json"), default="json")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"Error: {root} does not exist", file=sys.stderr)
        return 1

    result = scan_vault(root, args.include_inline)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Total files:  {result['total_files']}")
        print(f"Tagged files: {result['tagged_files']}")
        print(f"Unique tags:  {len(result['tags'])}\n")
        for tag in result["tags"][:30]:
            print(f"  {tag['count']:3d}  {tag['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
