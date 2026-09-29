# Contributing

All changes are Pull-Request-only.

1. start from latest `master`;
2. create a dedicated branch;
3. make the complete change;
4. squash/rebuild to exactly one commit;
5. rebase that commit onto current `master`;
6. run `python scripts/validate_repo.py`;
7. open a PR;
8. if master moves, rebase/regenerate and rerun checks;
9. leave the PR open for the human owner.

Do not auto-merge. Do not push directly to `master`.

Storage:
- canonical deck: `projects/<project>/decks/<deck>.json`;
- default Quizlet artifact: `apps/quizlet/<project>/<deck>.txt`;
- optional Anki artifact: `apps/anki/<project>/<deck>.apkg`;
- dedupe registry: `dedupe/<00-ff>.json`.
