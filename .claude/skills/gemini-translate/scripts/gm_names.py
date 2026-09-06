#!/usr/bin/env python3
"""gm_names.py — pin one spelling per recurring proper name, then re-run the blocks that drift.

Spot-reading the first full corpus run (2026-09-06) found the content sound but
the *spelling* of recurring names unstable across blocks: Hindi Oḍḍiyāna came
back as उड्डियान 33 times and as five other spellings 18 times; Nepali rendered
Thötreng Tsal three ways in one text. Meaning was never lost — the identity is
always right — but a display translation should spell a name one way.

Three passes, each idempotent:

  --propose   one Gemini call: the canonical rendering of each name in NAMES,
              in this language, under the track's own style.md. Appended to
              <track>/glossary.tsv (existing keys are kept, not overwritten), so
              every later call that touches the name sees "Terminology already
              fixed for this text".
  --check     scan the ledgers: a block whose source contains a glossary name
              but whose translation does not contain the canonical rendering is
              a candidate. Prints them per text; makes no calls.
  --rerun     re-translate exactly those blocks (`gm_translate.py --force
              --only …`, glossary in context), then re-stamp the track. Prints
              what still lacks the canonical form afterwards — it is raw model
              output, so a residue is possible and is reported, not hidden.

Every glossary entry is checked, not only names: an interjection or a mantra
syllable pinned in the glossary is held to the same one-spelling rule. A
rendering's parenthesised gloss (for the model's benefit) is not part of the
pinned form.

Usage:
    gm_names.py --lang hindi --propose
    gm_names.py --lang hindi --check
    gm_names.py --lang hindi --rerun [--limit N]
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
VAULT = HERE.parents[3]
GM = HERE / "gm_translate.py"
STAMP = VAULT / "4-SYSTEM" / "scripts" / "stamp_metadata.py"

sys.path.insert(0, str(HERE))
from gm_translate import DEFAULT_MODEL, DEFAULT_TRACK_ROOT, KEY_ENV, LANG_TAGS  # noqa: E402
from gm_titles import call as gemini_call  # noqa: E402  (JSON call with retries)

# Tibetan spelling(s) -> identity. Several Tibetan spellings of one name share a
# canonical rendering; the identity string is what the model is asked to name.
NAMES = [
    (["ཨོ་རྒྱན", "ཨུ་རྒྱན"], "Oḍḍiyāna (the land; also used as an epithet of Padmasambhava, 'the one from Oḍḍiyāna')"),
    (["པདྨ་འབྱུང་གནས"], "Padmasambhava (Pema Jungne, 'Lotus-Born')"),
    (["གུ་རུ་རིན་པོ་ཆེ"], "Guru Rinpoche"),
    (["ཐོད་ཕྲེང་རྩལ", "ཐོད་འཕྲེང་རྩལ"], "Thötreng Tsal (Tötrengtsal, Padmasambhava's wrathful name)"),
    (["ཚེ་དཔག་མེད"], "Amitāyus (Buddha of Limitless Life)"),
    (["འོད་དཔག་མེད"], "Amitābha (Buddha of Limitless Light)"),
    (["སྤྱན་རས་གཟིགས"], "Avalokiteśvara (Chenrezig)"),
    (["འཇམ་དཔལ་དབྱངས", "འཇམ་དཔལ"], "Mañjuśrī"),
    (["སྒྲོལ་མ"], "Tārā"),
    (["ཕྱག་ན་རྡོ་རྗེ"], "Vajrapāṇi"),
    (["ཤཱཀྱ་ཐུབ་པ"], "Śākyamuni"),
    (["རྡོ་རྗེ་འཆང"], "Vajradhara"),
    (["རྡོ་རྗེ་སེམས་དཔའ"], "Vajrasattva"),
    (["ཀུན་ཏུ་བཟང་པོ"], "Samantabhadra"),
    (["བྱམས་པ"], "Maitreya"),
    (["རྟ་མགྲིན"], "Hayagrīva"),
    (["ཙོང་ཁ་པ"], "Tsongkhapa"),
    (["བློ་བཟང་གྲགས་པ"], "Lobsang Drakpa (Tsongkhapa's ordination name)"),
    (["མི་ལ་རས་པ"], "Milarepa"),
    (["ཡེ་ཤེས་མཚོ་རྒྱལ"], "Yeshe Tsogyal"),
    (["ཆེ་མཆོག"], "Chemchok (Mahottara Heruka)"),
    (["དགའ་རབ་རྡོ་རྗེ"], "Garab Dorje (Prahevajra)"),
    (["ཤཱནྟ་རཀྵི་ཏ", "ཞི་བ་འཚོ"], "Śāntarakṣita"),
    (["ཁྲི་སྲོང་ལྡེའུ་བཙན", "ཁྲི་སྲོང་ལྡེ་བཙན"], "Trisong Detsen (the Tibetan king)"),
    (["བི་མ་ལ་མི་ཏྲ"], "Vimalamitra"),
    (["ཀློང་ཆེན"], "Longchenpa (Longchen Rabjam)"),
    (["ཨ་ཏི་ཤ"], "Atiśa"),
    (["བསམ་ཡས"], "Samye (the monastery)"),
    (["ཟངས་མདོག་དཔལ་རི"], "Zangdok Palri (the Copper-Coloured Mountain)"),
    (["ཛམྦུ་གླིང"], "Jambudvīpa"),
    (["བོད་ཡུལ", "བོད"], "Tibet"),
]

SCHEMA = {
    "type": "object",
    "properties": {"names": {"type": "array", "items": {"type": "object", "properties": {
        "id": {"type": "integer"}, "rendering": {"type": "string"}, "note": {"type": "string"}},
        "required": ["id", "rendering", "note"]}}},
    "required": ["names"],
}


def track_dir(tag):
    return VAULT / DEFAULT_TRACK_ROOT / tag


def read_glossary(path):
    out = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        for sep in ("\t", " -> ", " → ", "|"):
            if sep in line:
                s, t = line.split(sep, 1)
                out.append((s.strip(), t.strip()))
                break
    return out


def propose(lang, tag, model, key):
    style = (track_dir(tag) / "style.md").read_text(encoding="utf-8").strip()
    rows = [{"id": i, "tibetan": tibs, "identity": ident} for i, (tibs, ident) in enumerate(NAMES, 1)]
    prompt = (
        f"You are fixing the ONE spelling that each of these proper names will have throughout a "
        f"{lang} translation of Tibetan Buddhist liturgy. The translation's style instruction is:\n\n"
        f"{style}\n\nFor each name give exactly the form that instruction implies — the established "
        f"{lang} form where one exists, otherwise the transliteration the instruction asks for — as a "
        f"bare stem with no honorific, no case ending, no article, and no alternatives. Return JSON "
        f"with one entry per id (the same integer id), in the same order, plus a one-line note.\n\n"
        + json.dumps(rows, ensure_ascii=False, indent=1)
    )
    data, version = gemini_call(prompt, model, key, schema=SCHEMA)
    got = {int(n["id"]): n for n in data.get("names", []) if "id" in n}
    path = track_dir(tag) / "glossary.tsv"
    have = {s for s, _ in read_glossary(path)}
    lines = []
    if not path.exists():
        lines.append("# Track glossary — `Tibetan term<TAB>rendering`, auto-loaded by gm_translate.py.")
    lines.append(f"# Proper names pinned by gm_names.py --propose ({version}); one spelling each.")
    n = 0
    for i, (tibs, ident) in enumerate(NAMES, 1):
        r = got.get(i)
        if not r or not r["rendering"].strip():
            print(f"  !! no rendering for {ident}", file=sys.stderr)
            continue
        for t in tibs:
            if t in have:
                continue
            lines.append(f"{t}\t{r['rendering'].strip()}")
            n += 1
        print(f"  {ident[:34]:36} {r['rendering'].strip()}   ({r['note'][:60]})")
    with path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"appended {n} entries to {path.relative_to(VAULT)}")


def name_entries(tag):
    """Every glossary entry as [(tib, canonical)] — names, interjections, mantra
    syllables alike. A rendering may carry a parenthesised gloss for the model
    ("үлдэлгүйгээр (without exception)"); the pinned form is the part before it."""
    out = []
    for s, t in read_glossary(track_dir(tag) / "glossary.tsv"):
        canon = t.split(" (")[0].strip()
        if canon:
            out.append((s, canon))
    return out


def occurs(tib, text):
    """A glossary key counts only at a syllable boundary: `མར་པ` must not match
    inside `དམར་པོ` ("red"). The character before it may not be a Tibetan letter,
    vowel sign or subjoined letter; what follows is free (case endings attach)."""
    return re.search(r"(?<![\u0F40-\u0FBC])" + re.escape(tib), text) is not None


def check(tag, verbose=True):
    entries = name_entries(tag)
    if not entries:
        sys.exit("no name entries in the glossary yet — run --propose first")
    work = track_dir(tag) / "work"
    todo = {}
    n_hit = 0
    for led in sorted(work.glob(f"*-{tag}.jsonl")):
        latest = {}
        for line in led.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                latest[r["block_id"]] = r
        stem = led.name[: -(len(tag) + 7)]
        for bid, r in latest.items():
            missing = []
            for tib, canon in entries:
                if occurs(tib, r["source"]):
                    n_hit += 1
                    if canon not in r["translation"]:
                        missing.append((tib, canon))
            if missing:
                todo.setdefault(stem, []).append((bid, missing))
    n_blocks = sum(len(v) for v in todo.values())
    if verbose:
        for stem, items in todo.items():
            ids = ", ".join("^" + b for b, _ in items)
            print(f"  {stem[:40]:42} {len(items):3} block(s): {ids[:70]}")
        print(f"{n_blocks} block(s) in {len(todo)} text(s) lack a canonical name form "
              f"(of {n_hit} name occurrences)")
    return todo


def rerun(lang, tag, todo, limit):
    done = 0
    for stem, items in todo.items():
        src = VAULT / "1-SOURCES" / "Text" / f"{stem}.md"
        ids = [b for b, _ in items]
        if limit and done >= limit:
            break
        print(f"\n=== {stem}  ({len(ids)} block(s)) ===", flush=True)
        cmd = [sys.executable, str(GM), "--source", str(src.relative_to(VAULT)), "--lang", lang,
               "--lang-tag", tag, "--out", str(track_dir(tag).relative_to(VAULT)),
               "--force", "--only", ",".join(ids)]
        res = subprocess.run(cmd, cwd=VAULT, capture_output=True, text=True)
        tail = [l for l in res.stdout.splitlines() if l.startswith(("[", "calls", "note", "SUMMARY"))]
        print("  " + "\n  ".join(tail[-6:]))
        if res.returncode != 0:
            print(res.stderr[-600:], file=sys.stderr)
            break
        done += len(ids)
    r = subprocess.run([sys.executable, str(STAMP), "--ids", "--track-meta", "--titles",
                        "--track", str(track_dir(tag).relative_to(VAULT))],
                       cwd=VAULT, capture_output=True, text=True)
    print("\nstamp:", " | ".join(r.stdout.strip().splitlines()))
    print("\nafter re-run:")
    check(tag)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lang", required=True)
    ap.add_argument("--lang-tag", default=None)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--propose", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--rerun", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="re-run at most N blocks")
    args = ap.parse_args()
    lang = args.lang.strip().lower()
    tag = args.lang_tag or LANG_TAGS.get(lang) or re.sub(r"[^a-z]", "", lang)[:3]
    if not any([args.propose, args.check, args.rerun]):
        ap.error("choose --propose, --check or --rerun")
    key = os.environ.get(KEY_ENV, "")
    if (args.propose or args.rerun) and not key:
        sys.exit(f"{KEY_ENV} is not set")
    if args.propose:
        propose(lang, tag, args.model, key)
    if args.check:
        check(tag)
    if args.rerun:
        todo = check(tag)
        rerun(lang, tag, todo, args.limit)


if __name__ == "__main__":
    main()
