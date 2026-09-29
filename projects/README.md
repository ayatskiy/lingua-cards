# projects/

Application-neutral canonical decks live here:

```text
projects/<project-slug>/decks/<deck-name>.json
```

Application-specific artifacts do **not** live here.

Use:
- `apps/quizlet/<project-slug>/<deck-name>.txt`
- `apps/anki/<project-slug>/<deck-name>.apkg`

Project/deck grouping is expressed by path and filename, not duplicated inside every flashcard.
