# Tagging Guidelines

Rules for selecting and creating tags when auto-tagging Obsidian documents.

## Tag Selection Priority

1. **Always prefer existing tags** — scan the vault's tag taxonomy first
2. Only create new tags when no existing tag fits the document's main topic
3. When creating new tags, mark them as "new" in suggestions for user review

## Tag Count

- Target: 1-2 tags per document
- Maximum: 3 tags
- Focus on the document's primary topic, not every mentioned concept

## Tag Style

- Lowercase English words
- Hyphen-separated for multi-word tags (e.g., `prompt-engineering`)
- No spaces, underscores, or special characters
- Match the existing tag style in the vault

## What NOT to Tag

- Author handles (e.g., `@Russell3402`, `@username`)
- Platform names unless they're the document's main topic
- Generic terms that apply to most documents
- Overly specific terms that won't be reused

## Tag Granularity

Prefer coarse-grained topic tags:
- Good: `ai`, `engineering`, `business`, `java`
- Acceptable: `distributed-systems`, `prompt-engineering`
- Too specific: `gpt4-turbo-api`, `react-18-hooks`

## Reading Documents

When analyzing a document for tagging:
1. Read the title and frontmatter first
2. Skim the first 2-3 paragraphs for main topic
3. Check for explicit topic statements or summaries
4. Don't over-index on passing mentions

## Confidence Levels

- **High confidence**: Document clearly about a topic with matching existing tag
- **Medium confidence**: Document topic matches but requires new tag
- **Low confidence**: Document topic unclear or too broad — skip and report

## Safety Rules

- Never modify document body content
- Never remove existing tags (append-only in optimization mode)
- Preserve all other frontmatter fields unchanged
- Skip documents where confidence is low
