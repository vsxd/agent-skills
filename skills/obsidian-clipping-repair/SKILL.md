---
name: obsidian-clipping-repair
description: Repair and enrich Obsidian clipping notes imported from browser extensions, mobile share sheets, or other Markdown clipping flows. Use when notes in a vault's `Clippings`-like folders contain only a source URL, thin preview text, partial metadata, broken filenames, or incomplete bodies and need their source content, metadata, and note structure normalized without damaging real user-authored notes.
license: MIT
compatibility: Best in agents that can read local Markdown files, browse or extract web pages, and edit notes inside an Obsidian-compatible vault.
metadata:
  author: vsxd
  version: "2.0.0"
---

# Obsidian Clipping Repair

Repair broken or thin clipping notes inside an Obsidian vault.

## Use This Skill When

- Notes were created by a browser clipper, mobile share flow, or clipping extension.
- The saved Markdown contains only a link, a title plus teaser, partial metadata, or a body that is obviously incomplete.
- The user wants vault-safe cleanup: better filenames, normalized frontmatter, recovered article content, and optional media import.

## Do Not Use

- The note already contains substantial human writing, annotation, or curation.
- The intended source cannot be matched confidently.
- Repair would require fabricating missing article text.

## Workflow

1. Determine scope.
   If the user names one note, inspect that note directly. If the user points at a vault or folder, inventory likely candidates first. Use [references/candidate-detection.md](references/candidate-detection.md).

2. Preserve note evidence before rewriting.
   Keep the current filename, title, source URL, existing frontmatter, and any short preview text. These are disambiguation hints, not noise.

3. Recover the true source.
   Resolve redirects, archive pages, hub pages, mirrors, and social-post links to the page the note actually intended. Use [references/source-recovery.md](references/source-recovery.md).

4. Extract the article or document with the lightest reliable method.
   Prefer one clean extraction path over repeated scraping attempts. Use structured page readers when available; fall back to rendered-page navigation only when needed.

5. Rewrite the note conservatively.
   Normalize frontmatter, replace only the broken placeholder body, preserve useful user-authored text, and keep media organized predictably. Use [references/note-shaping.md](references/note-shaping.md).

6. Rename and verify.
   Rename the file only after the final title is stable. Stop on collisions, mismatches, or low-confidence recoveries.

7. Batch safely when working across a vault.
   Process candidates in small groups, keep a summary of repaired and skipped notes, and do not let one ambiguous clip block the entire batch. Use [references/batch-mode.md](references/batch-mode.md).

## Built-In Helper

For vault-wide work, use the bundled candidate scanner to rank likely broken clipping notes:

```bash
python3 skills/obsidian-clipping-repair/scripts/find_candidates.py /path/to/vault --format json --top 50
```

This scanner is a triage aid, not authority. Review high-scoring candidates before rewriting them.

## Ground Rules

- Prefer canonical URLs without redirect wrappers or tracking parameters.
- Prefer deterministic note cleanup over clever but fragile scraping.
- Never overwrite meaningful user writing just because a note looks short.
- Never replace a note with unrelated page content.
- If confidence is low, leave the original note intact and report why.

## Reference Files

- [references/candidate-detection.md](references/candidate-detection.md): candidate heuristics, exclusions, and scanner usage.
- [references/source-recovery.md](references/source-recovery.md): source resolution for redirects, mirrors, social posts, PDFs, and inaccessible pages.
- [references/note-shaping.md](references/note-shaping.md): frontmatter, attachments, rename rules, and final validation.
- [references/batch-mode.md](references/batch-mode.md): vault-scale sequencing and reporting.
