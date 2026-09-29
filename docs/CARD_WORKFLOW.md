# Universal Deck Workflow

## Meaning of «собери карточки»

Create **one deck / набор карточек** containing many useful flashcards from the requested source.

Supported sources include a lesson, conversation, pasted text, file, screenshot, verified video material, or translated German text.

## Deck placement

Project folder:
1. explicit user project/folder;
2. known current ChatGPT Project;
3. `general`.

Deck filename:
1. explicit short name;
2. explicit lesson number;
3. otherwise ISO date `YYYY-MM-DD`;
4. append `-02`, `-03`, etc. on collision.

Path:

`projects/<project-slug>/decks/<deck-name>.json`

No extra project/lesson/date/source metadata is needed inside the deck; path and filename provide grouping.

## Deck file

```json
{
  "schema_version": 1,
  "cards": [
    {
      "canonical_key": "noun:entscheidung",
      "german": "die Entscheidung",
      "russian": "решение",
      "part_of_speech": "noun",
      "article": "die",
      "plural": "Entscheidungen",
      "example_de": "Das war eine schwierige Entscheidung.",
      "example_ru": "Это было трудное решение."
    },
    {
      "canonical_key": "verb:sich entscheiden",
      "german": "sich entscheiden",
      "russian": "решаться; принимать решение",
      "part_of_speech": "verb"
    }
  ]
}
```

## Normalization

Canonical key format:

`<part_of_speech>:<normalized_item>`

Rules:
- Unicode NFC;
- trim and collapse whitespace;
- preserve umlauts and `ß`;
- lowercase;
- noun: dictionary lemma without article;
- verb: dictionary infinitive, preserving required `sich` and joined separable prefix;
- adjective/adverb: base form;
- phrase/connector: preserve meaningful internal punctuation.

Examples:
- `noun:entscheidung`
- `verb:gehen`
- `verb:sich entscheiden`
- `phrase:meiner meinung nach`

## Sharded global duplicate check

Do not use one giant global index.

For each candidate:

1. compute canonical key;
2. compute SHA-256 hex;
3. use first two hex characters as shard;
4. read `dedupe/<shard>.json`; missing file = empty shard;
5. if key exists, skip;
6. if new, add flashcard to new deck and key -> deck path to shard.

Example:

```text
candidate       = die Entscheidung
canonical_key   = noun:entscheidung
sha256          = 31f3de787252e2246bad78628c5f92ac1c441b6c2ea26b1da70f5b1f67afc15b
shard           = 31
lookup          = dedupe/31.json
new deck        = projects/deutsch-uebungen/decks/lesson-12.json
```

```json
{
  "schema_version": 1,
  "entries": {
    "noun:entscheidung": "projects/deutsch-uebungen/decks/lesson-12.json"
  }
}
```

If the same key appears later, no new flashcard is added to the later deck unless the user explicitly requests duplicates.

With 256 shards, each lookup touches only a small part of the registry and avoids one shared write hot spot.

## Selection quality

Prefer useful active vocabulary:
- nouns with article/plural;
- verbs with separability/reflexivity/government;
- adjectives/adverbs;
- connectors and B1 Redemittel;
- useful short phrases.

Do not add every token mechanically.

## Translation-first requests

If user asks to translate first, produce natural German near B1, identify it as translation/adaptation, then build the deck from that German text.

## AnkiDroid export

One deck JSON becomes one Anki deck/package.

Each flashcard may receive a generated stable technical note ID derived from SHA-256(canonical_key). This is an export identity only; it does not create one repository file per word.

Default study direction:
- front: Russian cue;
- back: German target + useful linguistic details.

Use deck filename as human-facing Anki deck name.

Return `.apkg`/TSV to user; do not commit binaries.

For app usage instructions use `docs/ANKIDROID_GUIDE.md`.

## Verb boundary

The source-wide verb-table workflow is separate. It returns DOCX/PDF and does not store those files or tables here.

## Git workflow

Every deck batch:
1. start from current `master`;
2. create dedicated branch;
3. extract candidates;
4. read only required dedupe shards;
5. create one deck file containing all new flashcards;
6. update all touched dedupe shards;
7. make exactly one commit whose parent is current `master` HEAD;
8. validate;
9. open PR;
10. if master moved, rebase/squash and rerun dedupe;
11. stop and return PR URL.

Never merge automatically.
