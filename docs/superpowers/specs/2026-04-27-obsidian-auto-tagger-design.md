# Obsidian Auto Tagger — Design Spec

## Overview

A skills.sh-compatible skill that automatically tags untagged Obsidian vault documents using existing tag taxonomy. The agent reads document content, selects 1-2 tags from the vault's existing tag list, and only creates new tags when no existing tag fits.

## Trigger Conditions

Use when:
- User points at an Obsidian vault and asks to tag documents
- User specifies a folder or single document needing tags
- User asks to organize/supplement vault tags

Do not use when:
- Documents already have well-maintained tags and user hasn't asked for optimization
- Non-Markdown files (Excalidraw scripts, attachments, etc.)

## Workflow (7 Steps)

### 1. Determine Scope
Single document → process directly. Vault/folder → scan for candidates first.

### 2. Scan Existing Tag Taxonomy
Run `scripts/scan_tags.py <vault-path>` to collect all tags and their frequencies. Output: JSON with tag list sorted by frequency.

### 3. Discover Untagged Candidates
Run `scripts/find_untagged.py <vault-path>` to identify documents needing tags:
- No frontmatter
- No `tags` field in frontmatter
- Empty `tags` field

Configurable: `--include-weak-tags` flag to also include documents with existing tags for optimization.

### 4. Read and Recommend Tags
Agent reads each candidate's title, frontmatter, and body. Selects 1-2 tags from existing tag list. Only proposes new tags (marked "new") when no existing tag fits.

### 5. Present Suggestion List
Table format: `file path → recommended tags (existing/new) → brief reason`. User reviews batch before any writes.

### 6. Apply Changes
After user confirmation, write tags into frontmatter:
- No frontmatter → create frontmatter block with tags
- No tags field → add tags field to existing frontmatter
- Empty tags → populate tags list
- Optimization mode → append only, never remove existing tags
- Preserve all other frontmatter fields unchanged

### 7. Verify and Report
Report: new tags per document, existing vs new tag ratio, skipped documents with reasons.

## Scripts

### `scripts/scan_tags.py`
- Input: vault path
- Behavior: recursively scan `.md` files, skip hidden dirs (`.obsidian`, `.claude`, etc.), parse frontmatter `tags` field
- Output: `{"tags": [{"name": "ai", "count": 36}, ...], "total_files": 173, "tagged_files": 161}`
- Sorted by frequency descending
- Optional `--include-inline` flag to also detect `#tag` in body text
- Standard library only (regex-based frontmatter parsing, no pyyaml)

### `scripts/find_untagged.py`
- Input: vault path, optional `--include-folder`, `--exclude-folder`, `--include-weak-tags`
- Output: `[{"path": "...", "title": "...", "reason": "no-frontmatter|no-tags-field|empty-tags", "preview": "first 200 chars"}, ...]`
- Sorted by folder then filename
- Standard library only, read-only (never writes files)

## Tagging Guidelines

- Prefer existing tags over new ones — always
- 1-2 tags per document, max 3
- New tags: lowercase English, hyphen-separated (e.g., `prompt-engineering`)
- Never use author handles as tags (e.g., `@Russell3402`)
- Never modify document body — only frontmatter `tags` field
- Optimization mode: append only, never remove existing tags
- Must present suggestion list and wait for user confirmation before writing

## Directory Structure

```
skills/obsidian-auto-tagger/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── tagging-guidelines.md
│   └── batch-mode.md
└── scripts/
    ├── scan_tags.py
    └── find_untagged.py
```

## Ground Rules

- Never overwrite existing user-authored tags
- Never modify document body content
- Always present suggestions before applying
- Prefer deterministic scanning over heuristic guessing
- If confidence is low, skip the document and report why
