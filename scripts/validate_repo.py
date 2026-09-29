#!/usr/bin/env python3
import hashlib
import json
import re
import sqlite3
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = 0

REQUIRED = [
    "README.md","START_HERE.md","AGENTS.md","CONTRIBUTING.md","repo-context.json",
    "docs/CARD_WORKFLOW.md","docs/FORMAT_CONVERSION.md","docs/QUIZLET_GUIDE.md","docs/ANKIDROID_GUIDE.md",
    "projects/README.md","apps/quizlet/README.md","apps/anki/README.md","dedupe/README.md",
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

for forbidden in ["cards/README.md","cards/index.json","cards/by-key","exports/verbs","verbs"]:
    if (ROOT / forbidden).exists():
        fail(f"forbidden legacy/storage path exists: {forbidden}")

legacy_apkg = list((ROOT / "projects").glob("*/decks/*.apkg")) if (ROOT / "projects").exists() else []
for p in legacy_apkg:
    fail(f"app artifact must not live beside canonical JSON: {p.relative_to(ROOT)}")

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
    if storage.get("default_app") != "quizlet":
        fail("Quizlet must be the default app")
    if storage.get("required_default_artifact") != "quizlet":
        fail("Quizlet artifact must be required")
    if storage.get("anki_required") is not False:
        fail("Anki must remain optional")
    if storage.get("global_single_index") is not False:
        fail("single global index must be disabled")
    if storage.get("per_word_files") is not False:
        fail("per-word files must be disabled")

key_re = re.compile(r"^[a-z_]+:.+$")
deck_keys = {}
deck_cards = {}

GRAMMAR_KINDS = (
    "plural",
    "praesens-3sg",
    "praeteritum",
    "partizip-ii",
    "perfekt",
    "rektion",
    "notes",
)

def canonical_lemma(card):
    ck = card.get("canonical_key", "")
    return ck.split(":", 1)[1] if ":" in ck else card.get("german", "")

def render_vocab(card):
    return f"{card.get('german', '')}\t{card.get('russian', '')}"

def render_verbs(cards):
    return [render_vocab(card) for card in cards if card.get("part_of_speech") == "verb"]

def render_grammar(cards, kind):
    rows = []
    for card in cards:
        if kind == "plural" and card.get("plural"):
            rows.append(f"{card['german']} — Plural\tdie {card['plural']}")
        elif kind == "praesens-3sg" and card.get("verb_forms", {}).get("praesens_3sg"):
            rows.append(f"{canonical_lemma(card)} — Präsens (er/sie/es)\t{card['verb_forms']['praesens_3sg']}")
        elif kind == "praeteritum" and card.get("verb_forms", {}).get("praeteritum"):
            rows.append(f"{canonical_lemma(card)} — Präteritum\t{card['verb_forms']['praeteritum']}")
        elif kind == "partizip-ii" and card.get("verb_forms", {}).get("partizip_ii"):
            rows.append(f"{canonical_lemma(card)} — Partizip II\t{card['verb_forms']['partizip_ii']}")
        elif kind == "perfekt" and card.get("verb_forms", {}).get("perfekt"):
            rows.append(f"{canonical_lemma(card)} — Perfekt\t{card['verb_forms']['perfekt']}")
        elif kind == "rektion" and card.get("government"):
            rows.append(f"{canonical_lemma(card)} — Rektion\t{card['government']}")
        elif kind == "notes" and card.get("grammar_note"):
            rows.append(f"{card['german']} — Grammatik\t{card['grammar_note']}")
    return rows

for path in sorted((ROOT / "projects").glob("*/decks/*.json")) if (ROOT / "projects").exists() else []:
    rel = path.relative_to(ROOT).as_posix()
    project = path.parent.parent.name
    name = path.stem
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

    deck_cards[rel] = cards

    # Hint-free Quizlet vocabulary is required and must be an exact canonical view.
    qpath = ROOT / "apps" / "quizlet" / project / f"{name}.txt"
    if not qpath.is_file():
        fail(f"{rel} is missing required Quizlet artifact {qpath.relative_to(ROOT)}")
    else:
        try:
            lines = [line for line in qpath.read_text(encoding="utf-8").splitlines() if line.strip()]
            expected = [render_vocab(card) for card in cards]
            if lines != expected:
                fail(f"{qpath.relative_to(ROOT)} must exactly match canonical German<TAB>Russian meaning rows without German answer clues")
        except Exception as exc:
            fail(f"invalid Quizlet artifact {qpath.relative_to(ROOT)}: {exc}")

    # A verbs-only Quizlet view is required whenever canonical verb cards exist.
    expected_verbs = render_verbs(cards)
    vpath = ROOT / "apps" / "quizlet" / project / f"{name}-verbs.txt"
    if expected_verbs:
        if not vpath.is_file():
            fail(f"{rel} is missing derived Quizlet verbs artifact {vpath.relative_to(ROOT)}")
        else:
            try:
                lines = [line for line in vpath.read_text(encoding="utf-8").splitlines() if line.strip()]
                if lines != expected_verbs:
                    fail(f"{vpath.relative_to(ROOT)} does not exactly match canonical verb rows")
            except Exception as exc:
                fail(f"invalid Quizlet verbs artifact {vpath.relative_to(ROOT)}: {exc}")
    elif vpath.exists():
        fail(f"{vpath.relative_to(ROOT)} exists but canonical deck has no verb cards")

    # Grammar Quizlet sets are required whenever canonical source fields are available.
    for kind in GRAMMAR_KINDS:
        expected = render_grammar(cards, kind)
        gpath = ROOT / "apps" / "quizlet" / project / f"{name}-grammar-{kind}.txt"
        if expected:
            if not gpath.is_file():
                fail(f"{rel} is missing derived Quizlet grammar artifact {gpath.relative_to(ROOT)}")
            else:
                try:
                    lines = [line for line in gpath.read_text(encoding="utf-8").splitlines() if line.strip()]
                    if lines != expected:
                        fail(f"{gpath.relative_to(ROOT)} does not exactly match canonical {kind} rows")
                    for i, line in enumerate(lines, start=1):
                        if line.count("\t") != 1:
                            fail(f"{gpath.relative_to(ROOT)} row {i} must contain exactly one TAB")
                except Exception as exc:
                    fail(f"invalid Quizlet grammar artifact {gpath.relative_to(ROOT)}: {exc}")
        elif gpath.exists():
            fail(f"{gpath.relative_to(ROOT)} exists but canonical deck has no {kind} data")

    # Anki is optional.
    apath = ROOT / "apps" / "anki" / project / f"{name}.apkg"
    if apath.is_file():
        try:
            with zipfile.ZipFile(apath, "r") as z:
                names = set(z.namelist())
                cname = "collection.anki2" if "collection.anki2" in names else ("collection.anki21" if "collection.anki21" in names else None)
                if not cname:
                    fail(f"{apath.relative_to(ROOT)} has no Anki collection database")
                    continue
                data = z.read(cname)
            with tempfile.NamedTemporaryFile(suffix=".anki2") as tmp:
                tmp.write(data); tmp.flush()
                con = sqlite3.connect(tmp.name)
                cc = con.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
                nc = con.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
                con.close()
            if cc != len(cards) or nc != len(cards):
                fail(f"{apath.relative_to(ROOT)} has {cc} cards/{nc} notes; expected {len(cards)}")
        except Exception as exc:
            fail(f"invalid Anki artifact {apath.relative_to(ROOT)}: {exc}")

# No orphan app artifacts.
grammar_name_re = re.compile(r"^(?P<deck>.+)-grammar-(?P<kind>plural|praesens-3sg|praeteritum|partizip-ii|perfekt|rektion|notes)$")
for qpath in sorted((ROOT / "apps" / "quizlet").glob("*/*.txt")) if (ROOT / "apps" / "quizlet").exists() else []:
    project, artifact_name = qpath.parent.name, qpath.stem
    direct = ROOT / "projects" / project / "decks" / f"{artifact_name}.json"
    if direct.is_file():
        continue
    if artifact_name.endswith("-verbs"):
        deck_name = artifact_name[:-6]
    else:
        match = grammar_name_re.match(artifact_name)
        deck_name = match.group("deck") if match else artifact_name
    canonical = ROOT / "projects" / project / "decks" / f"{deck_name}.json"
    if not canonical.is_file():
        fail(f"orphan Quizlet artifact: {qpath.relative_to(ROOT)}")

for apath in sorted((ROOT / "apps" / "anki").glob("*/*.apkg")) if (ROOT / "apps" / "anki").exists() else []:
    project, name = apath.parent.name, apath.stem
    canonical = ROOT / "projects" / project / "decks" / f"{name}.json"
    if not canonical.is_file():
        fail(f"orphan Anki artifact: {apath.relative_to(ROOT)}")

# Dedupe validation.
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
    for ck, deck_path in shard["entries"].items():
        expected = hashlib.sha256(ck.encode("utf-8")).hexdigest()[:2]
        if path.stem != expected:
            fail(f"{ck} belongs in dedupe/{expected}.json, not {rel}")
        if ck in shard_entries:
            fail(f"{ck} appears in multiple shards")
        shard_entries[ck] = deck_path
        cards = deck_cards.get(deck_path)
        if cards is None:
            fail(f"{rel} points {ck} to missing deck {deck_path}")
        elif ck not in {c.get("canonical_key") for c in cards}:
            fail(f"{rel} points {ck} to {deck_path}, but deck does not contain key")

for ck, deck_path in deck_keys.items():
    shard = hashlib.sha256(ck.encode("utf-8")).hexdigest()[:2]
    if shard_entries.get(ck) != deck_path:
        fail(f"{deck_path} contains {ck}, but dedupe/{shard}.json mapping is missing or wrong")

if errors:
    print(f"Validation failed with {errors} error(s).")
    sys.exit(1)

print("lingua-cards validation passed.")
