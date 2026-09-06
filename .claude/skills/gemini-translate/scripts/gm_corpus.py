#!/usr/bin/env python3
"""gm_corpus.py — drive gm_translate.py across the liturgy corpus for ONE language.

One language per invocation, one track folder per language, so several
languages can run side by side in separate processes without sharing a file.
Per text it runs gm_translate.py (which already resumes from its ledger and
enforces line parity), collects that script's SUMMARY line, and at the end
re-stamps the track's frontmatter (backend ids, provenance, researched titles)
with stamp_metadata.py restricted to THIS track — the track-only passes are
what make parallel runs safe; the passes that write 1-SOURCES/ are left for
the main session.

Stops on a daily-quota or hard API failure and says so; a re-run resumes.

Usage:
    gm_corpus.py --lang hindi                       # all 94 texts, track Gemini/hi
    gm_corpus.py --lang nepali --only "ཚིག་བདུན"     # texts whose name contains this
    gm_corpus.py --lang mongolian --sources list.txt --limit 2
    gm_corpus.py --lang vietnamese --reference-track 3-TRANSFORMATIONS/Translations/Dharmamitra/en
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
GM = HERE / "gm_translate.py"
VAULT = HERE.parents[3]
STAMP = VAULT / "4-SYSTEM" / "scripts" / "stamp_metadata.py"
SOURCES = VAULT / "1-SOURCES" / "Text"
RETIRED = VAULT / "4-SYSTEM" / "retired-texts.txt"

sys.path.insert(0, str(HERE))
from gm_translate import DEFAULT_MODEL, DEFAULT_TRACK_ROOT, LANG_TAGS  # noqa: E402


def retired_stems():
    if not RETIRED.exists():
        return set()
    return {l.strip() for l in RETIRED.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lang", required=True, help="target language LABEL")
    ap.add_argument("--lang-tag", default=None)
    ap.add_argument("--out", default=None, help=f"track folder (default {DEFAULT_TRACK_ROOT}/<tag>)")
    ap.add_argument("--sources", default=None, help="file listing source .md paths (default: all)")
    ap.add_argument("--only", default=None, help="substring of source filename(s) to run")
    ap.add_argument("--limit", type=int, default=0, help="only the first N texts")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--thinking", default=None, choices=[None, "low", "medium", "high"])
    ap.add_argument("--batch", type=int, default=None)
    ap.add_argument("--context-blocks", type=int, default=None)
    ap.add_argument("--reference-track", default=None)
    ap.add_argument("--sleep", type=float, default=None)
    ap.add_argument("--force", action="store_true", help="re-translate everything")
    ap.add_argument("--no-stamp", action="store_true",
                    help="skip the stamp_metadata pass at the end (not recommended)")
    args = ap.parse_args()

    lang = args.lang.strip().lower()
    tag = args.lang_tag or LANG_TAGS.get(lang) or re.sub(r"[^a-z]", "", lang)[:3]
    out = pathlib.Path(args.out or f"{DEFAULT_TRACK_ROOT}/{tag}")

    if args.sources:
        srcs = [pathlib.Path(l.strip()) for l in
                open(args.sources, encoding="utf-8") if l.strip()]
    else:
        skip = retired_stems()
        srcs = [p for p in sorted(SOURCES.glob("*.md")) if p.stem not in skip]
    if args.only:
        srcs = [p for p in srcs if args.only in p.name]
        if not srcs:
            sys.exit(f"no source matched {args.only!r}")
    if args.limit:
        srcs = srcs[: args.limit]

    os.chdir(VAULT)
    results, stopped = [], None
    t_start = _dt.datetime.now()
    print(f"language {lang} ({tag})  model {args.model}  texts {len(srcs)}  track {out}")

    for i, src in enumerate(srcs, 1):
        cmd = [sys.executable, str(GM), "--source", str(src.relative_to(VAULT) if src.is_absolute() else src),
               "--lang", lang, "--lang-tag", tag, "--out", str(out), "--model", args.model]
        for flag, val in (("--thinking", args.thinking), ("--batch", args.batch),
                          ("--context-blocks", args.context_blocks),
                          ("--reference-track", args.reference_track), ("--sleep", args.sleep)):
            if val is not None:
                cmd += [flag, str(val)]
        if args.force:
            cmd.append("--force")
        res = subprocess.run(cmd, capture_output=True, text=True)
        summary = None
        for line in res.stdout.splitlines():
            if line.startswith("SUMMARY "):
                summary = json.loads(line[8:])
        if res.returncode != 0 or summary is None:
            print(f"[{i}/{len(srcs)}] FAIL     {src.name}\n{res.stderr[-800:]}", flush=True)
            results.append({"text": src.stem, "status": "fail", "stderr": res.stderr[-800:]})
            stopped = "fail"
            break
        results.append(summary)
        status = "ok"
        if summary["parity_failures"]:
            status = f"{len(summary['parity_failures'])} PARITY"
        if summary["failed"]:
            status = f"{len(summary['failed'])} FAILED"
        if summary["blocks_done"] < summary["blocks_total"]:
            status += " PARTIAL"
        print(f"[{i}/{len(srcs)}] {status:<12} {summary['blocks_done']}/{summary['blocks_total']} blocks, "
              f"{summary['calls']} calls  {src.name}", flush=True)
        for pf in summary["parity_failures"]:
            print(f"      ^{pf['id']}: source {pf['source']} lines -> output {pf['output']}", flush=True)
        if summary["stopped_at"]:
            stopped = summary["stopped_at"]
            print(f"STOPPED ({stopped}) at {src.name}; re-run the same command to resume.", flush=True)
            break

    if not args.no_stamp and STAMP.exists():
        r = subprocess.run([sys.executable, str(STAMP), "--ids", "--track-meta", "--titles",
                            "--track", str(out)], capture_output=True, text=True)
        print("\nstamp_metadata (track-only passes):")
        print("  " + "\n  ".join((r.stdout + r.stderr).strip().splitlines()[-8:]))

    done = [r for r in results if r.get("status") != "fail"]
    n_blocks = sum(r["blocks_done"] for r in done)
    n_total = sum(r["blocks_total"] for r in done)
    n_calls = sum(r["calls"] for r in done)
    parity = [(r["text"], pf) for r in done for pf in r["parity_failures"]]
    failed = [(r["text"], f) for r in done for f in r["failed"]]
    report = {
        "lang": lang, "lang_tag": tag, "track": str(out), "model": args.model,
        "thinking": args.thinking or "default", "reference_track": args.reference_track,
        "started": t_start.isoformat(timespec="seconds"),
        "finished": _dt.datetime.now().isoformat(timespec="seconds"),
        "texts_attempted": len(results), "texts_planned": len(srcs),
        "blocks_done": n_blocks, "blocks_total": n_total, "calls": n_calls,
        "parity_failures": [{"text": t, **pf} for t, pf in parity],
        "failed_blocks": [{"text": t, "id": f} for t, f in failed],
        "stopped": stopped, "texts": results,
    }
    (out / "work").mkdir(parents=True, exist_ok=True)
    rp = out / "work" / f"_corpus-run-{t_start.strftime('%Y%m%dT%H%M%S')}.json"
    rp.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\n=== {lang} ({tag}) ===")
    print(f"texts    : {len(results)}/{len(srcs)} attempted")
    print(f"blocks   : {n_blocks}/{n_total} in ledger, {n_calls} calls this run")
    print(f"parity   : {len(parity)} block(s) without line parity")
    for t, pf in parity:
        print(f"           {t}  ^{pf['id']}  {pf['source']} -> {pf['output']}")
    print(f"failed   : {len(failed)} block(s) with no usable response")
    if stopped:
        print(f"STOPPED  : {stopped} — this run is PARTIAL; re-run to resume")
    print(f"report   : {rp}")
    return 1 if stopped else 0


if __name__ == "__main__":
    sys.exit(main())
