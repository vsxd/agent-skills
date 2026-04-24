---
name: obsidian-vault-auto-tagger
description: Add suitable tags to untagged Markdown notes in an Obsidian vault. Use when a vault or folder should be audited for notes without frontmatter or inline tags, existing vault tags should be inventoried first, and new tags should be introduced only when no existing tag fits the note.
license: MIT
compatibility: Best in agents that can read and edit local Markdown files inside an Obsidian-compatible vault.
metadata:
  author: vsxd
  version: "1.0.0"
---

# Obsidian Vault Auto Tagger

Add appropriate tags to untagged Obsidian notes while preserving the vault's existing tag vocabulary.

## Use This Skill When

- The user wants every untagged note in a vault or folder to receive useful tags.
- Existing vault tags should be reused before creating new tags.
- Tags should be written as Obsidian-compatible frontmatter `tags` entries.

## Do Not Use

- The user wants to redesign the entire taxonomy from scratch.
- Notes are generated/cache/plugin files rather than user notes.
- The note topic is too ambiguous to tag confidently.

## Workflow

1. Inventory the vault before editing.
   Run the bundled scanner to collect existing tags and untagged notes:

   ```bash
   python3 skills/obsidian-vault-auto-tagger/scripts/vault_tag_inventory.py scan /path/to/vault --format json --top-untagged 100
   ```

2. Review the existing tag list.
   Prefer high-frequency, semantically matching tags already present in the vault. Use [references/tag-selection.md](references/tag-selection.md).

3. Assign tags in small batches.
   For each untagged note, choose 1-4 tags from the existing list when possible. Add a new tag only when existing tags do not describe the note well.

4. Dry-run writes first.
   Put assignments in JSON and validate the exact files that would change:

   ```bash
   python3 skills/obsidian-vault-auto-tagger/scripts/vault_tag_inventory.py apply /path/to/vault assignments.json
   ```

5. Apply only after the dry run is clean.

   ```bash
   python3 skills/obsidian-vault-auto-tagger/scripts/vault_tag_inventory.py apply /path/to/vault assignments.json --write
   ```

6. Rescan and summarize.
   Confirm fewer untagged notes remain and report reused tags, new tags, skipped notes, and any ambiguous cases. Use [references/batch-mode.md](references/batch-mode.md).

## Assignment Format

```json
{
  "assignments": [
    {"path": "Notes/example.md", "tags": ["ai", "research"]}
  ]
}
```

Paths are relative to the vault root. The apply command skips files that already have tags unless `--force` is provided.

## Ground Rules

- Preserve existing frontmatter and note content.
- Prefer existing tags over new tags.
- Use concise, reusable tags rather than one-off sentence-like tags.
- Do not infer sensitive or private attributes from personal notes.
- Skip ambiguous notes instead of inventing misleading tags.

## Reference Files

- [references/tag-selection.md](references/tag-selection.md): tag reuse, new-tag criteria, and note-reading heuristics.
- [references/batch-mode.md](references/batch-mode.md): vault-scale sequencing, dry-run checks, and final reporting.
