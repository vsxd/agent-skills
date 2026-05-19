# agent-skills

[![skills.sh](https://skills.sh/b/vsxd/agent-skills)](https://skills.sh/vsxd/agent-skills)

Portable agent skills for Codex, Claude Code, and other AI coding agents.

This repository is structured for the open `skills.sh` ecosystem and follows the `npx skills` repository layout. Skills live under [`skills/`](./skills), each skill is self-contained, and detailed guidance stays in per-skill `references/` files so the main instructions remain small and activation-friendly.

## Install

Install the full collection directly from GitHub:

```bash
npx skills add vsxd/agent-skills
```

Install a specific skill by name:

```bash
npx skills add vsxd/agent-skills --skill <skill-name>
```

Browse the public skills.sh page:

```text
https://skills.sh/vsxd/agent-skills
```

List the skills in this repo:

```bash
npx skills add vsxd/agent-skills --list
```

## Discover Skills

Use the CLI to see the current skills published by this repo:

```bash
npx skills add vsxd/agent-skills --list
```

## Repository Layout

```text
.
├── .github/workflows/validate.yml
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       └── scripts/
└── README.md
```

## Authoring Guidelines

- Put each public skill in `skills/<skill-name>/`.
- Match each directory name exactly with the `name` field in `SKILL.md` frontmatter.
- Keep `SKILL.md` focused on activation and execution.
- Put detailed edge cases and long examples in `references/`.
- Add `agents/openai.yaml` for agent UI metadata when publishing a skill.
- Validate discoverability with `npx skills add . --list`.
- Prefer portable instructions that work across multiple agents and toolchains.

## Publishing Checklist

Before sharing a new skill publicly:

1. Confirm the skill lives at `skills/<skill-name>/SKILL.md`.
2. Confirm `SKILL.md` frontmatter includes `name`, `description`, `license`, and compatibility notes.
3. Keep helper scripts, examples, and references inside the skill directory.
4. Run local discovery:

   ```bash
   npx skills add . --list
   ```

5. Push to GitHub, then install by repository name:

   ```bash
   npx skills add vsxd/agent-skills --skill <skill-name>
   ```
