# lingua-cards

Standalone durable card catalog for the **Deutsch Lesson Cards** ChatGPT plugin.

This repository is intentionally independent of any single ChatGPT Project or tutor repository. It stores unique German vocabulary cards, cross-lesson provenance, export metadata, and the deduplication index used before generating AnkiDroid decks.

## Core rules

- one canonical card per normalized German lemma or phrase;
- deduplicate before creating any new card;
- repeated items update lesson/date/source metadata instead of creating duplicates;
- Anki/AnkiDroid owns review scheduling; this repository does not mirror SRS state;
- operational card writes use the `runtime/cards` branch;
- development changes use branch -> PR -> merge;
- never claim a card batch was saved until the GitHub write is verified by read-back.

## Android target

Canonical client: **AnkiDroid**.

Exports:
- `.apkg` — primary deck package;
- UTF-8 `.tsv` — backup/export interchange;
- `.docx` / `.pdf` — lesson verb tables.

## Privacy

This repository currently contains only schemas and empty metadata. Before real lesson/card data is written, repository visibility should be **private**, because lesson metadata and source references may reveal personal study history.

See `START_HERE.md` and `docs/CARD_WORKFLOW.md`.
