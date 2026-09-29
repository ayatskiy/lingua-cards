# Quizlet User Guide

This is the default card workflow.

## What the plugin gives you

For every deck the repository stores:

- canonical source: `projects/<project>/decks/<name>.json`;
- Quizlet import text: `apps/quizlet/<project>/<name>.txt`.

The default vocabulary TXT is UTF-8 text with one flashcard per line and a TAB between the German term and Russian meaning. It intentionally excludes German morphology from the definition side so Quizlet study modes do not leak the answer. When canonical data contains plural, verb forms or government, separate grammar TXT sets are generated alongside the vocabulary file.

## Vocabulary and grammar sets

The main `<deck>.txt` contains only `German<TAB>Russian meaning`.

Derived files such as `<deck>-grammar-plural.txt`, `<deck>-grammar-praesens-3sg.txt`, `<deck>-grammar-praeteritum.txt`, `<deck>-grammar-partizip-ii.txt`, `<deck>-grammar-perfekt.txt` and `<deck>-grammar-rektion.txt` keep morphology/government practice separate from vocabulary recognition.

## Repository snapshot vs Quizlet account

The repository TXT is the complete current snapshot of the deck. Updating `apps/quizlet/<project>/<deck>.txt` in GitHub does **not** automatically update an already-published Quizlet set.

Use one of the workflows below.

## Import through a connected app/plugin

If the current ChatGPT runtime exposes the connected Quizlet action, the learner may ask to publish a generated repository deck directly, for example:

- «создай карточки, сохрани в GitHub и импортируй в Quizlet»;
- «возьми `deutsch-uebungen/2026-09-29` из GitHub и импортируй в Quizlet».

The agent must still use canonical JSON as semantic source, validate the derived vocabulary/grammar sets, and treat the external app as a deployment target rather than a second source of truth. Do not re-run cross-deck dedupe for a GitHub→app import. Never report a successful import without confirmation from the connected app action.

If the runtime does not expose such an action, use the website import below.

## Create a new Quizlet set

Quizlet's current bulk import is performed on the **website**.

1. Open Quizlet in a browser and sign in.
2. Select **Create** -> **Flashcard set**.
3. Enter the set title.
4. Select **Import**.
5. Open the generated `.txt` from `apps/quizlet/<project>/`.
6. Copy all text and paste it into Quizlet's import field.
7. Choose **Tab** between term and definition.
8. Choose **New line** between cards.
9. Import the terms.
10. Set term language to **German** and definition language to **Russian**.
11. Review the preview and create/publish the set.

After publishing, study it on web or in the Quizlet mobile app.

## Update an existing Quizlet set

For a small or targeted change:

1. Regenerate the canonical JSON and full Quizlet TXT through the normal repository PR.
2. Open the existing set in Quizlet.
3. Open the more/options menu and choose **Edit / Edit set**.
4. Reconcile the affected cards with the regenerated TXT: add new rows, edit changed terms/definitions, remove deleted rows, and reorder if needed.
5. Save/Done.

For a large rewrite, the documented bulk-import flow creates a new set rather than synchronizing over an existing one. The safe replacement workflow is:

1. Create a new Quizlet set from the regenerated full TXT.
2. Verify card count, languages, and a sample of changed cards.
3. Only after verification decide whether to keep, rename, or retire the old set.

Agents must never say that the Quizlet account was updated merely because a GitHub PR changed the TXT.

## Why TXT

Quizlet's official import workflow is copy/paste based rather than a proprietary deck file upload. Tab-separated UTF-8 text is deterministic, diffable in Git and easy to convert to other apps.

## Study orientation

In the vocabulary set the stored term is German and the definition is Russian meaning only. Grammar facts are practiced in separate sets so German morphology does not act as a multiple-choice hint in the vocabulary deck.

## Export back out

Quizlet can export terms/definitions from sets you created on its website. Use that exported text as input to the format-conversion workflow when needed.

## Anki

Anki is a supported fallback, not the default. Explicitly ask for an Anki version or for Quizlet -> Anki conversion.
