#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = 0

REQUIRED = [
    "README.md","START_HERE.md","AGENTS.md","CONTRIBUTING.md","repo-context.json",
    "docs/CARD_WORKFLOW.md","docs/ANKIDROID_GUIDE.md","projects/README.md","dedupe/README.md",
    "schemas/deck.schema.json","schemas/dedupe-shard.schema.json",
    ".github/pull_request_template.md",".github/workflows/validate.yml",".github/workflows/pr-shape.yml",
]

def fail(msg):
    global errors
    print(f"ERROR: {msg}")
    errors += 1

for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        fail(f"missing required file: {rel}")

for forbidden in [
    "cards/README.md","cards/index.json","cards/by-key",
    "schemas/card.schema.json","schemas/card-set.schema.json","schemas/card-index.schema.json",
    "exports/verbs","verbs"
]:
    if (ROOT / forbidden).exists():
        fail(f"forbidden legacy/storage path exists: {forbidden}")

for rel in ["repo-context.json","schemas/deck.schema.json","schemas/dedupe-shard.schema.json"]:
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
        fail("merge policy must forbid auto-merge")
    storage = ctx.get("storage", {})
    if storage.get("global_single_index") is not False:
        fail("single global index must be disabled")
    if storage.get("per_word_files") is not False:
        fail("per-word repository files must be disabled")

key_re = re.compile(r"^[a-z_]+:.+$")
deck_keys = {}
deck_paths = {}

for path in sorted((ROOT / "projects").glob("*/decks/*.json")) if (ROOT / "projects").exists() else []:
    rel = path.relative_to(ROOT).as_posix()
    try:
        deck = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid deck JSON {rel}: {exc}")
        continue
    if set(deck) != {"schema_version","cards"} or deck.get("schema_version") != 1:
        fail(f"{rel} has invalid deck shape")
        continue
    cards = deck.get("cards")
    if not isinstance(cards, list):
        fail(f"{rel} cards must be an array")
        continue
    seen = set()
    for i, card in enumerate(cards):
        if not isinstance(card, dict):
            fail(f"{rel} card #{i+1} must be an object")
            continue
        ck = card.get("canonical_key")
        if not isinstance(ck, str) or not key_re.match(ck):
            fail(f"{rel} card #{i+1} has invalid canonical_key")
            continue
        if ck in seen:
            fail(f"{rel} duplicates {ck} inside one deck")
        seen.add(ck)
        if ck in deck_keys:
            fail(f"{ck} appears in multiple decks: {deck_keys[ck]} and {rel}")
        deck_keys[ck] = rel
        deck_paths.setdefault(rel, set()).add(ck)

shard_entries = {}
dedupe_dir = ROOT / "dedupe"
for path in sorted(dedupe_dir.glob("[0-9a-f][0-9a-f].json")) if dedupe_dir.exists() else []:
    rel = path.relative_to(ROOT).as_posix()
    try:
        shard = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid dedupe shard {rel}: {exc}")
        continue
    if set(shard) != {"schema_version","entries"} or shard.get("schema_version") != 1 or not isinstance(shard.get("entries"), dict):
        fail(f"{rel} has invalid shard shape")
        continue
    expected_name = path.stem
    for ck, deck_path in shard["entries"].items():
        expected_shard = hashlib.sha256(ck.encode("utf-8")).hexdigest()[:2]
        if expected_shard != expected_name:
            fail(f"{ck} belongs in dedupe/{expected_shard}.json, not {rel}")
        if ck in shard_entries:
            fail(f"{ck} appears in multiple shards")
        shard_entries[ck] = deck_path
        target = ROOT / deck_path
        if not target.is_file():
            fail(f"{rel} points {ck} to missing deck {deck_path}")
        elif ck not in deck_paths.get(deck_path, set()):
            fail(f"{rel} points {ck} to {deck_path}, but deck does not contain key")

for ck, deck_path in deck_keys.items():
    shard = hashlib.sha256(ck.encode("utf-8")).hexdigest()[:2]
    if shard_entries.get(ck) != deck_path:
        fail(f"{deck_path} contains {ck}, but dedupe/{shard}.json mapping is missing or wrong")

if errors:
    print(f"Validation failed with {errors} error(s).")
    sys.exit(1)

print("lingua-cards validation passed.")
