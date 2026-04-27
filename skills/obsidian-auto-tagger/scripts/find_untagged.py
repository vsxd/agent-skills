#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
IGNORE_DIRS = {
    ".git", ".hg", ".svn", ".obsidian", ".trash",
    ".claude", ".codex", ".agents", "node_modules", "__pycache__", "attachments",
}


def parse_frontmatter(text: str) -> tuple[dict, str, list[str]]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text, []
    fm_text = match.group(1)
    body = text[match.end():]
    fields: dict = {}
    tags: list[str] = []
    in_tags = False
    for line in fm_text.splitlines():
        if re.match(r"^tags:\s*$", line):
            fields["tags"] = True
            in_tags = True
            continue
        if in_tags:
            m = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if m:
                tags.append(m.group(1).strip().strip('"').strip("'"))
                continue
            elif not line.startswith(" "):
                in_tags = False
        kv = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if kv:
            fields[kv.group(1).lower()] = kv.group(2).strip()
    if tags:
        fields["tags"] = True
    return fields, body, tags


def excerpt(text: str, limit: int = 200) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    compact = " ".join(lines)
    return compact[:limit - 3] + "..." if len(compact) > limit else compact


def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def iter_files(root: Path, include: list[str], exclude: list[str]) -> list[Path]:
    roots = [root / f for f in include] if include else [root]
    files = []
    for sr in roots:
        if not sr.exists():
            continue
        for p in sr.rglob("*.md"):
            rel = p.relative_to(root)
            if should_skip(rel):
                continue
            if exclude and any(str(rel).startswith(e) for e in exclude):
                continue
            files.append(p)
    return sorted(set(files))


def find_untagged(root: Path, include: list[str], exclude: list[str]) -> list[dict]:
    results = []
    for path in iter_files(root, include, exclude):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        fields, body, tags = parse_frontmatter(text)
        rel = str(path.relative_to(root))
        if not fields:
            results.append({"path": rel, "title": path.stem, "reason": "no-frontmatter", "preview": excerpt(text)})
        elif "tags" not in fields:
            results.append({"path": rel, "title": fields.get("title", path.stem), "reason": "no-tags-field", "preview": excerpt(body)})
        elif not tags:
            results.append({"path": rel, "title": fields.get("title", path.stem), "reason": "empty-tags", "preview": excerpt(body)})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Find untagged documents in Obsidian vault.")
    parser.add_argument("root", help="Vault root directory.")
    parser.add_argument("--include-folder", action="append", default=[])
    parser.add_argument("--exclude-folder", action="append", default=[])
    parser.add_argument("--format", choices=("text", "json"), default="json")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"Error: {root} does not exist", file=sys.stderr)
        return 1

    candidates = find_untagged(root, args.include_folder, args.exclude_folder)

    if args.format == "json":
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
    else:
        if not candidates:
            print("No untagged documents found.")
        else:
            print(f"Found {len(candidates)} untagged documents:\n")
            for item in candidates:
                print(f"[{item['reason']:>16}] {item['path']}")
                print(f"      title: {item['title']}")
                if item["preview"]:
                    print(f"      preview: {item['preview'][:100]}")
                print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
