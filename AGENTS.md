# AGENTS.md

Mandatory rules for humans and agents working in this repository.

## Development workflow

`master` is integration-only. Never write development changes directly to `master`.

For schemas, docs, validation, CI, or repository contracts:

1. start from latest `master`;
2. create a dedicated branch;
3. make focused changes;
4. run `python scripts/validate_repo.py`;
5. open a PR targeting `master`;
6. merge only when the task/user authorizes it.

Always include the direct clickable PR URL in the user-facing report.

## Runtime card workflow

Operational lesson-card state is separate from development history.

Runtime writes:
- branch: `runtime/cards`;
- allowed paths:
  - `cards/CARD-*.json`
  - `cards/index.json`
  - `exports/cards/*.json`
  - `exports/verbs/*.json`;
- deduplicate through `cards/index.json` before creating cards;
- use stable IDs and deterministic Anki GUIDs;
- write one lesson batch atomically when possible;
- read back after write before claiming success.

## Privacy guard

Real lesson/card data must not be persisted while the repository is public. Before runtime writes, verify repository visibility. If visibility is not private, stop and ask the user to make the repository private.

## Source boundary

Card extraction may use the current chat/project lesson: screenshots, uploaded files, exercises, verified video/manuscript material, scenarios, questions, answers, and corrections.

Do not invent unseen or unheard source material.

## SRS boundary

GitHub owns card identity, deduplication, provenance, and export metadata.

Anki/AnkiDroid owns scheduling, intervals, due dates, FSRS/ease state, and review history.
