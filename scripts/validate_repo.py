#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md","START_HERE.md","AGENTS.md","CONTRIBUTING.md","repo-context.json",
    "docs/CARD_WORKFLOW.md","docs/ANKIDROID_GUIDE.md","cards/README.md","projects/README.md",
    "schemas/card.schema.json","schemas/card-set.schema.json",
    ".github/pull_request_template.md",".github/workflows/validate.yml",".github/workflows/pr-shape.yml",
]

errors = 0

def fail(msg):
    global errors
    print(f"ERROR: {msg}")
    errors += 1

for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        fail(f"missing required file: {rel}")

for forbidden_path in ["cards/index.json","schemas/card-index.schema.json","verbs","exports/verbs"]:
    if (ROOT / forbidden_path).exists():
        fail(f"forbidden legacy/storage path exists: {forbidden_path}")

for rel in ["repo-context.json","schemas/card.schema.json","schemas/card-set.schema.json"]:
    p = ROOT / rel
    if p.is_file():
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"invalid JSON in {rel}: {exc}")

ctx_path = ROOT / "repo-context.json"
if ctx_path.is_file():
    ctx = json.loads(ctx_path.read_text(encoding="utf-8"))
    if ctx.get("repository") != "ayatskiy/lingua-cards":
        fail("repository mismatch")
    if ctx.get("write_mode") != "pull_request_only":
        fail("write_mode must be pull_request_only")
    if ctx.get("merge_policy") != "human_only_never_auto_merge":
        fail("merge policy must forbid agent auto-merge")
    pr = ctx.get("pr_contract", {})
    if pr.get("commits_exactly") != 1:
        fail("PR contract must require exactly one commit")
    if pr.get("must_be_rebased_on_current_master") is not True:
        fail("PR contract must require rebase on current master")
    if pr.get("direct_master_push") is not False:
        fail("direct master pushes must be forbidden")
    if ctx.get("identity", {}).get("global_index") is not False:
        fail("global index must remain disabled")

forbidden_fields = {
    "created_date","date","project","project_id","lesson","lesson_id",
    "first_seen_lesson","last_seen_lesson","first_seen_date","last_seen_date",
    "seen_in_lessons","source","source_id","source_refs","provenance",
    "export_status","export_batch","chat_id","conversation_id","review_progress"
}

card_re = re.compile(r"^CARD-([0-9a-f]{64})$")
for path in sorted((ROOT / "cards" / "by-key").glob("*/*.json")) if (ROOT / "cards" / "by-key").exists() else []:
    try:
        card = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid card JSON {path}: {exc}")
        continue
    bad = sorted(forbidden_fields.intersection(card))
    if bad:
        fail(f"{path} contains forbidden metadata: {', '.join(bad)}")
    match = card_re.match(card.get("card_id", ""))
    if not match:
        fail(f"{path} has invalid card_id")
        continue
    expected_hash = hashlib.sha256(card.get("canonical_key","").encode("utf-8")).hexdigest()
    if match.group(1) != expected_hash:
        fail(f"{path} card_id does not match sha256(canonical_key)")
    expected = ROOT / "cards" / "by-key" / expected_hash[:2] / f"CARD-{expected_hash}.json"
    if path != expected:
        fail(f"{path} is not stored at deterministic path {expected.relative_to(ROOT)}")
    if card.get("schema_version") != 3:
        fail(f"{path} must use schema_version 3")

for path in sorted((ROOT / "projects").glob("*/sets/*.json")) if (ROOT / "projects").exists() else []:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid set JSON {path}: {exc}")
        continue
    if set(data) != {"schema_version","cards"}:
        fail(f"{path} may contain only schema_version and cards")
    if data.get("schema_version") != 2:
        fail(f"{path} must use schema_version 2")
    cards = data.get("cards")
    if not isinstance(cards, list) or len(cards) != len(set(cards)):
        fail(f"{path} cards must be a unique list")
        continue
    for card_id in cards:
        m = card_re.match(card_id)
        if not m:
            fail(f"{path} contains invalid card id {card_id}")
            continue
        h = m.group(1)
        card_path = ROOT / "cards" / "by-key" / h[:2] / f"{card_id}.json"
        if not card_path.is_file():
            fail(f"{path} references missing card {card_id}")

if errors:
    print(f"Validation failed with {errors} error(s).")
    sys.exit(1)

print("lingua-cards validation passed.")
