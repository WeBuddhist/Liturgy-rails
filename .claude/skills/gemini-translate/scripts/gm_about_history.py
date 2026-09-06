"""gm_about_history.py — (re)write the Run-history table in a Gemini track's about.md from its own files (report, ledgers, glossary). Usage: gm_about_history.py <tag> [extra note]. Idempotent: replaces an existing section. Run from the vault root."""
import sys, json, glob, re, pathlib, datetime
tag = sys.argv[1]; extra = sys.argv[2] if len(sys.argv) > 2 else ""
track = pathlib.Path(f"3-TRANSFORMATIONS/Translations/Gemini/{tag}")
about = track / "about.md"; s = about.read_text()
if "## Run history" in s:
    s = s[: s.index("\n## Run history")].rstrip("\n") + "\n"
reps = sorted(glob.glob(str(track / "work/_corpus-run-*.json")))
rep = json.load(open(reps[-1]))
# names residue from the log
sys.path.insert(0, ".claude/skills/gemini-translate/scripts")
import gm_names as g
todo = g.check(tag, verbose=False)
n_res = sum(len(v) for v in todo.values())
n_occ = 0
for led in (track / "work").glob(f"*-{tag}.jsonl"):
    latest = {}
    for line in led.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line); latest[r["block_id"]] = r
    for r in latest.values():
        n_occ += sum(1 for tib, _ in g.name_entries(tag) if g.occurs(tib, r["source"]))
gl = [l for l in (track / "glossary.tsv").read_text().splitlines() if l.strip() and not l.startswith("#")]
sec = f"""
## Run history

| Date | Step | Result |
| --- | --- | --- |
| 2026-09-06 | Pilot: `བློ་སྦྱོང་ཚིག་བརྒྱད་མ།`, `སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ།` | 39/39 blocks, line parity clean; reviewed block by block in `pilot-review.md` (READY FOR FULL RUN, `style.md` unchanged) |
| 2026-09-06 | Full corpus, `gm_corpus.py --lang` (model `{rep['model']}`, thinking {rep['thinking']}) | {rep['texts_attempted']}/{rep['texts_planned']} texts, {rep['blocks_done']}/{rep['blocks_total']} blocks, {rep['calls']} calls in the final resumed run, {len(rep['parity_failures'])} line-parity failures, {len(rep['failed_blocks'])} failed blocks |
| 2026-09-06 | Spot-read of three unseen texts (`corpus-run-review.md`) | content sound; one systematic defect: recurring proper names spelled inconsistently across blocks |
| 2026-09-06 | Names pinned (`gm_names.py --propose`; {len(gl)} glossary entries) and drifting blocks re-run (`--rerun`, two passes) | {n_res} block(s) of {n_occ} name occurrences still lack the pinned form after the boundary-aware check — epithets or longer names containing the key, listed by `gm_names.py --check` |
| 2026-09-06 | Ornament re-run (output contract now forbids copying ༈ ། ༔) and `gm_verify.py` | OK: every file whole, block ids identical to the Tibetan, no stray script{(' — ' + extra) if extra else ''} |

Every re-run is an appended ledger record produced by the same model under the
same `style.md`, with the glossary hits in context; nothing was hand-edited.
"""
about.write_text(s.rstrip("\n") + "\n" + sec)
print(tag, "run history appended")
