## Summary

<!-- What changed and why? -->

## Required checks

- [ ] This PR contains exactly one commit.
- [ ] The commit is rebased directly on current `master`.
- [ ] No direct-master write was used.
- [ ] `python scripts/validate_repo.py` passes.
- [ ] Canonical deck JSON is application-neutral.
- [ ] Every canonical deck has a Quizlet TXT under `apps/quizlet/`.
- [ ] Anki artifacts, if present, live only under `apps/anki/`.
- [ ] Dedupe shards are consistent with canonical deck JSON.
- [ ] Flashcards contain no source/chat/project/date/history metadata.
- [ ] No verb inventory/DOCX/PDF is persisted here.
- [ ] The PR stays open for the human owner; no agent auto-merge.
