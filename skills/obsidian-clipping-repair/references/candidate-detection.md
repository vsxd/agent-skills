# Candidate Detection

Use this file when deciding which Markdown notes in an Obsidian vault are safe targets for repair.

## Strong Signals

- The note lives in a `Clippings`, `clippings`, `clips`, or similar capture folder.
- The body is mostly a single URL, Markdown link, preview card, or one short teaser paragraph.
- Frontmatter includes a `source`, `url`, `link`, or similar field, but the body is still thin.
- The filename looks auto-generated, truncated, or disconnected from the actual article title.

## Exclusions

Do not treat a note as a repair candidate when it already contains:

- substantial commentary or annotations
- curated excerpts from multiple sources
- meeting notes, highlights, tasks, or follow-up bullets unrelated to a broken clip
- obvious hand-edited structure that should be preserved as-is

## Scanner

For vault-wide triage, use the bundled scanner:

```bash
python3 skills/obsidian-clipping-repair/scripts/find_candidates.py /path/to/vault --format json --top 50
```

The scanner ranks notes using portable heuristics:

- clipping-like folder paths
- short bodies
- URL-dominant content
- frontmatter source fields
- title-only or preview-like bodies

Review high-scoring candidates before editing them.

## Practical Rule

If deleting the current body would erase meaningful user thinking, it is not a safe candidate.
