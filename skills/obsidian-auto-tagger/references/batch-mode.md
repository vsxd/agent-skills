# Batch Mode

Use this file when tagging many untagged notes across a vault or folder.

## Sequence

1. Run a full scan and save or inspect the JSON output.
2. Review the top existing tags before assigning any new tags.
3. Group untagged notes by folder or topic to keep decisions consistent.
4. Read 5-10 candidate notes at a time.
5. Present a suggestion table with file, suggested tags, confidence, and reason.
6. Create a small assignment JSON for the approved batch.
7. Run `apply` without `--write` and inspect the dry-run output.
8. Run `apply --write` only when the dry run is correct.
9. Rescan after each batch.

## Suggestion Table

```text
| File | Current Tags | Suggested Tags | Confidence | Reason |
| --- | --- | --- | --- | --- |
| Notes/example.md | (none) | ai, engineering | high | Main topic matches existing tags |
| Notes/strategy.md | (none) | business, strategy (new) | medium | Existing business tag fits; strategy is reusable |
```

Mark new tags as `new`. Do not include low-confidence notes in the assignment JSON; list them as skipped.

## Safety Rules

- Do not tag plugin, cache, local skill, template, attachment, or generated files.
- Do not overwrite notes that already have tags unless the user explicitly asks for retagging.
- Never write before a reviewable suggestion list and a clean dry run.
- Prefer leaving a note untagged over assigning misleading tags.
- Stop on path mismatches, missing files, or frontmatter parse surprises.

## Good Final Summary

Report:

- number of notes scanned
- number of tagged notes before and after
- tags reused most often
- new tags introduced, if any
- skipped notes and why they were skipped
- verification command and result
