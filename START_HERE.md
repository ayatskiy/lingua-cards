# START HERE

Canonical bootstrap for any human or agent working with `ayatskiy/lingua-cards`.

1. Read `repo-context.json`.
2. Read `AGENTS.md`.
3. For new cards, read `docs/CARD_WORKFLOW.md`.
4. For format conversion, read `docs/FORMAT_CONVERSION.md`.
5. Remember: one canonical deck JSON contains many flashcards.
6. **Quizlet is the default target**; every deck must have `apps/quizlet/<project>/<deck>.txt`.
7. Anki is optional and belongs under `apps/anki/`.
8. Never push directly to `master`.
9. Every repository change uses a dedicated branch -> validation -> PR.
10. Every PR contains exactly one commit whose only parent is current `master`.
11. If `master` moves, rebase/squash back to one commit and rerun validation.
12. Never merge PRs automatically; return the direct PR URL.
13. Verb tables/grammar documents are generated outside this repository.
14. For ordinary usage questions answer from the local app guide without web search unless current UI verification is explicitly requested.

Plugin source: `ayatskiy/ai-plugins/plugins/deutsch-lesson-cards`.
