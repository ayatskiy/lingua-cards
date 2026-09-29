# START HERE

Canonical bootstrap for any human or agent working with `ayatskiy/lingua-cards`.

1. Read `repo-context.json`.
2. Read `AGENTS.md`.
3. For card work, read `docs/CARD_WORKFLOW.md` and the schemas.
4. Never push directly to `master`.
5. Every change, including a card batch, must use a dedicated branch -> validation -> Pull Request.
6. Every PR must contain exactly one commit.
7. That commit must have the current `master` HEAD as its only parent.
8. If `master` moves, rebase/squash back to one commit and rerun checks.
9. **Never merge a PR automatically.** Leave it open for the user and return its direct URL.
10. Before persisting private conversation/file content, verify repository visibility is private unless the user explicitly authorizes public storage.
11. This repository stores cards only. Verb tables/grammar documents are generated outside it.
12. For user questions such as «как пользоваться карточками», «как импортировать .apkg», «какое приложение поставить», or «где смотреть прогресс», read `docs/ANKIDROID_GUIDE.md` and answer from it without web search unless the user explicitly asks for current version-specific verification.

Plugin source: `ayatskiy/ai-plugins/plugins/deutsch-lesson-cards`.
