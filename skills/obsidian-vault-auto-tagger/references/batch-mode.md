# Batch Mode

Use this file when tagging many untagged notes across a vault or folder.

## Sequence

1. Run a full scan and save or inspect the JSON output.
2. Review the top existing tags before assigning any new tags.
3. Group untagged notes by folder or topic to keep decisions consistent.
4. Create a small assignment JSON for one batch.
5. Run `apply` without `--write` and inspect the dry-run output.
6. Run `apply --write` only when the dry run is correct.
7. Rescan after each batch.

## Safety Rules

- Do not tag plugin, cache, local skill, template, attachment, or generated files.
- Do not overwrite notes that already have tags unless the user explicitly asks for retagging.
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
