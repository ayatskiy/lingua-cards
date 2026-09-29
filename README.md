# lingua-cards

Standalone, project-agnostic source of truth for German **flashcard decks** created by the **Deutsch Lesson Cards** ChatGPT plugin.

## Domain model

A user request such as «собери карточки по этому уроку» creates **one deck / набор карточек** that contains many individual flashcards.

```text
one lesson/topic/dialogue/source
        ↓
one deck file
        ↓
many flashcards
```

This repository does not create one repository file per word.

## Layout

```text
projects/
  <project-slug>/
    decks/
      lesson-12.json
      2026-09-29.json
      restaurant-dialog.json

dedupe/
  00.json
  01.json
  ...
  ff.json
```

A deck file contains its flashcards directly:

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

The deck filename is the user-facing deck name. Prefer a user-supplied short name, lesson number, or ISO date.

## Global duplicate prevention without one huge index

There is no single `index.json`.

For each candidate lexical item:

```text
canonical_key = <part_of_speech>:<normalized_item>
hash          = sha256(canonical_key)
shard         = first two hex characters
lookup        = dedupe/<shard>.json
```

Example for **die Entscheidung**:

```text
canonical_key = noun:entscheidung
sha256        = 31f3de787252e2246bad78628c5f92ac1c441b6c2ea26b1da70f5b1f67afc15b
lookup        = dedupe/31.json
```

A shard may contain:

```json
{
  "schema_version": 1,
  "entries": {
    "noun:entscheidung": "projects/deutsch-uebungen/decks/lesson-12.json"
  }
}
```

If the key already exists, that item is skipped in a later deck. If it is new, it is added to the new deck and the shard is updated in the same PR.

This gives global duplicate detection while avoiding one ever-growing write hot spot.

## Boundaries

- deck file = one group of many flashcards;
- flashcard = one word/phrase/item inside the deck;
- no source/chat/history metadata inside flashcards;
- complete verb tables/grammar DOCX/PDF are not stored here;
- generated `.apkg` is a delivery artifact, not canonical Git state;
- AnkiDroid owns review scheduling and progress;
- every repository change uses a PR;
- every PR has exactly one commit rebased on current `master`;
- agents/plugins never merge PRs;
- never push directly to `master`.

## Android

Recommended client: **AnkiDroid Flashcards**.

One deck JSON is exported as one Anki deck/package. Ready instructions are in [docs/ANKIDROID_GUIDE.md](docs/ANKIDROID_GUIDE.md).

Start with `START_HERE.md`.
