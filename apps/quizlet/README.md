# apps/quizlet

Primary/default study format.

Vocabulary path:

`apps/quizlet/<project-slug>/<deck-name>.txt`

Vocabulary format: UTF-8 text, no header, one card per line:

`German<TAB>Russian meaning`

Do not append German plural forms, verb forms, government or German examples to the vocabulary definition. Those create answer clues in Quizlet study modes.

Derived grammar paths use:

`apps/quizlet/<project-slug>/<deck-name>-grammar-<kind>.txt`

Supported kinds are `plural`, `praesens-3sg`, `praeteritum`, `partizip-ii`, `perfekt`, and `rektion`. Generate a set when the canonical deck contains that data. Grammar rows should test one fact per card.

Every canonical deck must have the vocabulary Quizlet TXT artifact. Grammar sets are required when their source fields are present.
