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
npx skills add vsxd/agent-skills --skill fill-link-clippings
```

List the skills in this repo:

```bash
npx skills add vsxd/agent-skills --list
```

## Available Skills

| Skill | Description |
| --- | --- |
| [`fill-link-clippings`](./skills/fill-link-clippings) | Repairs Markdown or Obsidian clipping notes that captured only a link or thin preview instead of the actual article. |

## Repository Layout

```text
.
├── .github/workflows/validate.yml
├── skills/
│   └── fill-link-clippings/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
└── README.md
```

## Authoring Guidelines

- Put each public skill in `skills/<skill-name>/`.
- Keep `SKILL.md` focused on activation and execution.
- Put detailed edge cases and long examples in `references/`.
- Validate discoverability with `npx skills add . --list`.
- Prefer portable instructions that work across multiple agents and toolchains.
