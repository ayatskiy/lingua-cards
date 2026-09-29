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

## Quizlet exports — vocabulary plus grammar

Generate UTF-8 text with no header.

### Default vocabulary set

`apps/quizlet/<project>/<deck>.txt` tests lexical meaning. Each line is exactly:

`<German term><TAB><Russian meaning>`

Do **not** append German plural forms, conjugated forms, Partizip II, Perfekt, government, German examples, or other target-language material to the definition side. In Quizlet Learn/Test those details can reveal the correct multiple-choice answer.

Example:

```text
die Entscheidung	решение
kommen	приходить; происходить из
```

### Separate grammar sets

Keep morphology and government in canonical JSON, then derive focused Quizlet sets when the corresponding data exists:

- `<deck>-grammar-plural.txt`;
- `<deck>-grammar-praesens-3sg.txt`;
- `<deck>-grammar-praeteritum.txt`;
- `<deck>-grammar-partizip-ii.txt`;
- `<deck>-grammar-perfekt.txt`;
- `<deck>-grammar-rektion.txt`.

Each grammar card tests one fact. Do not add grammar-set cards to cross-deck lexical dedupe because they are derived views of existing canonical items.

Examples:

```text
das Geburtsdatum — Plural	die Geburtsdaten
kommen — Präteritum	kam
kommen — Rektion	aus + Dat. (происхождение)
```

Quizlet import settings:
- between term and definition: **Tab**;
- between cards: **New line**.

For the vocabulary set use German terms and Russian definitions. Grammar sets may intentionally use German on both sides because they test German morphology rather than lexical meaning.

## Updating an existing deck

When adding, changing, or removing cards in an existing repository deck:

1. treat the canonical JSON as semantic source;
2. keep the existing project/deck identity unless the user asks for a new deck;
3. update canonical membership/content;
4. update dedupe shards only when canonical lexical membership changes;
5. regenerate the **entire** hint-free vocabulary TXT and every applicable grammar TXT from canonical JSON;
6. validate every generated row exactly against canonical fields;
7. open the normal one-commit PR.

Do not append blindly to the TXT and do not use it as semantic source when canonical JSON exists.

The repository update is not a Quizlet account sync. After merge, the learner must reconcile an existing Quizlet set through Edit/Edit set, or create a replacement set from the regenerated full TXT when changes are extensive.

## Anki export — optional fallback

Generate APKG only when the user explicitly requests Anki or asks for a format conversion to Anki.

Store it under `apps/anki/<project>/<deck>.apkg`.

## Connected study-app import

GitHub remains the semantic source of truth. The connected Quizlet plugin/action may be used as an optional publishing target when its runtime action is available and the user asks for it.

Supported intent includes:
- create/update the canonical deck and PR, then import the validated vocabulary/grammar sets into the connected app;
- «возьми deck из GitHub и импортируй в Quizlet» — read canonical JSON, validate/regenerate app views as needed, and publish them without re-running new-lesson dedupe or rewriting vocabulary.

Never claim the external app was updated unless its tool confirms the write. If no compatible action is exposed in the current runtime, return the validated TXT files/manual import path instead.

## Translation-first requests

If the user asks to translate first, translate naturally near B1, identify the result as an adaptation, then extract the deck.

## Git workflow

For every new deck batch:
1. start from current `master`;
2. create dedicated branch;
3. extract candidates and run dedupe;
4. create canonical JSON;
5. generate the hint-free Quizlet vocabulary TXT and applicable grammar sets;
6. optionally generate Anki only if requested;
7. validate canonical JSON, dedupe and app artifacts;
8. make exactly one commit based on current `master`;
9. open PR;
10. if master moved, rebase/squash and regenerate/revalidate;
11. stop and return PR URL.

Never merge automatically.

## Verb boundary

The complete verb-table workflow remains separate and returns DOCX/PDF rather than storing those documents here.
