# Lesson Card Workflow

## Commands

The connected plugin exposes two learner workflows:

- **Собери карточки по этому уроку**
- **Собери все глаголы по этому уроку**

## Card extraction boundary

Use material actually present in the current lesson:
- chat and corrections;
- screenshots/files;
- exercises;
- verified video/manuscript/subtitle content;
- generated lesson scenarios;
- questions and answers.

Do not invent unseen or unheard content.

## Vocabulary selection

Collect useful vocabulary rather than every token.

Prefer:
- nouns with article and plural;
- verbs with separability/reflexivity and useful government;
- adjectives/adverbs;
- connectors and B1 Redemittel;
- useful fixed phrases.

Skip incidental names and low-value filler.

## Deduplication

Before creating a card:

1. normalize the candidate;
2. compute `canonical_key`;
3. look it up in `cards/index.json`;
4. if it exists, do not create a new card or Anki note;
5. update last-seen lesson/date and provenance only;
6. if it is new, allocate the next `CARD-NNNNNN`, create the record, and update the index.

Normalization:
- Unicode NFC;
- trim;
- lowercase for key;
- noun: lemma without article;
- verb: infinitive, preserving semantically relevant `sich` and separable prefix;
- adjective/adverb: base form;
- phrase: normalized phrase;
- punctuation-only differences do not create distinct keys.

Key format:

`<part_of_speech>:<normalized_lemma_or_phrase>`

## Card metadata

Store when applicable:
- stable card ID;
- canonical key;
- German lemma/phrase;
- Russian translation;
- part of speech;
- article/plural;
- verb forms;
- government;
- German example;
- Russian example translation;
- grammar note;
- first/last seen lesson and date;
- all lessons in which the item was selected;
- source refs;
- deterministic Anki GUID;
- export status.

## Lesson naming

Lesson ID:

`LESSON-YYYYMMDD-NN`

Human-readable deck title:

`Deutsch B1::Lektion <N> — <topic> — <YYYY-MM-DD>`

Artifacts:
- `Lektion-<N>_<YYYY-MM-DD>_Karten.apkg`
- `Lektion-<N>_<YYYY-MM-DD>_Karten.tsv`
- `Lektion-<N>_<YYYY-MM-DD>_Verben.docx`
- PDF on request.

## AnkiDroid export

Primary target is AnkiDroid.

Use a deterministic note GUID derived from `card_id` or `canonical_key`, not from mutable example text.

Default direction:
- front: Russian cue;
- back: German target + useful metadata + example.

Do not claim import to Android succeeded unless it was actually verified.

## Verb inventory

The verb command is a complete per-lesson inventory and does **not** deduplicate away verbs seen in earlier lessons.

Required columns:
1. Infinitiv
2. Präsens (er/sie/es)
3. Präteritum
4. Partizip II
5. Perfekt
6. Bedeutung (RU)
7. Rektion / Besonderheiten
8. Beispiele DE — Präsens / Präteritum / Perfekt
9. Перевод примеров
10. Грамматика / пояснение

Default downloadable artifact: DOCX. PDF when requested.

## Runtime persistence

Runtime branch: `runtime/cards`.

Allowed runtime paths:
- `cards/CARD-*.json`
- `cards/index.json`
- `exports/cards/*.json`
- `exports/verbs/*.json`

Before write:
- verify repository is private;
- read latest `cards/index.json`;
- detect duplicates;
- use stable transaction/export IDs.

After write:
- read back the index;
- read back at least one touched card/export record;
- only then report persistence as successful.
