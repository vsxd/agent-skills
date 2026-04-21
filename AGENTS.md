# AGENTS.md

This repository is a public `skills.sh`-compatible collection of agent skills.

## Repository Rules

- Keep skills in `skills/<skill-name>/`.
- Match the directory name and frontmatter `name` exactly.
- Write for public, portable use. Do not assume private repos, local shell aliases, or one user's filesystem layout.
- Keep `SKILL.md` concise. Move detailed heuristics, examples, and edge cases into `references/`.
- Add `agents/openai.yaml` for UI metadata when publishing a skill.
- Prefer capability-based instructions over one vendor-specific tool unless the skill truly depends on it.
- Before shipping a change, run `npx skills add . --list` from the repo root.
