# START HERE

Canonical bootstrap for any human or agent working with `ayatskiy/lingua-cards`.

1. Read `repo-context.json`.
2. Read `AGENTS.md`.
3. Read `docs/CARD_WORKFLOW.md` before creating decks.
4. Remember: **one deck file contains many flashcards**.
5. Never push directly to `master`.
6. Every change, including a deck batch, uses a dedicated branch -> validation -> Pull Request.
7. Every PR contains exactly one commit.
8. That commit must have current `master` HEAD as its only parent.
9. If `master` moves, rebase/squash back to one commit and rerun dedupe checks.
10. Never merge PRs automatically. Leave them open and return the direct URL.
11. Before persisting private content, verify repository visibility is private unless public storage was explicitly authorized.
12. Verb tables/grammar documents are generated outside this repository.
13. For ordinary AnkiDroid usage questions, answer from `docs/ANKIDROID_GUIDE.md` without web search unless current version-specific UI verification is explicitly requested.

Plugin source: `ayatskiy/ai-plugins/plugins/deutsch-lesson-cards`.
