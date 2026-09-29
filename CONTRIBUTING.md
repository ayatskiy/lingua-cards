# Contributing

All changes to `lingua-cards` are Pull-Request-only.

Required workflow:

1. start from latest `master`;
2. create a dedicated branch;
3. make the full change;
4. squash to exactly one commit;
5. rebase that commit onto current `master`;
6. run `python scripts/validate_repo.py`;
7. open a PR;
8. if master moves, rebase again and rerun checks;
9. leave the PR open for the human owner.

Do not auto-merge. Do not push directly to `master`.

Content model:
- one deck file contains many flashcards;
- deck path: `projects/<project-slug>/decks/<deck-name>.json`;
- duplicate registry: `dedupe/<00-ff>.json`;
- no per-word repository files.
