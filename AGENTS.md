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

Primary Quizlet vocabulary export:

`apps/quizlet/<project-slug>/<deck-name>.txt`

Derived Quizlet verb export:

`apps/quizlet/<project-slug>/<deck-name>-verbs.txt`

Derived Quizlet grammar exports:

`apps/quizlet/<project-slug>/<deck-name>-grammar-<kind>.txt`

Optional Anki exports:

`apps/anki/<project-slug>/<deck-name>.apkg`

Do not put app-specific artifacts inside `projects/<project>/decks/`.

## Default target

Quizlet is the default application.

For every new canonical deck:
1. create/update the canonical JSON;
2. update dedupe shards;
3. generate the hint-free Quizlet vocabulary TXT;
4. when verbs exist, generate the derived verbs-only Quizlet TXT;
5. generate separate Quizlet grammar sets for available plural, verb-form, government and grammar-note data;
6. validate canonical↔Quizlet consistency;
7. do **not** generate Anki unless explicitly requested.

## Quizlet representation

UTF-8 text, no header, one flashcard per line.

### Vocabulary set

`apps/quizlet/<project>/<deck>.txt` is optimized for recall rather than reference display:
- column 1: canonical German term;
- one TAB;
- column 2: Russian meaning only;
- do not append German plural forms, verb forms, government, German examples, or other target-language material that can reveal the correct multiple-choice answer.

Canonical JSON still keeps morphology/government as semantic data.

### Verbs-only set

When canonical cards contain verbs, generate `<deck>-verbs.txt` from those same canonical verb cards using the same hint-free `German<TAB>Russian meaning` rows. It is a derived study view, not a second canonical deck and not a source-wide DOCX/PDF inventory.

### Grammar sets

When corresponding canonical fields exist, generate separate one-fact-per-card sets:
- `-grammar-plural.txt`;
- `-grammar-praesens-3sg.txt`;
- `-grammar-praeteritum.txt`;
- `-grammar-partizip-ii.txt`;
- `-grammar-perfekt.txt`;
- `-grammar-rektion.txt`;
- `-grammar-notes.txt` when `grammar_note` exists.

Grammar sets are derived views of the same canonical deck and do not create new canonical lexical items or dedupe entries.

Tabs/newlines inside term or definition are flattened to spaces.

## Quizlet account create/update semantics

The repository controls canonical deck data and export artifacts, not the learner's Quizlet account.

For a **new Quizlet set**, the deterministic path is website import from the full TXT. A connected Quizlet action may instead generate a new set from the validated canonical/TXT content, but that action is asynchronous/generative rather than a raw TXT importer, so do not claim byte-for-byte fidelity without a supported read-back verification.

For an **existing Quizlet set**:
- the connected Quizlet action cannot modify/update the existing set; it creates new sets only;
- regenerate the full TXT snapshot from canonical JSON;
- tell the learner to open the existing set and use Edit/Edit set for small changes;
- for large rewrites, recommend creating and verifying a replacement set from the regenerated TXT;
- never claim Quizlet itself was updated merely because repository files changed.

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

Complete source-wide verb inventories and DOCX/PDF grammar tables are separate outputs and are never persisted here. A `-verbs.txt` file is allowed because it is only a derived Quizlet view of verb cards already present in the canonical lesson deck.

## User help

Use `docs/QUIZLET_GUIDE.md` by default. Use `docs/ANKIDROID_GUIDE.md` only for explicit Anki questions.

## Reporting

Every repository-change report includes the direct PR URL. Never claim a PR is merged unless the human user merged it.
