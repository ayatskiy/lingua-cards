# Quizlet User Guide

This is the default card workflow.

## What the plugin gives you

For every deck the repository stores:

- canonical source: `projects/<project>/decks/<name>.json`;
- Quizlet import text: `apps/quizlet/<project>/<name>.txt`.

The Quizlet TXT is UTF-8 text with one flashcard per line and a TAB between German term and Russian definition.

## Import into Quizlet

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

## Why TXT

Quizlet's official import workflow is copy/paste based rather than a proprietary deck file upload. Tab-separated UTF-8 text is deterministic, diffable in Git and easy to convert to other apps.

## Study orientation

The stored term is German and the definition is Russian plus useful notes. Quizlet study modes can change which side is shown/answered, so you can use both recognition and active recall.

## Export back out

Quizlet can export terms/definitions from sets you created on its website. Use that exported text as input to the format-conversion workflow when needed.

## Anki

Anki is a supported fallback, not the default. Explicitly ask for an Anki version or for Quizlet -> Anki conversion.
