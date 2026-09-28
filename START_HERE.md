# START HERE

Canonical bootstrap for agents working with `ayatskiy/lingua-cards`.

1. Read `repo-context.json`.
2. Read `AGENTS.md`.
3. For card creation, read `docs/CARD_WORKFLOW.md`, `schemas/card.schema.json`, and `schemas/card-index.schema.json`.
4. Development changes always use a dedicated branch and Pull Request.
5. Runtime card writes use only `runtime/cards` and only the paths allowed by `docs/CARD_WORKFLOW.md`.
6. Before any runtime write, verify repository visibility is private. If it is public, stop and report that persistence is blocked for privacy.
7. Always verify a write by reading back the updated index and at least one touched record.
8. Every user-facing repository-change report must include the direct PR URL.

The connected plugin source lives in `ayatskiy/ai-plugins/plugins/deutsch-lesson-cards`.
