# Source Recovery

Use this file when a clipping note points at the wrong URL, an intermediate page, or an incomplete rendering.

## Primary Goal

Recover the page or document the clipping was supposed to preserve, not merely the first readable page returned by the URL.

## Common Cases

### Normal article page

- Prefer the canonical article URL when it is exposed.
- Extract title, author, published date, description, and body in one clean pass when possible.

### Redirect, archive, or hub page

- Use the note title, filename, preview text, and source domain to locate the intended article.
- Navigate to the matching article before extraction.
- Do not save the hub or archive page itself unless the note clearly targeted it.

### Mobile share or browser clipper partial capture

- Treat saved teaser text as a disambiguation hint.
- If the note body is only the first paragraph or a preview card, still recover the full article when the source is clear.

### Social posts and threads

- Prefer platform-aware extraction when available.
- If rendered-page extraction is the only option, confirm the visible post matches the note before using it.
- If login walls or dynamic loading block reliable access, stop instead of guessing.

### Mirrors, newsletters, and syndication

- Prefer the original or canonical article over mirrors when both are available.
- Keep the mirrored source only when the original is unavailable or the note clearly references the mirror.

### PDF and document links

- If the source is a PDF or document file, extract that document directly instead of forcing article-reader logic.
- Preserve the original document URL and identity in metadata.

### Paywalled, deleted, or inaccessible pages

- Do not invent missing text.
- Keep the note unchanged or annotate the failure if the surrounding workflow allows it.

## Confidence Checks

- The recovered title is compatible with the filename or note title.
- The recovered page topic matches the saved note context.
- The extracted body is substantive and not just navigation chrome, comments, or unrelated landing copy.
