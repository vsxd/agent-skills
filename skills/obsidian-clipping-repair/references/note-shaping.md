# Note Shaping

Use this file when rewriting a repaired clipping note.

## Frontmatter

Keep only fields that are known and useful. Typical fields:

- `title`
- `source`
- `author`
- `published`
- `description`
- `site_name` or `domain`
- `tags`

Preserve existing fields that are still correct and useful to the vault. Do not fabricate metadata.

## Body Shape

Prefer a simple structure:

1. Keep a short intro only if it already existed and still adds value.
2. Insert the recovered article or document body in readable Markdown.
3. Add a `## Media` section only when local assets materially improve the note.

Trim duplicated title blocks or author lines when the same data already appears in frontmatter.

## Attachments

- Follow the vault's existing media convention when one already exists.
- Otherwise use `attachments/clippings/<slug>/`.
- Keep each note's assets grouped together so links remain easy to verify.

## Filenames

- Rename the note only after the final title is stable.
- Keep metadata `title` human-readable.
- Sanitize only the filesystem filename.
- Stop on filename collisions instead of overwriting another note.

## Final Verification

- The note is no longer a placeholder clipping.
- The source URL points to the intended article or document.
- The title and body are consistent with each other.
- Any preserved user-authored text is still intact.
- Media links resolve if media was embedded.
