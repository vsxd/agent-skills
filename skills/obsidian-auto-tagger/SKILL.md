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
- Documents lack frontmatter, have no `tags` field, or have empty tags

## Do Not Use

- Documents already have well-maintained tags and user hasn't requested optimization
- Non-Markdown files (Excalidraw scripts, attachments, etc.)

## Workflow

### 1. Determine Scope

Single document → process directly. Vault/folder → scan for candidates first.

### 2. Scan Existing Tag Taxonomy

```bash
python3 skills/obsidian-auto-tagger/scripts/scan_tags.py /path/to/vault --format json
```

Build the tag vocabulary. Prefer existing tags over creating new ones.

### 3. Discover Untagged Candidates

```bash
python3 skills/obsidian-auto-tagger/scripts/find_untagged.py /path/to/vault --format json
```

Identifies: no frontmatter, no `tags` field, or empty `tags` field.

Optional: `--include-folder Clippings` to scan specific folders only.

### 4. Read and Recommend Tags

For each candidate, read title, frontmatter, and body. Select 1-2 tags from existing list. Only propose new tags (marked "new") when no existing tag fits.

See [references/tagging-guidelines.md](references/tagging-guidelines.md).

### 5. Present Suggestion List

```
| File | Suggested Tags | Reason |
|------|----------------|--------|
| ... | ... | ... |
```

Wait for user approval before writing any changes.

### 6. Apply Changes

After confirmation, write tags into frontmatter:
- No frontmatter → create frontmatter block with tags
- No tags field → add tags field to existing frontmatter
- Preserve all other frontmatter fields unchanged

### 7. Verify and Report

Report tags applied, new tags created, and skipped documents with reasons.

See [references/batch-mode.md](references/batch-mode.md).

## Scripts

```bash
# Collect existing tag taxonomy
python3 skills/obsidian-auto-tagger/scripts/scan_tags.py <vault> [--include-inline] [--format json|text]

# Find documents without tags
python3 skills/obsidian-auto-tagger/scripts/find_untagged.py <vault> [--include-folder DIR] [--exclude-folder DIR] [--format json|text]
```

## Ground Rules

- Prefer existing tags over new ones — always
- Never overwrite existing user-authored tags
- Never modify document body content
- Always present suggestions before applying
- Target 1-2 tags per document, max 3
- If confidence is low, skip and report why

## Reference Files

- [references/tagging-guidelines.md](references/tagging-guidelines.md): tag selection rules, style, confidence levels
- [references/batch-mode.md](references/batch-mode.md): batch workflow, safety rules, reporting
