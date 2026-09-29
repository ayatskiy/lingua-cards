# Quizlet User Guide

This is the default card workflow.

## What the plugin gives you

For every deck the repository stores:

- canonical source: `projects/<project>/decks/<name>.json`;
- Quizlet import text: `apps/quizlet/<project>/<name>.txt`.

The default vocabulary TXT is UTF-8 text with one flashcard per line and a TAB between the German term and Russian meaning. It intentionally excludes German morphology from the definition side so Quizlet study modes do not leak the answer. When canonical data contains verbs, a derived `<deck>-verbs.txt` is generated; when it contains plural, verb forms, government or `grammar_note`, separate grammar TXT sets are generated.

## Vocabulary, verbs and grammar sets

The main `<deck>.txt` contains only `German<TAB>Russian meaning`.

`<deck>-verbs.txt` contains only the canonical verb cards from the same lesson deck, using the same hint-free row format.

Derived files such as `<deck>-grammar-plural.txt`, `<deck>-grammar-praesens-3sg.txt`, `<deck>-grammar-praeteritum.txt`, `<deck>-grammar-partizip-ii.txt`, `<deck>-grammar-perfekt.txt` and `<deck>-grammar-rektion.txt`, plus `<deck>-grammar-notes.txt` when notes exist, keep morphology/government/grammar practice separate from vocabulary recognition.

## Repository snapshot vs Quizlet account

The repository TXT is the complete current snapshot of the deck. Updating `apps/quizlet/<project>/<deck>.txt` in GitHub does **not** automatically update an already-published Quizlet set.

Use one of the workflows below.

## Create through the connected Quizlet action

If the current ChatGPT runtime exposes the connected Quizlet action, the learner may ask for GitHub + Quizlet in one command or later ask to create a Quizlet set from an existing GitHub deck.

New lesson material must still go to GitHub first: branch -> validation -> PR, with the PR left open. The Quizlet action is then allowed to create a **new** set from the canonical content. It cannot update an existing Quizlet set.

The Quizlet action is asynchronous and generative. The agent must wait until generation status reports `complete` before reporting a set/link, instruct generation to preserve the exact requested card count/pairs and add nothing, and avoid claiming a deterministic TXT import unless a supported full read-back verifies it.

If deterministic fidelity is required, or the action is unavailable, use the website TXT import below.

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
