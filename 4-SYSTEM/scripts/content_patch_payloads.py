#!/usr/bin/env python3
"""Prepare `PATCH /v2/editions/{id}/content` payloads for the expert edits that
do NOT move a segment boundary — the texts the backend can take in place,
keeping every block id and therefore every translation alignment.

The repeated title line (the corpus-wide edit the experts will remove from
0-INBOX themselves) is dropped before comparing, per instruction: it is treated
as already gone.

What "the segment did not change" means here is checked, not assumed. For each
text:

  old   = 1-SOURCES/Text/<stem>.md  -> the exact content + segmentation that
          was POSTed to the backend (same code path as the uploader).
  new   = 0-INBOX/<file>.md, ids stripped, repeated title line dropped, then
          stamped and built the same way.

A text is *patchable* only if old and new have the same number of segments
with the same `reference`s, the same types and the same number of line spans.
Then the character difference is reduced to minimal insert/delete/replace
operations and the backend's OWN span arithmetic is replayed over the old
spans; the payload is emitted only if the replayed spans come out equal, char
for char, to the spans a fresh build of the new note produces. Anything that
fails that check is reported as a rebuild instead.

Ops are emitted in descending position order: each op's offsets are stated
against the content as it is on the backend now, and applying them highest
position first keeps every later offset valid without re-GETting between calls.

Read-only. Writes payload JSON and a report; never calls a mutating endpoint.

Usage (from the vault root):

    content_patch_payloads.py --out-dir 4-SYSTEM/scripts/payloads-content-patch
    content_patch_payloads.py --live          also GET each live edition's
                                              content and confirm the offsets
                                              are stated against what is there
    content_patch_payloads.py --only <stem>   one text, detail to stdout
"""

from __future__ import annotations

import argparse
import datetime
import difflib
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.dirname(os.path.dirname(HERE))
INBOX = os.path.join(VAULT, "0-INBOX")
SRC_DIR = os.path.join(VAULT, "1-SOURCES", "Text")
LEDGER = os.path.join(HERE, "upload_ledger.json")
BASE = "https://library.webuddhist.com"

sys.path.insert(0, HERE)
import block_ids as B            # noqa: E402
import inbox_diff as D           # noqa: E402
import liturgy_payloads as LP    # noqa: E402

# ---------------------------------------------------------------------------
# The backend's own span arithmetic, vendored verbatim so the simulation is the
# server's, not a re-reading of it.
#   ~/Desktop/work/webuddhist-library/openpecha-backend/database/span_database.py
#   commit cd1c205 (2026-09-04), lines 11-101.
# A Segment line span is a "continuous" span; a TOC section span is an
# "annotation" span.
# ---------------------------------------------------------------------------

def _adjust_continuous_for_insert(start, end, insert_pos, insert_len):
    if insert_pos == 0 and start == 0:
        return (start, end + insert_len)
    if insert_pos <= start:
        return (start + insert_len, end + insert_len)
    if insert_pos <= end:
        return (start, end + insert_len)
    return (start, end)


def _adjust_span_for_delete(start, end, del_start, del_end):
    del_len = del_end - del_start
    if del_end <= start:
        return (start - del_len, end - del_len)
    if del_start >= end:
        return (start, end)
    if del_start <= start and del_end >= end:
        return None
    if del_start <= start < del_end < end:
        return (del_start, end - del_len)
    if start < del_start < end <= del_end:
        return (start, del_start)
    if start < del_start and del_end < end:
        return (start, end - del_len)
    return (start, end)


def _adjust_continuous_for_replace(start, end, replace_start, replace_end,
                                   new_len, is_first_encompassed):
    delta = new_len - (replace_end - replace_start)
    if replace_start >= end:
        return (start, end)
    if replace_end <= start:
        return (start + delta, end + delta)
    if start == replace_start and end == replace_end:
        return (start, start + new_len)
    if replace_start <= start and replace_end >= end:
        if is_first_encompassed:
            return (replace_start, replace_start + new_len)
        return None
    if start < replace_start and replace_end < end:
        return (start, end + delta)
    if replace_start <= start < replace_end < end:
        return (replace_start + new_len, end + delta)
    if start < replace_start < end <= replace_end:
        return (start, replace_start + new_len)
    return (start, end)


def apply_op_to_spans(spans, op):
    """Replay one operation over a list of (start, end), in the backend's order
    (spans are fetched ORDER BY span_start, so `is_first_encompassed` goes to
    the lowest-start encompassed span). Returns None entries for spans the
    backend would delete."""
    out = []
    if op["type"] == "insert":
        for s in spans:
            out.append(None if s is None else
                       _adjust_continuous_for_insert(s[0], s[1], op["position"], len(op["text"])))
    elif op["type"] == "delete":
        for s in spans:
            out.append(None if s is None else
                       _adjust_span_for_delete(s[0], s[1], op["start"], op["end"]))
    else:
        first_found = False
        order = sorted((i for i, s in enumerate(spans) if s is not None),
                       key=lambda i: (spans[i][0], spans[i][1]))
        res = {}
        for i in order:
            s = spans[i]
            encompassed = op["start"] <= s[0] and op["end"] >= s[1]
            is_first = encompassed and not first_found
            if is_first:
                first_found = True
            res[i] = _adjust_continuous_for_replace(
                s[0], s[1], op["start"], op["end"], len(op["text"]), is_first)
        out = [res.get(i) if spans[i] is not None else None for i in range(len(spans))]
    return out


def apply_op_to_text(text, op):
    if op["type"] == "insert":
        return text[:op["position"]] + op["text"] + text[op["position"]:]
    if op["type"] == "delete":
        return text[:op["start"]] + text[op["end"]:]
    return text[:op["start"]] + op["text"] + text[op["end"]:]


# ---------------------------------------------------------------------------
# building the two editions
# ---------------------------------------------------------------------------

_PARSER = None


def parser():
    global _PARSER
    if _PARSER is None:
        _PARSER = LP.load_upstream_parser()
    return _PARSER


def build_edition(md_text, name_hint):
    """Run the uploader's own payload path over a note held in memory."""
    import pathlib
    import tempfile
    P = parser()
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / (name_hint + ".md")
        p.write_text(md_text, encoding="utf-8")
        fm, _ = P._read_source(p)
        _, edition = P.build_edition(p, None)
        LP.retype_segments(edition)
    return fm, edition


def seg_shape(edition):
    return [(s["reference"], s["type"], len(s["lines"]))
            for s in edition["segmentation"]["segments"]]


def flat_spans(edition):
    """Every line span, in segment order — the order the uploader POSTed and
    the order the backend stores."""
    out = []
    for si, s in enumerate(edition["segmentation"]["segments"]):
        for li, l in enumerate(s["lines"]):
            out.append((l["start"], l["end"]))
    return out


def span_labels(edition):
    out = []
    for s in edition["segmentation"]["segments"]:
        for li in range(len(s["lines"])):
            out.append(f'^{s["reference"]}[{li}]')
    return out


# ---------------------------------------------------------------------------
# minimal operations
# ---------------------------------------------------------------------------

def make_ops(old, new):
    """Minimal insert/delete/replace ops taking `old` to `new`, positions stated
    against `old`, returned highest-position-first so they can be sent in order
    without re-reading the content between calls."""
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    ops = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert":
            ops.append({"type": "insert", "position": i1, "text": new[j1:j2]})
        elif tag == "delete":
            ops.append({"type": "delete", "start": i1, "end": i2})
        else:
            ops.append({"type": "replace", "start": i1, "end": i2, "text": new[j1:j2]})
    ops.reverse()
    return ops


def op_pos(op):
    return op["position"] if op["type"] == "insert" else op["start"]


# ---------------------------------------------------------------------------

def ctx(s, a, b, pad=12):
    return (("…" if a - pad > 0 else "") + s[max(0, a - pad):a] + "«" + s[a:b] + "»"
            + s[b:b + pad] + ("…" if b + pad < len(s) else "")).replace("\n", "⏎")


def analyse(stem, src_path, in_path, ledger):
    r = {"stem": stem, "inbox": os.path.basename(in_path)}
    ids = ledger.get(stem) or {}
    r["text_id"] = ids.get("text_id")
    r["edition_id"] = ids.get("edition_id")

    src_raw = D.read(src_path)
    in_raw = D.read(in_path)

    fm_old, ed_old = build_edition(src_raw, stem)

    # inbox: strip any stray ids, drop the repeated title line, stamp.
    # split_frontmatter returns the frontmatter verbatim, fences included.
    stripped = B.strip_text(in_raw, in_path)
    fm_text, body = B.split_frontmatter(stripped, in_path)
    body = D.drop_title_line(body)
    rebuilt = fm_text + body
    try:
        stamped = B.stamp_text(rebuilt, in_path, restamp=True)
    except B.Abort as exc:
        r["verdict"] = "blocked"
        r["reason"] = f"{exc}"
        return r
    try:
        fm_new, ed_new = build_edition(stamped, stem)
    except Exception as exc:                                  # noqa: BLE001
        r["verdict"] = "blocked"
        r["reason"] = f"{type(exc).__name__}: {exc}"
        return r

    old_c, new_c = ed_old["content"], ed_new["content"]
    r["old_len"], r["new_len"] = len(old_c), len(new_c)
    r["segments_old"], r["segments_new"] = len(seg_shape(ed_old)), len(seg_shape(ed_new))

    if old_c == new_c:
        r["verdict"] = "unchanged"
        r["ops"] = []
        return r

    if seg_shape(ed_old) != seg_shape(ed_new):
        r["verdict"] = "rebuild"
        a, b = seg_shape(ed_old), seg_shape(ed_new)
        if len(a) != len(b):
            r["reason"] = f"segment count {len(a)} -> {len(b)}"
        else:
            d = [f"^{x[0]}({x[1]},{x[2]}ln) -> ^{y[0]}({y[1]},{y[2]}ln)"
                 for x, y in zip(a, b) if x != y]
            r["reason"] = "segments differ: " + "; ".join(d[:4]) + (" …" if len(d) > 4 else "")
        return r

    ops = make_ops(old_c, new_c)
    r["ops"] = ops

    # replay the backend's arithmetic
    spans = flat_spans(ed_old)
    text = old_c
    for op in ops:
        spans = apply_op_to_spans(spans, op)
        text = apply_op_to_text(text, op)

    r["content_ok"] = (text == new_c)
    want = flat_spans(ed_new)
    got = spans
    r["spans_ok"] = (got == want)
    if not r["spans_ok"]:
        labels = span_labels(ed_old)
        bad = [f"{labels[i]}: replay {got[i]} vs fresh {want[i]}"
               for i in range(min(len(got), len(want))) if got[i] != want[i]]
        r["span_mismatch"] = bad[:6]

    r["verdict"] = "patch" if (r["content_ok"] and r["spans_ok"]) else "rebuild"
    if r["verdict"] == "rebuild" and "reason" not in r:
        r["reason"] = ("replayed spans do not match a fresh build"
                       if not r["spans_ok"] else "replayed content does not match")

    # which segment each op falls in, and a readable context
    segs = []
    for s in ed_old["segmentation"]["segments"]:
        for l in s["lines"]:
            segs.append((l["start"], l["end"], s["reference"], s["type"]))
    detail = []
    for op in ops:
        a = op_pos(op)
        b = op["end"] if op["type"] != "insert" else a
        owner = None
        for st, en, ref, ty in segs:
            if st <= a <= en and (op["type"] == "insert" or b <= en):
                owner = (ref, ty)
                break
        detail.append({
            "op": op["type"],
            "at": a,
            "segment": f'^{owner[0]}' if owner else "?",
            "segment_type": owner[1] if owner else "?",
            "was": old_c[a:b],
            "now": op.get("text", ""),
            "context": ctx(old_c, a, b),
        })
    r["detail"] = detail

    # metadata side
    fm_src = D.read_fm(B.split_frontmatter(src_raw, src_path)[0] or "")
    fm_in = D.read_fm(B.split_frontmatter(in_raw, in_path)[0] or "")
    meta = D.compare_metadata(fm_src, fm_in)
    r["metadata"] = meta
    return r


def api_get(path):
    req = urllib.request.Request(BASE + path, headers={"Accept": "application/json"})
    key = os.environ.get("WEBUDDHIST_API_KEY", "")
    if key:
        req.add_header("X-API-Key", key)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def live_segments(edition_id):
    """Every segment of the live segmentation, in order (the endpoint pages at
    500)."""
    out, offset = [], 0
    while True:
        page = api_get(f"/v2/editions/{edition_id}/segmentation/segments"
                       f"?limit=500&offset={offset}")
        items = page["items"] if isinstance(page, dict) else page
        out.extend(items)
        if len(items) < 500:
            return out
        offset += 500


def live_check(r, ed_old):
    """Confirm the backend is in the state the offsets are stated against:
    same content string, same segment shape, same line spans."""
    live = api_get(f'/v2/editions/{r["edition_id"]}/content')
    r["live_len"] = len(live)
    r["live_content_matches"] = (live == ed_old["content"])

    segs = live_segments(r["edition_id"])
    r["live_shape_matches"] = (
        [(s.get("reference"), s.get("type"), len(s.get("lines", []))) for s in segs]
        == seg_shape(ed_old))
    r["live_spans_matches"] = (
        [(l["start"], l["end"]) for s in segs for l in s["lines"]] == flat_spans(ed_old))

    al = api_get(f'/v2/editions/{r["edition_id"]}/alignments')
    items = al["items"] if isinstance(al, dict) and "items" in al else al
    r["alignments"] = len(items)

    if not (r["live_content_matches"] and r["live_shape_matches"] and r["live_spans_matches"]):
        bad = [k for k in ("content", "shape", "spans") if not r[f"live_{k}_matches"]]
        r["verdict"] = "blocked"
        r["reason"] = ("live edition does not match the source note the offsets are "
                       f"computed against ({', '.join(bad)} differ)")


def md_report(results, out_dir, live):
    L = []
    w = L.append
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tally = {}
    for r in results:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    pat = [r for r in results if r["verdict"] == "patch"]
    ops = sum(len(r["ops"]) for r in pat)
    al = sum(r.get("alignments") or 0 for r in pat)

    w("# In-place content patches — texts whose segments did not move\n")
    w(f"Generated {now} by `4-SYSTEM/scripts/content_patch_payloads.py`"
      f"{' with `--live`' if live else ''}. Generated file — re-run the script "
      "rather than editing it.\n")
    w("The repeated title line is treated as already removed from 0-INBOX, per "
      "instruction: it is dropped from the inbox note before anything is compared. "
      "Nothing here has been sent to the backend.\n")

    w("## Summary\n")
    w("| verdict | texts | meaning |")
    w("|---|---|---|")
    w(f'| patch | {tally.get("patch", 0)} | segments identical; the character edits go in '
      "as `PATCH /v2/editions/{id}/content`, every block id and alignment survives |")
    w(f'| unchanged | {tally.get("unchanged", 0)} | content is byte-identical; no call at all |')
    w(f'| rebuild | {tally.get("rebuild", 0)} | a segment boundary or id moved; not patchable, '
      "needs delete + re-POST segmentation |")
    w(f'| blocked | {tally.get("blocked", 0)} | the note cannot be stamped as it stands |')
    w(f'| **total** | **{len(results)}** | |\n')
    w(f"**{ops} operations across {len(pat)} texts**, preserving {al} translation "
      "alignments. Payloads in `" + os.path.relpath(out_dir, VAULT) + "/`.\n")

    w("## How each payload was proved safe\n")
    w("For every text the old edition is rebuilt from `1-SOURCES/Text/` through the "
      "uploader's own payload path, and the new one from the inbox note with ids "
      "stripped, the repeated title line dropped, then re-stamped. A text qualifies "
      "only if both have the same segments — same `reference`, same type, same number "
      "of line spans. The character difference is then reduced to minimal operations "
      "and the backend's **own** span arithmetic (`adjust_spans_for_*` in "
      "`database/span_database.py`, vendored verbatim) is replayed over the old "
      "spans. The payload is written only if the replayed spans come out equal, "
      "position for position, to the spans a fresh stamp of the new note produces.\n")
    if live:
        w("With `--live`, each edition is also read back before being trusted: its "
          "content string, its segment shape and all its line spans must equal the "
          "local old side, so the offsets are stated against what is actually "
          "there.\n")

    w("## The patchable texts\n")
    w("| # | text | edition | chars | segments | ops | alignments kept | live checks |")
    w("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(pat, 1):
        checks = "—"
        if live:
            good = all(r.get(k) for k in ("live_content_matches", "live_shape_matches",
                                          "live_spans_matches"))
            checks = "content+shape+spans ✓" if good else "FAILED"
        w(f'| {i} | {r["stem"]} | `{r["edition_id"]}` | {r["old_len"]} → {r["new_len"]} '
          f'| {r["segments_old"]} | {len(r["ops"])} | {r.get("alignments", "—")} | {checks} |')
    w("")

    w("## Every operation\n")
    w("`«…»` is the range the operation covers in the content as it stands now. "
      "Send them per text in the order listed — descending by position, so no "
      "offset is invalidated by an earlier call.\n")
    for r in pat:
        w(f'### {r["stem"]}\n')
        w(f'`PATCH /v2/editions/{r["edition_id"]}/content` × {len(r["ops"])} · '
          f'{r["old_len"]} → {r["new_len"]} chars · {r.get("alignments", "?")} alignments kept\n')
        w("| # | op | body | in | was → now | context |")
        w("|---|---|---|---|---|---|")
        for n, (od, op) in enumerate(zip(r["detail"], r["ops"]), 1):
            if op["type"] == "insert":
                body = f'`position` {op["position"]}'
                change = f'→ `{op["text"]}`'
            elif op["type"] == "delete":
                body = f'`start` {op["start"]} `end` {op["end"]}'
                change = f'`{od["was"]}` →'
            else:
                body = f'`start` {op["start"]} `end` {op["end"]}'
                change = f'`{od["was"]}` → `{op["text"]}`'
            w(f'| {n} | {op["type"]} | {body} | `^{od["segment"][1:]}` ({od["segment_type"]}) '
              f'| {change} | `{od["context"]}` |')
        w("")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out-dir", default=os.path.join(HERE, "payloads-content-patch"))
    ap.add_argument("--only")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--report")
    ap.add_argument("--json")
    args = ap.parse_args(argv)

    ledger = json.load(open(LEDGER, encoding="utf-8")) if os.path.exists(LEDGER) else {}
    sources = {f[:-3]: f for f in os.listdir(SRC_DIR) if f.endswith(".md")}
    inbox = {}
    for f in sorted(os.listdir(INBOX)):
        if f.endswith(".md"):
            inbox.setdefault(D.norm(f[:-3]), []).append(f)

    results = []
    for stem in sorted(sources):
        if args.only and stem != args.only:
            continue
        cands = inbox.get(D.norm(stem), [])
        if not cands:
            continue
        results.append(analyse(stem, os.path.join(SRC_DIR, sources[stem]),
                               os.path.join(INBOX, cands[0]), ledger))

    if args.live:
        for r in results:
            if r["verdict"] != "patch" or not r.get("edition_id"):
                continue
            _, ed_old = build_edition(D.read(os.path.join(SRC_DIR, sources[r["stem"]])),
                                      r["stem"])
            try:
                live_check(r, ed_old)
            except Exception as exc:                            # noqa: BLE001
                r["verdict"] = "blocked"
                r["reason"] = f"live check failed: {type(exc).__name__}: {exc}"

    os.makedirs(args.out_dir, exist_ok=True)
    written = []
    for r in results:
        if r["verdict"] != "patch":
            continue
        payload = {
            "stem": r["stem"],
            "text_id": r["text_id"],
            "edition_id": r["edition_id"],
            "endpoint": f'PATCH /v2/editions/{r["edition_id"]}/content',
            "body": "the operation object itself; ContentOperation is a RootModel",
            "note": ("one request per operation, sent in this order. Offsets are "
                     "stated against the content as it is on the backend now; the "
                     "order is descending by position so no offset is invalidated "
                     "by an earlier op and no re-GET is needed between calls."),
            "expected_content_length_before": r["old_len"],
            "expected_content_length_after": r["new_len"],
            "segments": r["segments_old"],
            "segments_unchanged": True,
            "alignments_preserved": r.get("alignments"),
            "verified": {
                "replayed_content_equals_fresh_build": r["content_ok"],
                "replayed_spans_equal_fresh_build": r["spans_ok"],
                "live_content_matches": r.get("live_content_matches"),
                "live_segment_shape_matches": r.get("live_shape_matches"),
                "live_line_spans_match": r.get("live_spans_matches"),
            },
            "operations": r["ops"],
        }
        path = os.path.join(args.out_dir, f'{r["stem"]}.content-patch.json')
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        written.append(path)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
                       "results": results}, fh, ensure_ascii=False, indent=1)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(md_report(results, args.out_dir, args.live))

    tally = {}
    for r in results:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print(f'{len(results)} texts compared (repeated title line dropped)')
    for k in ("unchanged", "patch", "rebuild", "blocked"):
        if k in tally:
            print(f'  {k:10} {tally[k]}')
    print(f'{len(written)} payload(s) in {args.out_dir}')

    if args.only:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
