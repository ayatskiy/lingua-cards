# START HERE

Canonical bootstrap for any human or agent working with `ayatskiy/lingua-cards`.

1. Read `repo-context.json`.
2. Read `AGENTS.md`.
3. For new cards, read `docs/CARD_WORKFLOW.md`.
4. For format conversion, read `docs/FORMAT_CONVERSION.md`.
5. Remember: one canonical deck JSON contains many flashcards.
6. **Quizlet is the default target**; every deck must have a hint-free vocabulary file at `apps/quizlet/<project>/<deck>.txt`.
7. When canonical cards contain verbs, generate `apps/quizlet/<project>/<deck>-verbs.txt`; when they contain grammar data, generate focused `-grammar-<kind>.txt` sets, including `grammar-notes` when `grammar_note` exists.
8. Requests containing both «глаголы/грамматика» and «карточки» stay in the card workflow; standalone verb-table requests remain separate.
9. Anki is optional and belongs under `apps/anki/`.
10. Never push directly to `master`.
11. Every repository change uses a dedicated branch -> validation -> PR.
12. Every PR contains exactly one commit whose only parent is current `master`.
13. If `master` moves, rebase/squash back to one commit and rerun validation.
14. Never merge PRs automatically; return the direct PR URL.
15. Verb tables/grammar documents are generated outside this repository; Quizlet verb/grammar flashcard sets remain app artifacts here.
16. For ordinary usage questions answer from the local app guide without web search unless current UI verification is explicitly requested.

Plugin source: `ayatskiy/ai-plugins/plugins/deutsch-lesson-cards`.
