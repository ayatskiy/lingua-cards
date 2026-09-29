# AnkiDroid User Guide

This is the ready, offline instruction for using flashcards generated from `lingua-cards`.

Agents/plugins should answer ordinary usage questions from this file without web search. Search the web only when the user explicitly asks to verify current version-specific UI.

## Recommended Android app

Use **AnkiDroid Flashcards**.

It is the target app for generated `.apkg` packages. AnkiDroid owns spaced-repetition scheduling, review history, due cards, and progress/statistics.

## Install

1. Install **AnkiDroid Flashcards** on Android.
2. Google Play is the normal installation route; F-Droid is also acceptable.
3. Open AnkiDroid once after installation.

## Import generated cards

The card plugin returns an `.apkg` file.

Preferred method:

1. Save/download the `.apkg` file to the Android device.
2. Open **Downloads** or another file manager.
3. Tap the `.apkg` file.
4. Choose **AnkiDroid** if Android asks which application should open it.
5. Confirm the import.
6. The imported deck appears in AnkiDroid.

Alternative method:

1. Open AnkiDroid.
2. Use AnkiDroid's import action.
3. Select the generated `.apkg` file.
4. Confirm import.

Exact menu placement can vary by AnkiDroid version, so ordinary instructions should describe the action rather than inventing a version-specific button path.

## Study and repeat

1. Open the imported deck.
2. Read the front side and recall the German target before revealing the answer.
3. Reveal the answer.
4. Grade your recall with the review buttons available in AnkiDroid, typically **Again / Hard / Good / Easy**.
5. Return regularly and review cards marked as due.

Do not create a second scheduling system in GitHub. AnkiDroid controls when cards are due.

## Progress and statistics

Use AnkiDroid's built-in statistics/progress views to inspect:
- review activity;
- due/review counts;
- deck/card progress;
- retention/statistical summaries available in the installed version.

## Optional sync

If you use multiple devices:

1. Sign in to **AnkiWeb** from AnkiDroid.
2. Run sync.
3. Use the same AnkiWeb account on the other Anki/AnkiDroid device.

Sync is optional for single-device study.

## Later card batches

Import later generated `.apkg` files in the same way.

Before export, Deutsch Lesson Cards performs canonical duplicate filtering through deterministic card identity. Generated notes should use stable `CardID`/GUID identity so content updates do not depend on mutable examples or translations.

## Naming

Internal canonical card names are deterministic technical IDs:

`CARD-<sha256(canonical_key)>`

Example:

`CARD-31f3de787252e2246bad78628c5f92ac1c441b6c2ea26b1da70f5b1f67afc15b`

Users normally interact with a simple deck/set name such as:
- `2026-09-29`
- `lesson-12`
- another short name explicitly supplied by the user.

Project/date/lesson/source information is not stored inside the canonical card fields.
