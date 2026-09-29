# Card Workflow — Quizlet First

## Meaning of «собери карточки»

Create one canonical deck containing many useful flashcards from the requested source and produce a **Quizlet import file by default**.

Supported sources include a lesson, conversation, pasted text, file, screenshot, verified video material, or translated German text.

## Paths

Canonical source:

`projects/<project-slug>/decks/<deck-name>.json`

Default Quizlet artifact:

`apps/quizlet/<project-slug>/<deck-name>.txt`

Optional Anki artifact:

`apps/anki/<project-slug>/<deck-name>.apkg`

## Naming

Choose project:
1. explicit user project/folder;
2. known current ChatGPT Project;
3. `general`.

Choose deck:
1. explicit short user name;
2. explicit lesson number;
3. otherwise ISO date `YYYY-MM-DD`;
4. append `-02`, `-03`, etc. on collision.

## Canonical JSON

The JSON is application-neutral and contains all selected flashcards. No Quizlet/Anki-specific fields belong in it.

## Selection

Prefer:
- nouns with article/plural;
- verbs with separability/reflexivity/government;
- adjectives/adverbs;
- connectors and B1 Redemittel;
- useful short phrases.

Do not mechanically add every token.

## Normalization and dedupe

Canonical key:

`<part_of_speech>:<normalized_item>`

Use Unicode NFC, trim/collapse whitespace, preserve umlauts and `ß`, lowercase for the key, noun dictionary lemma without article, verb infinitive preserving required `sich` and joined separable prefix, base adjective/adverb, and meaningful phrase punctuation.

For each key:
1. SHA-256;
2. first two hex chars -> `dedupe/<shard>.json`;
3. if key exists, skip it;
4. if new, add it to the canonical deck and shard.

## Quizlet export — default

Generate UTF-8 text with no header.

Each line:

`<German term><TAB><Russian definition + compact notes>`

Definition enrichment may include plural, verb forms, government, examples and concise grammar notes, separated with ` · `.

Example:

```text
die Entscheidung	решение · Plural: Entscheidungen
kommen	приходить; происходить из · Präsens: kommt · Präteritum: kam · Partizip II: gekommen · Perfekt: ist gekommen · Rektion: aus + Dat.
```

Quizlet import settings:
- between term and definition: **Tab**;
- between cards: **New line**;
- term language: German;
- definition language: Russian.

## Updating an existing deck

When adding, changing, or removing cards in an existing repository deck:

1. treat the canonical JSON as semantic source;
2. keep the existing project/deck identity unless the user asks for a new deck;
3. update canonical membership/content;
4. update dedupe shards only when canonical lexical membership changes;
5. regenerate the **entire** Quizlet TXT snapshot from the canonical JSON;
6. validate row count and German terms against canonical JSON;
7. open the normal one-commit PR.

Do not append blindly to the TXT and do not use it as semantic source when canonical JSON exists.

The repository update is not a Quizlet account sync. After merge, the learner must reconcile an existing Quizlet set through Edit/Edit set, or create a replacement set from the regenerated full TXT when changes are extensive.

## Anki export — optional fallback

Generate APKG only when the user explicitly requests Anki or asks for a format conversion to Anki.

Store it under `apps/anki/<project>/<deck>.apkg`.

## Translation-first requests

If the user asks to translate first, translate naturally near B1, identify the result as an adaptation, then extract the deck.

## Git workflow

For every new deck batch:
1. start from current `master`;
2. create dedicated branch;
3. extract candidates and run dedupe;
4. create canonical JSON;
5. generate Quizlet TXT;
6. optionally generate Anki only if requested;
7. validate canonical JSON, dedupe and app artifacts;
8. make exactly one commit based on current `master`;
9. open PR;
10. if master moved, rebase/squash and regenerate/revalidate;
11. stop and return PR URL.

Never merge automatically.

## Verb boundary

The complete verb-table workflow remains separate and returns DOCX/PDF rather than storing those documents here.
