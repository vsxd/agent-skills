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

- File read errors: skip and report
- Frontmatter parse errors: skip and report
- Low confidence: skip and report
- User rejects suggestion: skip that document

## Reporting

Final report should include:
- Total candidates found
- Tags applied (count)
- New tags created (list them)
- Skipped documents (count and reasons)
- Any errors encountered

## Optimization Mode

When processing documents with existing tags:
- Append suggested tags to existing ones
- Never remove existing tags
- Mark as "optimization" in suggestions
