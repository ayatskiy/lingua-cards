# AGENTS.md

Mandatory rules for every human contributor and AI/coding agent.

## Terminology

Use these terms consistently:

- **deck / набор карточек** — one user-facing collection created from a lesson, topic, dialogue, text, video, or other source;
- **flashcard** — one vocabulary/phrase item inside a deck;
- **dedupe shard** — technical cross-deck lookup used only to prevent duplicate lexical items.

Never model one word as one repository-level deck/file.

## Git workflow

Never push directly to `master`.

Every change follows:

```text
latest master
-> dedicated branch
-> exactly ONE commit
-> validate
-> PR
-> checks pass
-> STOP and return PR URL
```

The PR commit must have current `master` HEAD as its only parent. If `master` changes, rebase/squash and rerun validation.

### No-auto-merge

Agents, plugins, automations, and assistants must never merge a PR in this repository. Only the human owner merges it.

## Storage

Decks are stored as a required pair:

- `projects/<project-slug>/decks/<deck-name>.json` — canonical editable source;
- `projects/<project-slug>/decks/<deck-name>.apkg` — versioned ready-to-import Anki package.

The JSON contains many flashcard objects. The APKG is generated from that JSON and committed in the same PR.

Duplicate shards:

`dedupe/<sha256(canonical_key)[0:2]>.json`

Each shard maps canonical key -> first deck path.

There is no per-word repository file and no one-file global index.

## Normalization

Follow `docs/CARD_WORKFLOW.md`:

- Unicode NFC;
- trim and collapse whitespace;
- preserve umlauts and `ß`;
- lowercase for canonical key;
- nouns use dictionary lemma without article;
- verbs use dictionary infinitive, preserving required `sich` and joined separable prefix;
- adjectives/adverbs use base form;
- phrases preserve meaningful internal punctuation.

## Duplicate check

For each candidate:

1. normalize;
2. create `canonical_key`;
3. hash with SHA-256;
4. read only the corresponding `dedupe/<shard>.json`;
5. if key exists, skip;
6. otherwise add flashcard to the new deck and update that shard.

Deck JSON, sibling APKG, and all touched shards must be changed in the same one-commit PR.

## Flashcard content

Allowed learning fields include German, Russian, part of speech, article/plural, useful verb forms, government, examples, and a concise grammar note.

Do not store source URLs, chat IDs, lesson IDs, project IDs, timestamps, provenance, review progress, or export history inside flashcards.

## Verbs

Complete source-wide verb inventories, tense tables, grammar documents, DOCX and PDF are separate outputs and are never persisted here.

A verb may still appear as an ordinary flashcard inside a deck.

## User help

For ordinary install/import/review/progress questions use `docs/ANKIDROID_GUIDE.md` without web search unless version-specific current UI verification is explicitly requested.

## Reporting

Every repository-change report includes the direct PR URL. Never claim a PR is merged unless the human user merged it.
