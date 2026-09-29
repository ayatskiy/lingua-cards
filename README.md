# lingua-cards

Standalone, project-agnostic source of truth for German flashcards used by the **Deutsch Lesson Cards** ChatGPT plugin.

This repository stores **flashcards only**. It does not store lesson history, chat/source provenance, verb study tables, DOCX/PDF verb files, or review progress.

## Storage model

```text
cards/
  by-key/
    ab/
      CARD-ab...<64-hex-sha256>.json

projects/
  <project-slug>/
    sets/
      2026-09-29.json
      lesson-12.json
```

A canonical card is identified deterministically:

```text
canonical_key = <part_of_speech>:<normalized_german_item>
hash          = sha256(canonical_key)
card_id       = CARD-<full 64-char hex hash>
path          = cards/by-key/<first-two-hash-chars>/<card_id>.json
```

There is deliberately **no global index file**. Duplicate detection is a direct lookup of the deterministic card path. This avoids an ever-growing hot-spot file and removes the need for a global sequential counter.

Project sets contain only canonical card IDs. The set filename is the human-facing grouping: a user-provided short name, lesson number, or ISO date.

## Core invariants

- one canonical card per normalized German lemma/phrase across the whole repository;
- cards contain learning content only;
- no project, lesson, date, source, chat, provenance, first/last-seen, or export metadata inside cards;
- verb inventories and grammar tables are **not stored here**;
- generated `.apkg`, DOCX, and PDF files are delivery artifacts, not repository state;
- Anki/AnkiDroid owns review scheduling and progress;
- every repository change goes through a Pull Request;
- every PR contains exactly one commit rebased directly on current `master`;
- agents/plugins **never merge PRs**; they leave PRs open and return the link;
- never push directly to `master`.

## Worked card lookup example

For **die Entscheidung**:

```text
normalized lemma = entscheidung
canonical_key    = noun:entscheidung
sha256           = 31f3de787252e2246bad78628c5f92ac1c441b6c2ea26b1da70f5b1f67afc15b
card_id          = CARD-31f3de787252e2246bad78628c5f92ac1c441b6c2ea26b1da70f5b1f67afc15b
path             = cards/by-key/31/CARD-31f3de787252e2246bad78628c5f92ac1c441b6c2ea26b1da70f5b1f67afc15b.json
```

The agent checks this exact path. Existing file with the same key = duplicate, so no new card is created.

## Android target and user instructions

Canonical client: **AnkiDroid**.

Primary delivery format: `.apkg`.
Optional backup/interchange: UTF-8 TSV.

Ready user instructions are stored in [docs/ANKIDROID_GUIDE.md](docs/ANKIDROID_GUIDE.md). Agents should answer ordinary usage questions from that local guide without web search unless the user explicitly asks for current version-specific UI verification.

Start with `START_HERE.md`.
