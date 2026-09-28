#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md","START_HERE.md","AGENTS.md","repo-context.json",
    "docs/CARD_WORKFLOW.md","cards/README.md","cards/index.json",
    "schemas/card.schema.json","schemas/card-index.schema.json",
    "exports/README.md"
]
errors = 0
for rel in required:
    if not (ROOT / rel).is_file():
        print(f"ERROR: missing {rel}")
        errors += 1

for rel in ["repo-context.json","cards/index.json","schemas/card.schema.json","schemas/card-index.schema.json"]:
    try:
        json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: invalid JSON in {rel}: {exc}")
        errors += 1

if not errors:
    ctx = json.loads((ROOT / "repo-context.json").read_text(encoding="utf-8"))
    if ctx.get("repository") != "ayatskiy/lingua-cards":
        print("ERROR: repository mismatch")
        errors += 1
    if ctx.get("runtime_branch") != "runtime/cards":
        print("ERROR: runtime branch must be runtime/cards")
        errors += 1
    idx = json.loads((ROOT / "cards/index.json").read_text(encoding="utf-8"))
    if idx.get("schema_version") != 1 or not isinstance(idx.get("entries"), dict):
        print("ERROR: invalid card index shape")
        errors += 1

if errors:
    sys.exit(1)
print("lingua-cards validation passed")
