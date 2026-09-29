# Universal Card Workflow

## Purpose

`lingua-cards` stores only canonical vocabulary flashcards. It is reusable from any ChatGPT Project or ordinary chat.

Supported card sources include:
- current conversation;
- pasted text or dialogue;
- selected messages;
- screenshots/files;
- exercises;
- verified video/transcript/manuscript material;
- German text created by a requested translation.

## Project/set placement

Choose a project folder:
1. explicit project/folder name from the user;
2. known current ChatGPT Project name;
3. `general`.

Set filename:
1. explicit short name;
2. explicit lesson number;
3. otherwise ISO date `YYYY-MM-DD`;
4. append `-02`, `-03`, etc. on collision.

Path:

`projects/<project-slug>/sets/<set-name>.json`

A set contains only:
- `schema_version`;
- ordered IDs of **new canonical cards created for that set**.

No chat IDs, source URLs, timestamps, lesson metadata, or provenance.

## Canonical identity: no global index

There is deliberately no `index.json`.

### Canonical normalization

Normalization must be deterministic across agents:

- normalize Unicode to NFC;
- trim leading/trailing whitespace and collapse internal whitespace runs to one space;
- preserve German umlauts and `ß`; do not transliterate to `ae/oe/ue/ss`;
- lowercase for the key using ordinary Unicode lowercase, not aggressive case-folding that turns `ß` into `ss`;
- noun: use the dictionary lemma without `der/die/das`; article remains a separate display field;
- verb: use dictionary infinitive; preserve semantically required `sich`; write separable verbs as their joined infinitive such as `aufstehen`;
- adjective/adverb: use the base form;
- phrase/connector: preserve meaningful internal punctuation, remove only surrounding whitespace and non-semantic terminal punctuation;
- do not normalize two genuinely different lexical items into one key merely because spelling is similar.

For each candidate:

1. normalize the German item;
2. form `canonical_key = <part_of_speech>:<normalized_item>`;
3. compute lowercase SHA-256 hex of the UTF-8 canonical key;
4. set `card_id = CARD-<full_hash>`;
5. derive path `cards/by-key/<hash[0:2]>/<card_id>.json`;
6. check that exact path.

If the file exists with the same key, skip it as a duplicate.

If it does not exist, create it and add its card ID to the current set.

This avoids an ever-growing central index and makes duplicate lookup O(1) by deterministic path.

Worked example for `die Entscheidung`:

```text
normalized lemma = entscheidung
canonical_key    = noun:entscheidung
sha256           = 31f3de787252e2246bad78628c5f92ac1c441b6c2ea26b1da70f5b1f67afc15b
card_id          = CARD-31f3de787252e2246bad78628c5f92ac1c441b6c2ea26b1da70f5b1f67afc15b
lookup path      = cards/by-key/31/CARD-31f3de787252e2246bad78628c5f92ac1c441b6c2ea26b1da70f5b1f67afc15b.json
```

If that file already exists and its `canonical_key` is `noun:entscheidung`, creation is skipped.

## Canonical card content

A card contains learning content only:
- card ID;
- canonical key;
- German target;
- Russian meaning;
- part of speech;
- optional article/plural;
- optional verb forms when this vocabulary item is a verb;
- optional government;
- optional German example;
- optional Russian translation of the example;
- optional grammar note.

No project/lesson/date/source/history/export metadata.

## Translation-first requests

For requests such as:
- «переведи этот разговор на немецкий и собери карточки»;
- «переведи текст на немецкий и сделай карточки»;

first produce natural German near B1, then extract useful vocabulary from that German adaptation. Do not represent the translated wording as original-source text.

## Selection quality

Prefer atomic, useful active vocabulary:
- nouns with article/plural;
- verbs with relevant separability/reflexivity/government;
- adjectives/adverbs;
- connectors and B1 Redemittel;
- short useful phrases.

Avoid low-value filler and one-off proper names unless explicitly requested.

## AnkiDroid export

`lingua-cards` JSON is canonical source; `.apkg` is generated output.

Use stable Anki note identity from `card_id` (or the canonical key). Mutable examples/translations must not define note identity.

Recommended Anki note model:
- first field: stable `CardID`;
- remaining fields: German, Russian, part of speech, article/plural, verb forms, government, examples, grammar note;
- no lesson/project/date/source fields.

When the APKG generator supports deterministic GUIDs, derive the Anki note GUID from `CardID`. Keeping `CardID` as the first field also provides an explicit stable source identifier.

Default:
- front: Russian cue;
- back: German target + useful linguistic detail.

Deck/set name: user label, lesson number, or date. Project grouping may be represented by an Anki parent deck, but never by extra fields inside the note.

Generated `.apkg`/TSV files are returned to the user and are not committed here.

For end-user installation/import/review/progress instructions, use `docs/ANKIDROID_GUIDE.md`.

## Verb workflow boundary

The source-wide verb-table command is separate.

It may generate a DOCX/PDF with:
- Infinitiv;
- Präsens;
- Präteritum;
- Partizip II;
- Perfekt;
- meaning;
- government;
- examples;
- translations;
- grammar notes.

That document is **not stored in this repository**.

## Git write workflow

Every card batch:
1. start from current `master`;
2. create `cards/<project>-<set>`;
3. create new canonical card files and one set manifest;
4. make exactly one commit;
5. ensure that commit's only parent is current `master` HEAD;
6. validate;
7. open a PR;
8. if `master` moves, rebase/squash back to one commit and repeat duplicate checks;
9. leave the PR open and give the user its direct URL.

**Never merge the PR automatically.**
