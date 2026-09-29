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

## Selection modes

Default mixed-card requests prefer:
- nouns with article/plural;
- verbs with separability/reflexivity/government;
- adjectives/adverbs;
- connectors and B1 Redemittel;
- useful short phrases.

Do not mechanically add every token in the default mixed mode.

If the learner explicitly asks for **verbs for cards** / «глаголы для карточек» / «собери глаголы в карточки», keep the request in this card workflow (do not route it to the standalone verb-document workflow). Include the distinct source verbs that are appropriate as flashcards, enrich them with verb forms/government, apply the normal canonical dedupe rules, and generate the derived `<deck>-verbs.txt` view.

If the learner explicitly asks for **grammar for cards** / «грамматика для карточек», keep the request in this card workflow. Capture supported grammar attached to the lesson items in canonical fields (`plural`, `verb_forms`, `government`, `grammar_note`) and generate the corresponding grammar sets. This does not create a separate canonical grammar database.

Routing precedence: when a request contains «карточки» together with «глаголы» or «грамматика», card intent wins. A plain «собери глаголы / таблицу глаголов» without card intent remains the separate standalone verb-table workflow.

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

### Verbs-only set

When canonical cards contain verbs, generate:

`apps/quizlet/<project>/<deck>-verbs.txt`

It contains only those canonical verb cards, each as the same hint-free `German<TAB>Russian meaning` row. It is a derived study view and must not create duplicate canonical items or new dedupe entries.

### Separate grammar sets

Keep morphology and government in canonical JSON, then derive focused Quizlet sets when the corresponding data exists:

- `<deck>-grammar-plural.txt`;
- `<deck>-grammar-praesens-3sg.txt`;
- `<deck>-grammar-praeteritum.txt`;
- `<deck>-grammar-partizip-ii.txt`;
- `<deck>-grammar-perfekt.txt`;
- `<deck>-grammar-rektion.txt`;
- `<deck>-grammar-notes.txt` when `grammar_note` exists.

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
5. regenerate the **entire** hint-free vocabulary TXT, the verbs-only TXT when verbs exist, and every applicable grammar TXT from canonical JSON;
6. validate every generated row exactly against canonical fields;
7. open the normal one-commit PR.

Do not append blindly to the TXT and do not use it as semantic source when canonical JSON exists.

The repository update is not a Quizlet account sync. After merge, the learner must reconcile an existing Quizlet set through Edit/Edit set, or create a replacement set from the regenerated full TXT when changes are extensive.

## Anki export — optional fallback

Generate APKG only when the user explicitly requests Anki or asks for a format conversion to Anki.

Store it under `apps/anki/<project>/<deck>.apkg`.

## Connected Quizlet creation

GitHub remains the semantic source of truth. New lesson material is **never Quizlet-only**: first complete the GitHub branch -> validation -> PR transaction and keep the PR open; only then may the connected Quizlet action be used if the learner asked for GitHub + Quizlet in one request.

For an existing GitHub deck, «возьми deck из GitHub и создай набор в Quizlet» means: read canonical JSON from the requested ref, validate/regenerate the repository views as needed, then ask the connected Quizlet action to create a **new** set from that content without re-running new-lesson dedupe or rewriting the canonical deck.

Current connected-action limitations must be respected:
- it creates new flashcard sets only; it cannot edit/add to/update an existing Quizlet set;
- creation is asynchronous, so success exists only after the generation-status action reports `complete` and returns the set link;
- it is a generative set-creation action, not a deterministic raw-TXT importer. Instruct it to use the canonical pairs/count exactly and add nothing, but do not claim byte-for-byte fidelity unless a future supported read-back verifies the complete set.

If exact deterministic import is required, use the repository TXT with Quizlet website Import. If the connected action is unavailable, return the validated TXT/manual import path.

## Translation-first requests

If the user asks to translate first, translate naturally near B1, identify the result as an adaptation, then extract the deck.

## Git workflow

For every new deck batch:
1. start from current `master`;
2. create dedicated branch;
3. extract candidates and run dedupe;
4. create canonical JSON;
5. generate the hint-free Quizlet vocabulary TXT, the verbs-only TXT when applicable, and applicable grammar sets;
6. optionally generate Anki only if requested;
7. validate canonical JSON, dedupe and app artifacts;
8. make exactly one commit based on current `master`;
9. open PR;
10. if master moved, rebase/squash and regenerate/revalidate;
11. stop and return PR URL.

Never merge automatically.

## Verb boundary

The complete verb-table workflow remains separate and returns DOCX/PDF rather than storing those documents here.
