# agent-skills

Portable agent skills for Codex, Claude Code, and other AI coding agents.

This repository is structured for the open `skills.sh` ecosystem and follows the `npx skills` repository layout. Skills live under [`skills/`](./skills), each skill is self-contained, and detailed guidance stays in per-skill `references/` files so the main instructions remain small and activation-friendly.

## Install

Install the full collection:

```bash
npx skills add vsxd/agent-skills
```

Install a specific skill:

```bash
npx skills add vsxd/agent-skills --skill obsidian-clipping-repair
npx skills add vsxd/agent-skills --skill obsidian-vault-auto-tagger
```

List the skills in this repo:

```bash
npx skills add vsxd/agent-skills --list
```

## Available Skills

| Skill | Description |
| --- | --- |
| [`obsidian-clipping-repair`](./skills/obsidian-clipping-repair) | Repairs and enriches Obsidian clipping notes imported from browsers or mobile clipping flows when the saved Markdown is thin, broken, or incomplete. |
| [`obsidian-vault-auto-tagger`](./skills/obsidian-vault-auto-tagger) | Adds suitable tags to untagged Obsidian notes by inventorying the vault's existing tag vocabulary first and preferring those tags before introducing new ones. |

## Repository Layout

```text
.
├── .github/workflows/validate.yml
├── skills/
│   ├── obsidian-clipping-repair/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   ├── references/
│   │   └── scripts/
│   └── obsidian-vault-auto-tagger/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       └── scripts/
└── README.md
```

## Authoring Guidelines

- Put each public skill in `skills/<skill-name>/`.
- Keep `SKILL.md` focused on activation and execution.
- Put detailed edge cases and long examples in `references/`.
- Validate discoverability with `npx skills add . --list`.
- Prefer portable instructions that work across multiple agents and toolchains.
