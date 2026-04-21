# Output Shape

Use this file when rewriting the repaired note.

## Recommended Frontmatter

Keep only fields that are known and useful:

- `title`
- `source`
- `author`
- `published`
- `description`
- `site_name` or `domain`
- `tags`

Do not fabricate fields just to fill space.

## Body Pattern

Use a clean note structure:

1. Optional short intro only if it already existed and still helps.
2. Recovered article body in readable Markdown.
3. A `## Media` section only when local images materially improve the note.

Trim duplicated title blocks or author lines when the same data already exists in frontmatter.

## Attachments

- If the project already has a media convention, follow it.
- Otherwise use `attachments/link-clippings/<slug>/`.
- Keep each article's assets together so the note remains portable and easy to verify.

## Filename Rules

- Rename the note to match the final article title as closely as the filesystem allows.
- Sanitize filesystem-hostile characters without mutating metadata `title`.
- Stop on filename collisions and resolve them explicitly.

## Final Verification

- The note is no longer a link-only placeholder.
- The source URL points to the intended article or document.
- The title and body match each other.
- Any preserved user-written content remains intact.
- Media links resolve correctly if media was embedded.
