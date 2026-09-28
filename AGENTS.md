# AGENTS.md

Mandatory operating rules for every human contributor and AI/coding agent.

## 1. Bootstrap

At the start of every repository task:

1. read `START_HERE.md`;
2. read `repo-context.json`;
3. read this file;
4. load only task-relevant workflow/schema files.

## 2. Master is integration-only

**Never push or commit directly to `master`.**

This applies to documentation, schemas, CI, canonical cards, project card sets, and every other repository path. There are no small-change or runtime exceptions.

## 3. Required Pull Request shape

Every change must follow:

```text
latest master
-> dedicated branch
-> exactly ONE commit
-> validate
-> PR to master
-> checks pass
-> STOP and give the user the PR link
```

Rules:
- exactly one commit may exist in `master..HEAD`;
- the PR commit must have exactly one parent;
- that parent must equal current `master` HEAD;
- if `master` moves, rebase and squash back to one commit;
- no merge commits inside the PR branch;
- do not keep working on a stale PR branch.

The CI workflow `.github/workflows/pr-shape.yml` enforces the commit shape.

### Absolute no-auto-merge rule

Agents, plugins, automations, and assistants **must never merge a Pull Request in this repository**.

Even when:
- the user asked for the underlying change;
- CI is green;
- the PR is mergeable;
- previous repository conventions allowed merge-after-validation.

The correct completion is: leave the PR open and return its direct link. Only the human user merges it.

## 4. Card identity and deduplication

There is no global word index.

Canonical-key normalization must follow `docs/CARD_WORKFLOW.md` exactly. In particular, preserve German umlauts and `ß`, use NFC, collapse whitespace, use noun lemmas without articles, and keep reflexive/separable verb identity stable.

Normalize to:

`<part_of_speech>:<normalized_german_item>`

Then compute SHA-256 and derive:

`CARD-<64 hex chars>`

Path:

`cards/by-key/<first-2-hash-chars>/<card_id>.json`

Before creating a card, compute that exact path:
- if it exists and has the same `canonical_key`, the item is a duplicate;
- if it does not exist, create the canonical card;
- if it exists with a different key, stop and report an identity collision/corruption.

This deterministic lookup is the only canonical duplicate check.

## 5. Card storage model

Canonical cards contain only learning content:
- stable card ID;
- canonical key;
- German target;
- Russian meaning;
- part of speech;
- optional article/plural;
- optional verb forms when the **card itself** is a verb;
- optional government;
- optional German example;
- optional Russian example translation;
- optional concise grammar note.

Do not store project, lesson, date, source, provenance, chat ID, first/last-seen, review progress, or export history inside a card.

Per-project grouping:
- `projects/<project-slug>/sets/<set-name>.json`
- set manifest contains only `schema_version` and canonical card IDs.

## 6. Verbs are a separate output workflow

This repository does **not** store:
- source-wide verb inventories;
- tense tables;
- verb DOCX/PDF files;
- grammar study documents.

The separate verb skill may generate those files for the user, but it must not persist them to `lingua-cards`.

A verb may still be a normal vocabulary card when selected as useful vocabulary; in that case its card may contain its lexical forms.

## 7. Privacy

Before persisting content derived from private chats/files, verify repository visibility is private. If public, stop unless the user explicitly authorizes public storage of that content.

## 8. Generated artifacts

`.apkg`, TSV, DOCX, and PDF are generated delivery artifacts, not canonical Git state. Return them to the user rather than committing them here.

## 9. Validation

Run:

```bash
python scripts/validate_repo.py
```

PR CI must also pass the one-commit/up-to-date check.

## 10. User-facing reports

Every repository-change report must include the direct clickable PR URL. Never report a PR as merged unless the human user actually merged it.
