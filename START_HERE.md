# START HERE

Canonical bootstrap for any human or agent working with `ayatskiy/lingua-cards`.

1. Read `repo-context.json`.
2. Read `AGENTS.md`.
3. For new cards, read `docs/CARD_WORKFLOW.md`.
4. For format conversion, read `docs/FORMAT_CONVERSION.md`.
5. Remember: one canonical deck JSON contains many flashcards.
6. **Quizlet is the default target**; every deck must have a hint-free vocabulary file at `apps/quizlet/<project>/<deck>.txt`.
7. When canonical cards contain plural, verb-form or government data, generate separate Quizlet grammar sets under `apps/quizlet/<project>/<deck>-grammar-<kind>.txt`.
8. Anki is optional and belongs under `apps/anki/`.
9. Never push directly to `master`.
10. Every repository change uses a dedicated branch -> validation -> PR.
11. Every PR contains exactly one commit whose only parent is current `master`.
12. If `master` moves, rebase/squash back to one commit and rerun validation.
13. Never merge PRs automatically; return the direct PR URL.
14. Verb tables/grammar documents are generated outside this repository; Quizlet grammar flashcard sets remain app artifacts here.
15. For ordinary usage questions answer from the local app guide without web search unless current UI verification is explicitly requested.

Plugin source: `ayatskiy/ai-plugins/plugins/deutsch-lesson-cards`.
