# Tag Selection

Use this file when deciding which tags to assign to an untagged Obsidian note.

## Reuse First

- Start from the scanner's `existing_tags` list.
- Prefer tags that already appear often and match the note's actual topic.
- Reuse a low-frequency tag when it is clearly more precise than a popular broad tag.
- Keep existing spelling, casing, and slash hierarchy unless the vault already mixes styles.
- Match the vault's style before applying generic style rules. If the vault has no clear style, prefer lowercase hyphen-separated tags.

## When To Create A New Tag

Create a new tag only when:

- no existing tag describes the note's main subject or durable use case
- the note represents a recurring category likely to apply to future notes
- the new tag is short, stable, and not a synonym of an existing tag

Avoid new tags for one-off filenames, people mentioned only incidentally, temporary moods, or details that belong in links or prose.

Mark new tags clearly in the suggestion list so the user can review taxonomy expansion before any write.

## Reading A Note

Look for durable signals in this order:

1. frontmatter fields such as `title`, `source`, `author`, `type`, or `category`
2. the filename and parent folders
3. headings and repeated terms
4. the first meaningful paragraphs
5. outgoing links and embedded resources

Ignore navigation chrome, clipped boilerplate, timestamps, and incidental URL fragments.

## Tag Count

- Use 1 tag for narrow utility notes.
- Use 1-2 tags for most notes with a clear topic.
- Use 3 tags when topic, type, and project/context each add retrieval value.
- Use 4 tags only when each tag adds a distinct retrieval path.
- Skip the note if no tag can be justified from its content.

## What Not To Tag

- Author handles or usernames unless the vault already uses them as deliberate entity tags.
- Platform names unless the platform is the note's main subject.
- Generic terms that apply to most notes in the vault.
- Overly specific release, API, or filename details that are unlikely to be reused.

## Confidence

- High: the note has a clear topic and matching existing tag.
- Medium: the topic is clear but requires a low-frequency tag or one new reusable tag.
- Low: the topic is unclear, too broad, or only implied. Skip and report the reason.

## Sensitive Notes

Do not infer or add tags for sensitive personal attributes, medical status, finances, identity, or private relationships unless the user explicitly asks and the note itself already uses that taxonomy.
