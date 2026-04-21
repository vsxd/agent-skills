# Batch Mode

Use this file when the user wants to clean up many clipping notes across a vault or folder.

## Sequence

1. Inventory likely candidates first instead of editing blindly.
2. Review the highest-confidence notes and group them by source type when useful.
3. Repair notes in small batches so ambiguous cases do not contaminate the whole run.
4. Verify each note before moving on.
5. End with a short summary of repaired, skipped, and failed notes.

## Safety Rules

- Prefer skipping one ambiguous note over corrupting several.
- Keep per-note checkpoints so a partial batch can stop cleanly.
- Do not close unrelated browser tabs or windows while resolving sources.
- Preserve the vault's existing attachment and naming conventions when they are already consistent.

## Good Summary Shape

Report:

- repaired notes
- skipped notes and why they were skipped
- unresolved sources or login/paywall blockers
- any attachment folders created or reused
