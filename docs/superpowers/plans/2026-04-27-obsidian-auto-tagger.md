# Obsidian Auto Tagger Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a skills.sh-compatible skill that automatically tags untagged Obsidian vault documents using existing tag taxonomy.

**Architecture:** Two Python scripts handle scanning (tag collection and candidate discovery), Agent reads document content and recommends tags from existing list, batch suggestion workflow with user review before applying changes.

**Tech Stack:** Python 3 (standard library only), Markdown frontmatter parsing (regex-based), skills.sh structure

---

## File Structure

```
skills/obsidian-auto-tagger/
├── SKILL.md                           # Main skill entry point
├── agents/openai.yaml                 # UI metadata for OpenAI integration
├── references/
│   ├── tagging-guidelines.md          # Tag selection rules and style guide
│   └── batch-mode.md                  # Batch processing and safety rules
└── scripts/
    ├── scan_tags.py                   # Collect existing tag taxonomy
    └── find_untagged.py               # Discover documents needing tags
```

---

### Task 1: Create Directory Structure

**Files:**
- Create: `skills/obsidian-auto-tagger/`
- Create: `skills/obsidian-auto-tagger/scripts/`
- Create: `skills/obsidian-auto-tagger/references/`
- Create: `skills/obsidian-auto-tagger/agents/`

- [ ] **Step 1: Create skill directory structure**

```bash
mkdir -p skills/obsidian-auto-tagger/{scripts,references,agents}
```

- [ ] **Step 2: Verify structure**

Run: `ls -la skills/obsidian-auto-tagger/`
Expected: directories `scripts`, `references`, `agents` exist

- [ ] **Step 3: Commit**

```bash
git add skills/obsidian-auto-tagger/
git commit -m "$(cat <<'EOF'
feat: create obsidian-auto-tagger skill structure

Initialize directory structure for auto-tagging skill
EOF
)"
```

---

### Task 2: Implement Tag Scanner Script

**Files:**
- Create: `skills/obsidian-auto-tagger/scripts/scan_tags.py`

- [ ] **Step 1: Write script skeleton with imports and constants**

```python
#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path
from collections import Counter


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
INLINE_TAG_RE = re.compile(r"(?:^|\s)#([a-zA-Z0-9_-]+)")
IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".obsidian",
    ".trash",
    ".claude",
    ".codex",
    ".agents",
    "node_modules",
    "__pycache__",
    "attachments",
}
```

- [ ] **Step 2: Add frontmatter parsing function**

```python
def parse_frontmatter_tags(text: str) -> list[str]:
    """Extract tags from YAML frontmatter."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return []
    
    fm = match.group(1)
    tags = []
    in_tags_section = False
    
    for line in fm.splitlines():
        if re.match(r"^tags:\s*$", line):
            in_tags_section = True
            continue
        if in_tags_section:
            tag_match = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if tag_match:
                tag = tag_match.group(1).strip().strip('"').strip("'")
                tags.append(tag)
            elif not line.startswith(" "):
                in_tags_section = False
    
    return tags
```

- [ ] **Step 3: Add inline tag extraction function**

```python
def parse_inline_tags(text: str) -> list[str]:
    """Extract #tag style tags from document body."""
    # Skip frontmatter
    match = FRONTMATTER_RE.match(text)
    body = text[match.end():] if match else text
    
    return INLINE_TAG_RE.findall(body)
```

- [ ] **Step 4: Add file iteration function**

```python
def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    return any(part in IGNORE_DIRS for part in path.parts)


def iter_markdown_files(root: Path) -> list[Path]:
    """Recursively find all Markdown files."""
    files = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if should_skip(rel):
            continue
        files.append(path)
    return sorted(files)
```

- [ ] **Step 5: Add main scanning logic**

```python
def scan_vault(root: Path, include_inline: bool = False) -> dict:
    """Scan vault and collect tag statistics."""
    tag_counter = Counter()
    total_files = 0
    tagged_files = 0
    
    for path in iter_markdown_files(root):
        total_files += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        
        fm_tags = parse_frontmatter_tags(text)
        if fm_tags:
            tagged_files += 1
            tag_counter.update(fm_tags)
        
        if include_inline:
            inline_tags = parse_inline_tags(text)
            tag_counter.update(inline_tags)
    
    tags = [{"name": tag, "count": count} 
            for tag, count in tag_counter.most_common()]
    
    return {
        "tags": tags,
        "total_files": total_files,
        "tagged_files": tagged_files,
    }
```

- [ ] **Step 6: Add CLI argument parser and main function**

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan Obsidian vault and collect existing tag taxonomy."
    )
    parser.add_argument("root", help="Vault root directory to scan.")
    parser.add_argument(
        "--include-inline",
        action="store_true",
        help="Also detect #tag style inline tags in document body.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="json",
        help="Output format (default: json).",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    
    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"Error: {root} does not exist", file=sys.stderr)
        return 1
    
    result = scan_vault(root, args.include_inline)
    
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Total files: {result['total_files']}")
        print(f"Tagged files: {result['tagged_files']}")
        print(f"Unique tags: {len(result['tags'])}")
        print("\nTop tags:")
        for tag_info in result['tags'][:30]:
            print(f"  {tag_info['count']:3d}  {tag_info['name']}")
    
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
```

- [ ] **Step 7: Make script executable**

```bash
chmod +x skills/obsidian-auto-tagger/scripts/scan_tags.py
```

- [ ] **Step 8: Test script on test vault**

Run: `python3 skills/obsidian-auto-tagger/scripts/scan_tags.py "/Users/xudongsun/Library/Mobile Documents/iCloud~md~obsidian/Documents/MainVault" --format text`
Expected: Output shows total files, tagged files, and top tags list

- [ ] **Step 9: Test JSON output**

Run: `python3 skills/obsidian-auto-tagger/scripts/scan_tags.py "/Users/xudongsun/Library/Mobile Documents/iCloud~md~obsidian/Documents/MainVault" --format json | head -30`
Expected: Valid JSON with tags array

- [ ] **Step 10: Commit**

```bash
git add skills/obsidian-auto-tagger/scripts/scan_tags.py
git commit -m "$(cat <<'EOF'
feat: add tag scanner script

Scans Obsidian vault to collect existing tag taxonomy with frequencies
EOF
)"
```

---

### Task 3: Implement Untagged Candidate Finder Script

**Files:**
- Create: `skills/obsidian-auto-tagger/scripts/find_untagged.py`

- [ ] **Step 1: Write script skeleton with imports and constants**

```python
#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".obsidian",
    ".trash",
    ".claude",
    ".codex",
    ".agents",
    "node_modules",
    "__pycache__",
    "attachments",
}
```

- [ ] **Step 2: Add frontmatter parsing and tag detection functions**

```python
def parse_frontmatter(text: str) -> tuple[dict, str, list[str]]:
    """Parse frontmatter. Returns (fields_dict, body, tags_list)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text, []
    
    fm_text = match.group(1)
    body = text[match.end():]
    fields = {}
    tags = []
    in_tags_section = False
    
    for line in fm_text.splitlines():
        if re.match(r"^tags:\s*$", line):
            fields["tags"] = True
            in_tags_section = True
            continue
        if in_tags_section:
            tag_match = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if tag_match:
                tags.append(tag_match.group(1).strip().strip('"').strip("'"))
                continue
            elif not line.startswith(" "):
                in_tags_section = False
        kv_match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if kv_match:
            key = kv_match.group(1).strip().lower()
            value = kv_match.group(2).strip()
            fields[key] = value
    
    if tags:
        fields["tags"] = True
    
    return fields, body, tags


def has_tags(fields: dict, tags: list[str]) -> tuple[bool, str]:
    """Check if document has tags. Returns (has_tags, reason)."""
    if "tags" not in fields:
        return False, "no-tags-field"
    if not tags:
        return False, "empty-tags"
    return True, "has-tags"
```

- [ ] **Step 3: Add excerpt generation function**

```python
def excerpt(text: str, limit: int = 200) -> str:
    """Generate preview excerpt from text."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    compact = " ".join(lines)
    if len(compact) <= limit:
        return compact
    return compact[:limit - 3] + "..."
```

- [ ] **Step 4: Add file iteration and filtering**

```python
def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    return any(part in IGNORE_DIRS for part in path.parts)


def iter_markdown_files(root: Path, include_folders: list[str], 
                        exclude_folders: list[str]) -> list[Path]:
    """Recursively find Markdown files with folder filters."""
    if include_folders:
        search_roots = [root / folder for folder in include_folders]
    else:
        search_roots = [root]
    
    files = []
    for search_root in search_roots:
        if not search_root.exists():
            continue
        for path in search_root.rglob("*.md"):
            rel = path.relative_to(root)
            if should_skip(rel):
                continue
            # Check exclude folders
            if exclude_folders and any(
                str(rel).startswith(folder) for folder in exclude_folders
            ):
                continue
            files.append(path)
    
    return sorted(set(files))
```

- [ ] **Step 5: Add candidate analysis function**

```python
def analyze_file(path: Path, root: Path, text: str) -> dict | None:
    """Analyze file and return candidate info if untagged."""
    rel_path = path.relative_to(root)
    fields, body, tags = parse_frontmatter(text)
    
    # Check if has frontmatter
    if not fields:
        title = path.stem
        return {
            "path": str(rel_path),
            "title": title,
            "reason": "no-frontmatter",
            "preview": excerpt(text),
        }
    
    # Check if has tags
    has_tag, reason = has_tags(fields, tags)
    if not has_tag:
        title = fields.get("title", path.stem)
        return {
            "path": str(rel_path),
            "title": title,
            "reason": reason,
            "preview": excerpt(body),
        }
    
    return None
```

- [ ] **Step 6: Add main scanning logic**

```python
def find_untagged(root: Path, include_folders: list[str],
                  exclude_folders: list[str]) -> list[dict]:
    """Find all untagged documents in vault."""
    candidates = []
    
    for path in iter_markdown_files(root, include_folders, exclude_folders):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        
        candidate = analyze_file(path, root, text)
        if candidate:
            candidates.append(candidate)
    
    return candidates
```

- [ ] **Step 7: Add CLI and main function**

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Find untagged documents in Obsidian vault."
    )
    parser.add_argument("root", help="Vault root directory to scan.")
    parser.add_argument(
        "--include-folder",
        action="append",
        default=[],
        help="Only scan these folders (relative to root). May be repeated.",
    )
    parser.add_argument(
        "--exclude-folder",
        action="append",
        default=[],
        help="Skip these folders (relative to root). May be repeated.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="json",
        help="Output format (default: json).",
    )
    return parser


def main() -> int:
    parser = build_parser()
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
                if item['preview']:
                    print(f"      preview: {item['preview']}")
                print()
    
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
```

- [ ] **Step 8: Make script executable**

```bash
chmod +x skills/obsidian-auto-tagger/scripts/find_untagged.py
```

- [ ] **Step 9: Test script on test vault**

Run: `python3 skills/obsidian-auto-tagger/scripts/find_untagged.py "/Users/xudongsun/Library/Mobile Documents/iCloud~md~obsidian/Documents/MainVault" --format text`
Expected: Lists untagged documents with reasons

- [ ] **Step 10: Test JSON output**

Run: `python3 skills/obsidian-auto-tagger/scripts/find_untagged.py "/Users/xudongsun/Library/Mobile Documents/iCloud~md~obsidian/Documents/MainVault" --format json`
Expected: Valid JSON array of candidate objects

- [ ] **Step 11: Commit**

```bash
git add skills/obsidian-auto-tagger/scripts/find_untagged.py
git commit -m "$(cat <<'EOF'
feat: add untagged document finder script

Discovers documents without tags (no frontmatter, no tags field, empty tags)
EOF
)"
```

---

### Task 4: Write Tagging Guidelines Reference

**Files:**
- Create: `skills/obsidian-auto-tagger/references/tagging-guidelines.md`

- [ ] **Step 1: Write tagging guidelines document**

```markdown
# Tagging Guidelines

Rules for selecting and creating tags when auto-tagging Obsidian documents.

## Tag Selection Priority

1. **Always prefer existing tags** — scan the vault's tag taxonomy first
2. Only create new tags when no existing tag fits the document's main topic
3. When creating new tags, mark them as "new" in suggestions for user review

## Tag Count

- Target: 1-2 tags per document
- Maximum: 3 tags
- Focus on the document's primary topic, not every mentioned concept

## Tag Style

- Lowercase English words
- Hyphen-separated for multi-word tags (e.g., `prompt-engineering`)
- No spaces, underscores, or special characters
- Match the existing tag style in the vault

## What NOT to Tag

- Author handles (e.g., `@Russell3402`, `@username`)
- Platform names unless they're the document's main topic
- Generic terms that apply to most documents
- Overly specific terms that won't be reused

## Tag Granularity

Prefer coarse-grained topic tags:
- Good: `ai`, `engineering`, `business`, `java`
- Acceptable: `distributed-systems`, `prompt-engineering`
- Too specific: `gpt4-turbo-api`, `react-18-hooks`

## Reading Documents

When analyzing a document for tagging:
1. Read the title and frontmatter first
2. Skim the first 2-3 paragraphs for main topic
3. Check for explicit topic statements or summaries
4. Don't over-index on passing mentions

## Confidence Levels

- **High confidence**: Document clearly about a topic with matching existing tag
- **Medium confidence**: Document topic matches but requires new tag
- **Low confidence**: Document topic unclear or too broad — skip and report

## Safety Rules

- Never modify document body content
- Never remove existing tags (append-only in optimization mode)
- Preserve all other frontmatter fields unchanged
- Skip documents where confidence is low
```

- [ ] **Step 2: Commit**

```bash
git add skills/obsidian-auto-tagger/references/tagging-guidelines.md
git commit -m "$(cat <<'EOF'
docs: add tagging guidelines reference

Defines tag selection rules, style conventions, and safety guidelines
EOF
)"
```

---

### Task 5: Write Batch Mode Reference

**Files:**
- Create: `skills/obsidian-auto-tagger/references/batch-mode.md`

- [ ] **Step 1: Write batch mode document**

```markdown
# Batch Mode

Guidelines for processing multiple documents in a single tagging session.

## Workflow Sequence

1. **Scan existing tags** — Run `scan_tags.py` to build tag taxonomy
2. **Find candidates** — Run `find_untagged.py` to discover untagged documents
3. **Batch read** — Read candidates in groups of 5-10 documents
4. **Generate suggestions** — Create tag recommendations for the batch
5. **Present for review** — Show all suggestions in table format
6. **Apply after approval** — Write tags only after user confirms
7. **Report results** — Summarize applied, skipped, and new tags created

## Suggestion Table Format

```
| File | Current Tags | Suggested Tags | Reason |
|------|--------------|----------------|--------|
| path/to/doc1.md | (none) | ai, engineering | Article about AI agents |
| path/to/doc2.md | (none) | business (new) | Business strategy piece |
```

Mark new tags clearly so user can review tag taxonomy expansion.

## Safety Rules

- Never write tags without user confirmation
- Process in small batches (5-10 documents) to allow review
- Skip ambiguous documents rather than guessing
- Preserve existing frontmatter structure exactly
- Create frontmatter block if missing, using vault's standard format

## Error Handling

- File read errors → skip and report
- Frontmatter parse errors → skip and report
- Low confidence → skip and report
- User rejects suggestion → skip that document

## Reporting

Final report should include:
- Total candidates found
- Tags applied (count)
- New tags created (list them)
- Skipped documents (count and reasons)
- Any errors encountered

## Optimization Mode

When `--include-weak-tags` is used:
- Also process documents with existing tags
- Append suggested tags to existing ones
- Never remove existing tags
- Mark as "optimization" in suggestions
```

- [ ] **Step 2: Commit**

```bash
git add skills/obsidian-auto-tagger/references/batch-mode.md
git commit -m "$(cat <<'EOF'
docs: add batch mode reference

Defines batch processing workflow, safety rules, and reporting format
EOF
)"
```

---

### Task 6: Write Main Skill Document

**Files:**
- Create: `skills/obsidian-auto-tagger/SKILL.md`

- [ ] **Step 1: Write SKILL.md with frontmatter and overview**

```markdown
---
name: obsidian-auto-tagger
description: Automatically tag untagged Obsidian vault documents using existing tag taxonomy. Agent reads document content, selects 1-2 tags from vault's existing tags, and only creates new tags when no existing tag fits. Batch suggestion workflow with user review before applying changes.
license: MIT
compatibility: Best in agents that can read local Markdown files, execute Python scripts, and edit Obsidian vault frontmatter.
metadata:
  author: vsxd
  version: "1.0.0"
---

# Obsidian Auto Tagger

Automatically tag untagged documents in an Obsidian vault using the vault's existing tag taxonomy.

## Use This Skill When

- User points at an Obsidian vault and asks to tag documents
- User specifies a folder or single document needing tags
- User asks to organize or supplement vault tags
- Documents lack frontmatter, have no `tags` field, or have empty tags

## Do Not Use

- Documents already have well-maintained tags and user hasn't requested optimization
- Non-Markdown files (Excalidraw scripts, attachments, etc.)
- User wants to reorganize or rename existing tags (different workflow)

## Workflow

### 1. Determine Scope

If user names one document, process it directly. If user points at vault or folder, inventory candidates first.

### 2. Scan Existing Tag Taxonomy

```bash
python3 skills/obsidian-auto-tagger/scripts/scan_tags.py /path/to/vault --format json
```

This builds the tag vocabulary. Prefer existing tags over creating new ones.

### 3. Discover Untagged Candidates

```bash
python3 skills/obsidian-auto-tagger/scripts/find_untagged.py /path/to/vault --format json
```

Identifies documents needing tags:
- No frontmatter
- No `tags` field in frontmatter
- Empty `tags` field

Optional: `--include-folder Clippings` to scan specific folders only.

### 4. Read and Recommend Tags

For each candidate:
- Read title, frontmatter, and body (first few paragraphs)
- Identify the document's main topic
- Select 1-2 tags from existing tag list
- Only propose new tags (marked "new") when no existing tag fits

Use [references/tagging-guidelines.md](references/tagging-guidelines.md) for tag selection rules.

### 5. Present Suggestion List

Show all recommendations in table format:

```
| File | Current Tags | Suggested Tags | Reason |
|------|--------------|----------------|--------|
| ... | ... | ... | ... |
```

Wait for user approval before writing any changes.

### 6. Apply Changes

After user confirms, write tags into frontmatter:
- No frontmatter → create frontmatter block with tags
- No tags field → add tags field to existing frontmatter
- Empty tags → populate tags list
- Preserve all other frontmatter fields unchanged

### 7. Verify and Report

Report:
- Tags applied per document
- New tags created (list them)
- Existing vs new tag ratio
- Skipped documents with reasons

Use [references/batch-mode.md](references/batch-mode.md) for batch processing guidelines.

## Built-In Scripts

### Tag Scanner

```bash
python3 skills/obsidian-auto-tagger/scripts/scan_tags.py <vault-path> [--include-inline] [--format json|text]
```

Collects all existing tags and their frequencies. Use `--include-inline` to also detect `#tag` style tags in document bodies.

### Candidate Finder

```bash
python3 skills/obsidian-auto-tagger/scripts/find_untagged.py <vault-path> [--include-folder DIR] [--exclude-folder DIR] [--format json|text]
```

Finds documents without tags. Use folder filters to narrow scope.

## Ground Rules

- Prefer existing tags over new ones — always
- Never overwrite existing user-authored tags
- Never modify document body content
- Always present suggestions before applying
- If confidence is low, skip the document and report why
- Target 1-2 tags per document, max 3

## Reference Files

- [references/tagging-guidelines.md](references/tagging-guidelines.md): Tag selection rules, style conventions, confidence levels
- [references/batch-mode.md](references/batch-mode.md): Batch processing workflow, safety rules, reporting format
```

- [ ] **Step 2: Commit**

```bash
git add skills/obsidian-auto-tagger/SKILL.md
git commit -m "$(cat <<'EOF'
docs: add main skill document

Defines skill workflow, usage guidelines, and script integration
EOF
)"
```

---

### Task 7: Create OpenAI UI Metadata

**Files:**
- Create: `skills/obsidian-auto-tagger/agents/openai.yaml`

- [ ] **Step 1: Write openai.yaml**

```yaml
interface:
  display_name: "Obsidian Auto Tagger"
  short_description: "Auto-tag untagged Obsidian documents using existing tags."
  default_prompt: "Use $obsidian-auto-tagger to tag untagged documents in this vault."

policy:
  allow_implicit_invocation: true
```

- [ ] **Step 2: Commit**

```bash
git add skills/obsidian-auto-tagger/agents/openai.yaml
git commit -m "$(cat <<'EOF'
feat: add OpenAI UI metadata

Enables skill discovery and invocation in OpenAI-compatible interfaces
EOF
)"
```

---

### Task 8: Validate Skill Discovery

**Files:**
- Test: skill discovery via skills.sh CLI

- [ ] **Step 1: Run skills discovery**

Run: `npx skills add . --list`
Expected: Output includes `obsidian-auto-tagger` in the list

- [ ] **Step 2: Verify skill structure**

Run: `ls -la skills/obsidian-auto-tagger/`
Expected: All files present (SKILL.md, agents/, references/, scripts/)

- [ ] **Step 3: Test scan_tags.py on test vault**

Run: `python3 skills/obsidian-auto-tagger/scripts/scan_tags.py "/Users/xudongsun/Library/Mobile Documents/iCloud~md~obsidian/Documents/MainVault" --format text | head -20`
Expected: Shows tag statistics

- [ ] **Step 4: Test find_untagged.py on test vault**

Run: `python3 skills/obsidian-auto-tagger/scripts/find_untagged.py "/Users/xudongsun/Library/Mobile Documents/iCloud~md~obsidian/Documents/MainVault" --format text`
Expected: Lists untagged documents

- [ ] **Step 5: Verify all tests pass**

Confirm: skills discovery lists the skill, both scripts run without errors on the test vault.

---

### Task 9: Update Repository README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read current README**

Read: `README.md`

- [ ] **Step 2: Add obsidian-auto-tagger to skills list**

Add entry in the skills section:

```markdown
### obsidian-auto-tagger

Auto-tag untagged Obsidian vault documents using existing tag taxonomy. Agent reads content and recommends 1-2 tags from vault's existing tags, with batch suggestion workflow and user review.

**Installation:**
```bash
npx skills add vsxd/agent-skills --skill obsidian-auto-tagger
```

**Usage:** Point agent at vault and ask to tag untagged documents.
```

- [ ] **Step 3: Commit README update**

```bash
git add README.md
git commit -m "$(cat <<'EOF'
docs: add obsidian-auto-tagger to README

Document new skill in repository skill list
EOF
)"
```

---

## Self-Review Checklist

**Spec Coverage:**
- ✓ Directory structure (Task 1)
- ✓ scan_tags.py script (Task 2)
- ✓ find_untagged.py script (Task 3)
- ✓ Tagging guidelines reference (Task 4)
- ✓ Batch mode reference (Task 5)
- ✓ Main SKILL.md (Task 6)
- ✓ OpenAI metadata (Task 7)
- ✓ Validation (Task 8)
- ✓ Documentation (Task 9)

**Placeholder Scan:**
- No TBD, TODO, or "implement later" markers
- All code blocks contain complete implementations
- All file paths are exact
- All commands have expected output

**Type Consistency:**
- Function names consistent across tasks
- Data structures match between scripts and documentation
- File paths use consistent format

**No Gaps:**
- All spec requirements covered
- Scripts implement full functionality
- Documentation complete
- Testing included
