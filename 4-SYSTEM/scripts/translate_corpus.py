#!/usr/bin/env python3
"""Drive dharmamitra-translate across the liturgy corpus, enforcing line parity.

The API honours the "one line out per line in" style instruction most of the
time but not always — a four-line quatrain occasionally comes back as three
lines, which breaks the whole point of a block-ID-aligned translation. That
failure is recoverable: re-calling the same block reliably fixes it. So this
driver translates a text, checks every block's line count against its source,
re-runs the ones that diverged, and reports anything still divergent rather
than letting it pass silently.

Per language it produces one track folder holding one .md per source text,
each block-ID aligned to the Tibetan, plus a per-text ledger.

Usage:
    translate_corpus.py --lang english --lang-tag en \
        --out 3-TRANSFORMATIONS/Translations/Dharmamitra/en \
        --sources <file listing source paths> [--retries 3] [--limit N]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DM = os.path.join(os.path.dirname(HERE), "..", ".claude", "skills",
                  "dharmamitra-translate", "scripts", "dm_translate.py")
DM = os.path.normpath(os.path.join(HERE, "..", "..", ".claude", "skills",
                                   "dharmamitra-translate", "scripts",
                                   "dm_translate.py"))
SAFE = re.compile(r'[/\\:*?"<>|]')


def ledger_path(out_dir, src, tag):
    stem = SAFE.sub("", os.path.splitext(os.path.basename(src))[0]).strip() or "text"
    return os.path.join(out_dir, "work", f"{stem}-{tag}.jsonl")


def read_ledger(path):
    """Last record wins — the ledger is append-only, so a retry appends."""
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                out[r["block_id"]] = r
    return out


def mismatches(recs):
    bad = []
    for bid, r in recs.items():
        s = len([l for l in r["source"].split("\n") if l.strip()])
        t = len([l for l in r["translation"].split("\n") if l.strip()])
        if s != t:
            bad.append((bid, s, t))
    return sorted(bad, key=lambda x: [int(p) for p in x[0].split("-")])


def normalise_single_line(lp, recs):
    """Join a multi-line translation back to one line when its source is one line.

    A 400-character prose or mantra block is one line in the source; the API
    breaks it across several. Unlike a verse mismatch this is not a judgement
    call — there is exactly one correct answer, so fix it deterministically
    rather than burning retries on it. Appended, never edited in place: the
    ledger is append-only and render takes last-wins.
    """
    fixed = []
    for bid, r in recs.items():
        s = [l for l in r["source"].split("\n") if l.strip()]
        t = [l for l in r["translation"].split("\n") if l.strip()]
        if len(s) == 1 and len(t) > 1:
            new = dict(r)
            new["translation"] = " ".join(x.strip() for x in t)
            new["line_normalised"] = f"joined {len(t)} lines -> 1 (source is 1 line)"
            fixed.append(new)
    if fixed:
        with open(lp, "a", encoding="utf-8") as fh:
            for r in fixed:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(fixed)


def run(src, args, only=None, force=False):
    cmd = [sys.executable, DM, "--source", src, "--lang", args.lang,
           "--lang-tag", args.lang_tag, "--out", args.out,
           "--sleep", str(args.sleep), "--batch", str(args.batch)]
    if only:
        cmd += ["--only", ",".join(only)]
    if force:
        cmd.append("--force")
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lang", required=True, help="target language LABEL")
    ap.add_argument("--lang-tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sources", required=True, help="file listing source .md paths")
    ap.add_argument("--retries", type=int, default=3,
                    help="re-calls allowed per line-count mismatch")
    ap.add_argument("--sleep", type=float, default=4.0,
                    help="do not lower below 4 — the endpoint is public and shared")
    ap.add_argument("--batch", type=int, default=3,
                    help="blocks per API call, passed to dm_translate; 5 is "
                         "DharmaMitra's ceiling and is what makes a full-corpus "
                         "run fit the 400-calls/day quota")
    ap.add_argument("--limit", type=int, default=0, help="only the first N texts")
    args = ap.parse_args()

    with open(args.sources, encoding="utf-8") as fh:
        sources = [l.strip() for l in fh if l.strip()]
    if args.limit:
        sources = sources[:args.limit]

    unresolved = {}
    quota_stop = None
    for i, src in enumerate(sources, 1):
        name = os.path.basename(src)
        res = run(src, args)
        if res.returncode != 0:
            print(f"[{i}/{len(sources)}] FAIL {name}\n{res.stderr[-600:]}", flush=True)
            continue

        # dm_translate exits 0 after a daily-quota stop, having written a file
        # with nothing new in it. Without this check the driver reports every
        # remaining text as "ok  0 blocks" -- a spent quota looks like success,
        # and the loop keeps calling an endpoint that has already said no.
        if "daily quota spent" in res.stdout:
            print(f"[{i}/{len(sources)}] QUOTA EXHAUSTED at {name} -- "
                  f"stopping; {i - 1} text(s) attempted. Resume tomorrow with "
                  f"the same command (finished blocks are skipped).", flush=True)
            quota_stop = src
            break

        lp = ledger_path(args.out, src, args.lang_tag)
        recs = read_ledger(lp)
        bad = mismatches(recs)

        for attempt in range(args.retries):
            if not bad:
                break
            run(src, args, only=[b[0] for b in bad], force=True)
            recs = read_ledger(lp)
            bad = mismatches(recs)

        n_norm = normalise_single_line(lp, recs)
        if n_norm:
            recs = read_ledger(lp)
            bad = mismatches(recs)
            # re-render so the .md reflects the normalised ledger
            subprocess.run([sys.executable, DM, "--source", src, "--lang", args.lang,
                            "--lang-tag", args.lang_tag, "--out", args.out,
                            "--render-only"], capture_output=True, text=True)

        if not recs:
            status = "NO BLOCKS"
        else:
            status = "ok" if not bad else f"{len(bad)} UNRESOLVED"
        if n_norm:
            status += f" (+{n_norm} joined)"
        print(f"[{i}/{len(sources)}] {status:<16} {len(recs)} blocks  {name}", flush=True)
        if bad:
            unresolved[name] = bad
            for bid, s, t in bad:
                print(f"      ^{bid}: source {s} lines -> translation {t}", flush=True)

    if quota_stop:
        print(f"\nSTOPPED EARLY: daily quota exhausted at {os.path.basename(quota_stop)}. "
              f"This run is PARTIAL -- re-run tomorrow to finish.")
    print(f"\n{len(sources)} texts, {len(unresolved)} with unresolved line mismatches")
    for name, bad in unresolved.items():
        print(f"  {name}: {', '.join('^'+b[0] for b in bad)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
