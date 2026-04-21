---
name: fill-link-clippings
description: Repair Markdown or Obsidian clipping notes that captured only a link, redirect, or thin preview instead of the real article. Use when a note in a Clippings-like folder is mostly a URL or short teaser and needs its true title, metadata, body, and media restored from the source page without overwriting real user-written notes.
license: MIT
compatibility: Best in agents that can read local Markdown files, browse pages, and edit notes.
metadata:
  author: vsxd
  version: "1.0.0"
---

# Fill Link Clippings

Repair clipping notes that are effectively placeholders rather than finished notes.

## When to Use

- The note body is mostly one link after optional frontmatter.
- The note contains only a title, preview blurb, or one or two setup lines plus a source URL.
- The saved URL may point to a redirect, archive page, site index, or wrong landing page, but the filename or note title still hints at the intended article.

## Do Not Use

- The note already contains substantial commentary or curated excerpts.
- The source page cannot be matched confidently to the note.
- Repair would overwrite user writing instead of filling a broken clip.

## Workflow

1. Decide whether the note is still a placeholder.
   Treat short link-dominant notes as repair candidates, but leave real notes alone.

2. Capture disambiguation hints before browsing.
   Keep the existing filename, note title, source URL, tags, and any short preview text. These are often the only clues when the saved URL is generic.

3. Resolve the real source page.
   Prefer the canonical article page over archive, redirect, search, or home pages. If the saved link is wrong, use the note title and visible context to navigate to the intended page. See [references/source-recovery.md](references/source-recovery.md).

4. Extract the article body and metadata.
   Prefer the simplest reliable path available in the current agent:
   - a direct web-to-markdown or article reader tool
   - structured page extraction that returns title, author, and published date
   - browser automation only when the page is JS-heavy or requires navigation to the final article

5. Rewrite the note conservatively.
   Preserve useful frontmatter, replace the placeholder body with the recovered content, and embed downloaded media only when it improves the note. Use the output pattern in [references/output-shape.md](references/output-shape.md).

6. Rename the file after the final title is known.
   Keep metadata `title` human-readable. Sanitize only the filesystem filename. Stop on collisions instead of overwriting another note.

7. Verify before finishing.
   Confirm the repaired note matches the intended source, is no longer link-only, and still preserves any original user-authored material that should remain.

## Ground Rules

- Prefer canonical URLs without redirect wrappers or tracking parameters.
- Prefer one high-confidence extraction over multiple noisy passes.
- Never replace a note with unrelated page content just because a URL returned something readable.
- Never fabricate missing metadata or article text.
- If confidence is low, stop and leave the original note intact.

## Reference Files

- [references/source-recovery.md](references/source-recovery.md): URL classes, bad-link recovery, and source-specific edge cases.
- [references/output-shape.md](references/output-shape.md): frontmatter fields, attachment layout, filename rules, and final verification checklist.
