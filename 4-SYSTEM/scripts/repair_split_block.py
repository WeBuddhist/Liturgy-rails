#!/usr/bin/env python3
"""Repair a translation ledger after a source block was SPLIT in two.

    python3 4-SYSTEM/scripts/repair_split_block.py <text-stem> <lang-tag> <block-id>

Why this exists: `རྟེན་འབྲེལ་བསྟོད་པ།` carried a stray `ˌ` (U+02CC) sitting where a
blank line belonged, which fused two four-line verses into a single block. When
the character was removed the block split in two and every later block shifted
up by one, leaving the English ledger — and so the rendered translation and the
segment alignment derived from it — numbered against a source that no longer
existed.

The block ids ARE the segment alignment (translation `^N` renders source `^N`),
so a stale ledger does not merely produce an out-of-date file; it would upload a
wrong alignment. Renumbering has to happen in the ledger, because that is what
the renderer reads.

No API call is made. The merged block's translation already contains both
stanzas separated by a blank line, so it is split on that boundary and the two
halves become the two new blocks. The script refuses to run unless the split it
is about to make actually reconstructs the source: `merged == first + second`,
compared with Tibetan punctuation and the stray character normalised away.
"""

import json
import os
import re
import shutil
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def norm(s):
    return re.sub(r"[༄༅།༈་\s༎༏༐༑༔ˌ]+", "", s or "")


def source_blocks(path):
    body = open(path).read().split("\n---\n", 1)[1]
    out = {}
    for b in re.split(r"\n\s*\n", body):
        b = b.strip()
        if not b or b.startswith("#"):
            continue
        m = re.search(r"\^(\S+)\s*$", b)
        if m:
            out[m.group(1)] = re.sub(r"\s*\^\S+\s*$", "", b)
    return out


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    stem, tag, split_at = sys.argv[1], sys.argv[2], sys.argv[3]

    src_path = os.path.join(VAULT, "1-SOURCES", "Text", f"{stem}.md")
    ledger_path = os.path.join(VAULT, "3-TRANSFORMATIONS", "Translations",
                               "Dharmamitra", tag, "work", f"{stem}-{tag}.jsonl")
    for p in (src_path, ledger_path):
        if not os.path.exists(p):
            print(f"missing: {p}", file=sys.stderr)
            return 1

    blocks = source_blocks(src_path)
    recs = [json.loads(l) for l in open(ledger_path) if l.strip()]

    a, b = split_at, str(int(split_at) + 1)
    if a not in blocks or b not in blocks:
        print(f"source has no blocks ^{a} and ^{b}", file=sys.stderr)
        return 1

    merged = next((r for r in recs if r["block_id"] == split_at), None)
    if merged is None:
        print(f"ledger has no block ^{split_at}", file=sys.stderr)
        return 1

    # The split must reconstruct the source, or we are guessing.
    if norm(merged["source"]) != norm(blocks[a] + blocks[b]):
        print("REFUSING: ledger block does not equal source ^%s + ^%s" % (a, b),
              file=sys.stderr)
        return 1
    stanzas = [s.strip() for s in re.split(r"\n\s*\n", merged["translation"]) if s.strip()]
    if len(stanzas) != 2:
        print(f"REFUSING: translation splits into {len(stanzas)} parts, need exactly 2",
              file=sys.stderr)
        return 1

    shutil.copy2(ledger_path, ledger_path + ".pre-split-repair")

    note = (f"split from merged block ^{split_at}; the source carried a stray "
            f"U+02CC where a blank line belonged, fusing two blocks. No new API call.")
    out = []
    for r in recs:
        bid = r["block_id"]
        if not bid.isdigit():
            out.append(r)
            continue
        n = int(bid)
        if n < int(split_at):
            out.append(r)
        elif n == int(split_at):
            for new_id, stanza, src in ((a, stanzas[0], blocks[a]), (b, stanzas[1], blocks[b])):
                c = dict(r)
                c["block_id"] = new_id
                c["source"] = src
                c["translation"] = stanza
                c["repair"] = note
                out.append(c)
        else:
            c = dict(r)
            c["block_id"] = str(n + 1)
            c["repair"] = f"renumbered +1 after the split of ^{split_at}"
            out.append(c)

    with open(ledger_path, "w") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    ids = {r["block_id"] for r in out}
    want = {k for k in blocks}
    print(f"ledger repaired: {len(recs)} -> {len(out)} records, {len(ids)} unique ids")
    print(f"  backup: {ledger_path}.pre-split-repair")
    missing = sorted(want - ids, key=lambda x: int(x) if x.isdigit() else 0)
    extra = sorted(ids - want, key=lambda x: int(x) if x.isdigit() else 0)
    print(f"  source blocks not in ledger: {missing or 'none'}")
    print(f"  ledger blocks not in source: {extra or 'none'}")
    print("\nNow re-render from the ledger (no API calls), then re-stamp:")
    print(f"  python3 .claude/skills/dharmamitra-translate/scripts/dm_translate.py \\")
    print(f"      --source '1-SOURCES/Text/{stem}.md' --lang-tag {tag} \\")
    print(f"      --out 3-TRANSFORMATIONS/Translations/Dharmamitra/{tag} --render-only")
    print("  python3 4-SYSTEM/scripts/stamp_metadata.py --all")
    return 0 if not missing and not extra else 1


if __name__ == "__main__":
    sys.exit(main())
