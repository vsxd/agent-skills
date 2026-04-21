# Source Recovery

Use this file when the saved URL does not immediately open the intended article.

## Common Cases

### Normal article page

- Prefer the page's canonical URL if available.
- Extract title, author, published date, description, and body in one pass when your tools support it.

### Redirect, archive, or hub page

- Use the note title, filename, and preview text to identify the intended article.
- Navigate to the matching article before extracting content.
- Do not save the hub page itself unless the note clearly intended that page.

### X or other social posts

- Prefer platform-aware extraction when your current toolset supports it.
- If not, use rendered-page extraction only when the page content is visible and confidently matches the note.
- If login walls or dynamic loading prevent a reliable match, stop instead of guessing.

### Newsletter or blog mirrors

- Prefer the original or canonical article over mirrors when both are available.
- Keep the mirror only when the note clearly references that source or the original is unavailable.

### PDF source

- If the URL points to a PDF, extract the PDF text instead of trying to force article-reader logic.
- Preserve the PDF URL and document identity in metadata.

### Paywalled or inaccessible pages

- Do not invent missing text.
- Leave the original note unchanged or annotate the failure if the surrounding workflow allows it.

## Confidence Checks

- The recovered title is compatible with the note title or filename.
- The recovered page topic matches the saved note context.
- The body is substantive and not just nav chrome, comments, or unrelated landing copy.
