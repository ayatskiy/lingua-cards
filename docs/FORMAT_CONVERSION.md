# Format Conversion Workflow

## Purpose

Convert an existing flashcard deck from one application format to another in a specified GitHub repository and open a PR with the result.

Typical requests:
- «Конвертируй deck 2026-09-29 из Quizlet в Anki в ayatskiy/lingua-cards»
- «Сделай Quizlet-версию Anki-набора X в repo owner/name»
- «Преобразуй карточки из Anki в Quizlet и открой PR»

## Required resolution

Resolve:
1. repository;
2. deck/set identity;
3. source application/format;
4. target application/format.

If repository is omitted, `ayatskiy/lingua-cards` is the default for this plugin.

## Repository-first safety

Before writing:
1. read the target repository's `START_HERE.md`, `AGENTS.md`, or equivalent rules when present;
2. obey its branch/PR policy;
3. never merge unless that repository explicitly permits it **and** the user explicitly requests merge. For `lingua-cards`, never merge.

## Semantic source

If the repository contains an application-neutral canonical deck JSON, use that as the semantic source even when the user says “Quizlet -> Anki” or “Anki -> Quizlet”.

Verify that the named source artifact exists, but do not reverse-engineer a lossy app artifact when canonical data is available.

If no canonical source exists:
- Quizlet source: parse term/definition text using the detected delimiter;
- Anki source: parse APKG only when the note model can be read reliably;
- if semantics cannot be reconstructed without loss, stop and report what is missing.

## Conversion rules

Conversion must preserve vocabulary semantics. Do not:
- add new vocabulary;
- dedupe against unrelated decks as if this were a new lesson;
- silently rewrite translations;
- delete the source artifact unless explicitly requested.

App-specific escaping/flattening is allowed.

## Target paths in lingua-cards

Quizlet:
`apps/quizlet/<project>/<deck>.txt`

Anki:
`apps/anki/<project>/<deck>.apkg`

## Quizlet target

UTF-8, no header, German TAB Russian/notes, one card per line.

## Anki target

Generate stable notes from canonical keys and verify APKG note/card count equals canonical deck card count.

## Git transaction

1. start from latest target-repo default branch;
2. create dedicated conversion branch;
3. generate target artifact;
4. validate against source/canonical deck;
5. create exactly one commit when repository rules require it;
6. open PR;
7. return direct PR URL;
8. do not merge automatically.
