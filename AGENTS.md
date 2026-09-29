# AGENTS.md

Mandatory rules for every human contributor and AI/coding agent.

## Terminology

- **deck / набор карточек** — one user-facing collection created from one selected learning source;
- **flashcard** — one vocabulary/phrase item inside a deck;
- **canonical deck** — app-neutral JSON under `projects/<project>/decks/`;
- **app artifact** — Quizlet TXT, Anki APKG, or another application-specific representation;
- **dedupe shard** — app-independent technical lookup preventing lexical duplicates across decks.

Never model one word as one repository-level deck/file.

## Git workflow

Never push directly to `master`.

Every change:

```text
latest master
-> dedicated branch
-> exactly ONE commit
-> validate
-> PR
-> checks pass
-> STOP and return PR URL
```

The commit must have current `master` HEAD as its only parent. If master moves, rebase/squash and rerun validation.

### No-auto-merge

Agents, plugins, automations and assistants must never merge a PR. Only the human owner merges.

## Storage

Canonical decks:

`projects/<project-slug>/decks/<deck-name>.json`

Primary Quizlet exports:

`apps/quizlet/<project-slug>/<deck-name>.txt`

Optional Anki exports:

`apps/anki/<project-slug>/<deck-name>.apkg`

Do not put app-specific artifacts inside `projects/<project>/decks/`.

## Default target

Quizlet is the default application.

For every new canonical deck:
1. create/update the canonical JSON;
2. update dedupe shards;
3. generate the Quizlet TXT;
4. validate JSON↔Quizlet consistency;
5. do **not** generate Anki unless explicitly requested.

## Quizlet representation

UTF-8 text, no header:
- German term in column 1;
- one TAB;
- Russian meaning plus compact useful details in column 2;
- one flashcard per line.

Tabs/newlines inside term or definition are flattened to spaces.

## Anki fallback

Anki is optional. When requested, generate a stable APKG under `apps/anki/<project>/<deck>.apkg` and validate note/card count against the canonical JSON.

## Duplicate check

For each candidate:
1. normalize;
2. create `canonical_key`;
3. SHA-256 the key;
4. read only `dedupe/<first-two-hex>.json`;
5. existing key -> skip;
6. new key -> add to canonical deck and shard.

Dedupe is independent of Quizlet/Anki format.

## Format conversion

Follow `docs/FORMAT_CONVERSION.md`.

Conversion is not new-card extraction and must not silently rewrite vocabulary. In this repository, use canonical JSON as semantic source whenever available.

## Flashcard content

Allowed canonical fields include German, Russian, POS, article/plural, useful verb forms, government, examples and concise grammar notes.

Do not store source URLs, chat IDs, lesson IDs, timestamps, review state or export history inside flashcards.

## Verbs

Complete source-wide verb inventories and DOCX/PDF grammar tables are separate outputs and are never persisted here.

## User help

Use `docs/QUIZLET_GUIDE.md` by default. Use `docs/ANKIDROID_GUIDE.md` only for explicit Anki questions.

## Reporting

Every repository-change report includes the direct PR URL. Never claim a PR is merged unless the human user merged it.
