# Contributing

All changes to `lingua-cards` are Pull-Request-only.

## Required workflow

1. Fetch current `master`.
2. Create a dedicated branch.
3. Make the complete change.
4. Squash to exactly one commit.
5. Rebase that commit onto current `master`.
6. Run `python scripts/validate_repo.py`.
7. Open a PR.
8. If `master` changes, rebase again and keep the PR at exactly one commit.
9. Leave the PR open for the repository owner.

**Do not auto-merge PRs. Do not push directly to `master`.**

## Card changes

Card batches follow the same workflow as code/docs.

- canonical cards: `cards/by-key/<shard>/CARD-<sha256>.json`
- project grouping: `projects/<project-slug>/sets/<set-name>.json`
- no global index;
- no verb-table persistence.
