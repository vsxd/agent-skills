---
name: obsidian-auto-tagger
description: Add suitable tags to untagged Markdown notes in an Obsidian vault. Use when a vault, folder, or note should be audited for missing tags, existing vault tags should be inventoried first, recommendations should be reviewed in batches, and new tags should be introduced only when no existing tag fits.
license: MIT
compatibility: Best in agents that can read and edit local Markdown files inside an Obsidian-compatible vault.
metadata:
  author: vsxd
  version: "1.0.0"
---

# Obsidian Auto Tagger

Add useful tags to untagged Obsidian notes while preserving the vault's existing tag vocabulary.

## Use This Skill When

- The user points at an Obsidian vault, folder, or note and asks to add missing tags.
- Notes lack frontmatter, lack a `tags` field, have an empty `tags` field, or have no inline tags.
- Existing vault tags should be reused before creating new tags.
- Tags should be written as Obsidian-compatible frontmatter `tags` entries.

## Do Not Use

- The user wants to redesign the entire taxonomy from scratch.
- Notes are generated, cache, plugin, template, attachment, or local skill files.
- Existing tags are already maintained and the user has not requested optimization.
- The note topic is too ambiguous to tag confidently.

## Workflow

1. Determine scope.
   For a single note, read it directly and still inspect nearby vault tags when possible. For a folder or vault, run the bundled scanner first. Run commands from this skill directory or replace `scripts/...` with the script's absolute path. The script uses Python 3 standard library only.

   ```bash
   python3 scripts/vault_tag_inventory.py scan /path/to/vault --format json
   ```

2. Inventory the existing taxonomy before assigning tags.
   Prefer high-frequency, semantically matching tags already present in the vault. Use [references/tag-selection.md](references/tag-selection.md).

3. Read candidates and recommend tags in small batches.
   For each untagged note, read the title, frontmatter, headings, and meaningful body text. Choose 1-3 tags from the existing list when possible; use 4 only for notes with distinct retrieval paths. Mark any proposed new tag as `new` in the recommendation.

4. Present a reviewable suggestion list before editing.

   ```text
   | File | Suggested Tags | Confidence | Reason |
   | --- | --- | --- | --- |
   | Notes/example.md | ai, research | high | Matches existing tags and note topic |
   ```

5. Dry-run writes first.
   Put approved assignments in JSON and validate the exact files that would change:

   ```bash
   python3 scripts/vault_tag_inventory.py apply /path/to/vault assignments.json
   ```

6. Apply only after the dry run is clean.

   ```bash
   python3 scripts/vault_tag_inventory.py apply /path/to/vault assignments.json --write
   ```

7. Rescan and summarize.
   Confirm fewer untagged notes remain and report reused tags, new tags, skipped notes, and any ambiguous cases. Use [references/batch-mode.md](references/batch-mode.md).

## Assignment Format

```json
{
  "assignments": [
    {"path": "Notes/example.md", "tags": ["ai", "research"]}
  ]
}
```

Paths are relative to the vault root. The apply command is dry-run by default and skips files that already have frontmatter or inline tags unless `--force` is provided.

## Ground Rules

- Preserve existing frontmatter and note content.
- Prefer existing tags over new tags.
- Never remove existing user-authored tags.
- Use concise, reusable tags rather than one-off sentence-like tags.
- Do not infer sensitive or private attributes from personal notes.
- Skip low-confidence notes instead of inventing misleading tags.

## Reference Files

- [references/tag-selection.md](references/tag-selection.md): tag reuse, new-tag criteria, and note-reading heuristics.
- [references/batch-mode.md](references/batch-mode.md): vault-scale sequencing, dry-run checks, and final reporting.
