# lingua-cards

Standalone, project-agnostic source of truth for German flashcard decks created by the **Deutsch Lesson Cards** plugin.

## Product model

One learning source creates one **deck / набор карточек** containing many flashcards.

The canonical deck is application-neutral JSON:

```text
projects/<project-slug>/decks/<deck-name>.json
```

Application-specific study artifacts are stored separately:

```text
apps/
  quizlet/
    <project-slug>/
      <deck-name>.txt
  anki/
    <project-slug>/
      <deck-name>.apkg
```

**Quizlet is the default target.** Every canonical deck must have a Quizlet import file. Anki is an optional fallback and is generated only when explicitly requested or through format conversion.

## Quizlet-first format

Quizlet imports structured text on its website. This repository uses UTF-8 text with:

```text
German term<TAB>Russian definition and compact notes
one flashcard per line
```

Example:

```text
die Entscheidung	решение · Plural: Entscheidungen
kommen	приходить; происходить из · Präsens: kommt · Präteritum: kam · Partizip II: gekommen · Perfekt: ist gekommen · Rektion: aus + Dat. (происхождение)
```

The file has no header because every non-empty row is a card.

## Canonical deck

The JSON remains the semantic source of truth for vocabulary, morphology and notes. App exports are reproducible views of that source.

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
      "plural": "Entscheidungen"
    }
  ]
}
```

## Duplicate prevention

Cross-deck duplicate prevention remains app-independent. A canonical key is hashed with SHA-256 and looked up in:

`dedupe/<first-two-hash-characters>.json`

The shard maps the canonical key to the canonical deck JSON where the item was first introduced.

## Format conversion

See `docs/FORMAT_CONVERSION.md`.

Conversion creates or refreshes a target-app artifact while preserving the source artifact by default. In this repository, prefer the canonical JSON as the semantic source even when the request is phrased as “Quizlet → Anki” or “Anki → Quizlet”.

## Repository rules

- never push directly to `master`;
- every change goes through a PR;
- each PR contains exactly one commit rebased on current `master`;
- agents/plugins never merge PRs;
- flashcards do not carry source/chat/history metadata;
- complete verb DOCX/PDF tables remain outside this repository.

## User guides

- Primary: [Quizlet](docs/QUIZLET_GUIDE.md)
- Fallback: [Anki / AnkiDroid](docs/ANKIDROID_GUIDE.md)

Start with `START_HERE.md`.
