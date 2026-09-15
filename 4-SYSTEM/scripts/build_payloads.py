#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_payloads.py — turn the ID-free vault notes into OpenPecha v2 payloads.

The notes in 1-SOURCES/Text/ carry exactly three things: metadata (frontmatter), the
TOC (markdown headings), and the segmentation (blank-line-separated blocks).
No block IDs — the v2 API expresses segmentation as character spans, so the
IDs would be redundant scaffolding.

This is the reason the repo's older `tools/parser/parser.py` cannot read these
notes: that parser derives spans from `^chapter-verse` block IDs, which this
format deliberately omits. Here the block boundaries ARE the segmentation.

For each note it writes, into payloads/<name>/:

  text.json      POST /v2/texts
                   {type, title{bo}, language, contributions[], copyright,
                    license, category_id, bdrc?, ...}
  instance.json  POST /v2/texts/{text_id}/instances
                   {metadata{type:critical, source, bdrc?}, content,
                    annotation: [{span:{start,end}}, ...]}
  toc.json       POST /v2/annotations/{instance_id}/annotation
                   {type: table_of_contents,
                    annotation: [{title, segments:[indices]}]}
                 Segment IDs are backend-assigned, so sections reference
                 segment INDICES here; the uploader swaps in the real ids
                 returned by the instance POST.

Spans are validated: every span slices back to exactly its source block.

Usage:
    python3 scripts/build_payloads.py [--category-id CAT] [note.md ...]
Run from the vault root. With no note paths, processes all of
1-SOURCES/Text/*.md; payloads land in 4-SYSTEM/scripts/output/.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
# v2 API ContributorRole enum — the API rejects anything else.
CONTRIBUTOR_ROLES = {"translator", "reviser", "author", "scholar"}

LICENSE_TO_COPYRIGHT = {
    "public": "Public domain", "cc0": "Public domain",
    "unknown": "Unknown", "copyrighted": "In copyright",
}
LICENSE_TO_API = {
    "public": "Public Domain Mark", "cc0": "CC0", "cc-by": "CC BY",
    "cc-by-sa": "CC BY-SA", "cc-by-nd": "CC BY-ND", "cc-by-nc": "CC BY-NC",
    "cc-by-nc-sa": "CC BY-NC-SA", "cc-by-nc-nd": "CC BY-NC-ND",
    "copyrighted": "under copyright", "unknown": "unknown",
}


def parse_frontmatter(text: str) -> dict:
    m = FM_RE.match(text)
    if not m:
        raise ValueError("no frontmatter")
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def parse_body(text: str):
    """Return (sections, blocks).

    sections: [{"title": str, "blocks": [block_index, ...]}] — one per `##`
    blocks:   ["block text", ...] in document order
    """
    body = FM_RE.sub("", text)
    sections, blocks = [], []
    current = None
    for chunk in re.split(r"\n\s*\n", body):
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("# "):          # document title — not a TOC section
            continue
        if chunk.startswith("## "):
            current = {"title": chunk[3:].strip(), "blocks": []}
            sections.append(current)
            continue
        blocks.append(chunk)
        if current is not None:
            current["blocks"].append(len(blocks) - 1)
    return sections, blocks


def build(note: Path, category_id: str = "") -> dict:
    text = note.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    sections, blocks = parse_body(text)

    # content + spans: blocks joined by a single newline, spans over that string
    content, spans, cursor = "", [], 0
    for i, b in enumerate(blocks):
        if i:
            content += "\n"
            cursor += 1
        content += b
        spans.append({"start": cursor, "end": cursor + len(b)})
        cursor += len(b)

    for span, b in zip(spans, blocks):        # spans must slice back exactly
        assert content[span["start"]:span["end"]] == b, f"span mismatch in {note}"

    lic = fm.get("license", "")
    # FORK(liturgy-rails): the v2 API's PersonContributionInput is
    #   {"type": "person", "id": <person_id>, "bdrc_id": <P-number>, "role": <ContributorRole>}
    # with `type` and `role` REQUIRED and role drawn from
    #   translator | reviser | author | scholar.
    # This used to emit {"role", "person_bdrc_id", "_name"} — no `type`, wrong
    # key for bdrc, and a `_name` the API does not accept — so every upload
    # silently landed with contributions: []. All 94 texts in the backend had
    # no author recorded as a result. Verified against the live records, not
    # inferred.
    #
    # The author field carries its ids and role inline, one contributor per `;`:
    #   author: གླང་རི་ཐང་པ། [person:u4IF1iXKCtryLY6Gtf4KZ] [bdrc:P3445] [role:author]
    # role defaults to "author" when the tag is absent.
    #
    # NOTE: upload_liturgy.py POSTs text.json VERBATIM — it does NOT strip
    # underscore-prefixed keys. So no `_name` (or any other local-only key) may
    # be emitted here; the API would receive it.
    contributions = []
    if fm.get("author"):
        for part in fm["author"].split(";"):
            part = part.strip()
            if not part:
                continue
            pid = re.search(r"\[person:([^\]]+)\]", part)
            bid = re.search(r"\[bdrc:([^\]]+)\]", part)
            rol = re.search(r"\[role:([^\]]+)\]", part)
            role = (rol.group(1).strip() if rol else "author")
            if role not in CONTRIBUTOR_ROLES:
                raise SystemExit(
                    f"{note}: role {role!r} is not one of {sorted(CONTRIBUTOR_ROLES)}")
            # The API rejects a person contribution carrying BOTH id and
            # bdrc_id ("Only one of id or bdrc_id can be provided"). Prefer the
            # backend person id; fall back to bdrc_id only when there is none.
            entry = {"type": "person", "role": role}
            if pid:
                entry["id"] = pid.group(1).strip()
            elif bid:
                entry["bdrc_id"] = bid.group(1).strip()
            contributions.append(entry)

    text_payload = {
        "type": "root",
        "title": {fm.get("lang_tag", "bo"): fm.get("title", "")},
        "language": fm.get("lang_tag", "bo"),
        "contributions": contributions,
        "copyright": LICENSE_TO_COPYRIGHT.get(lic, "Unknown"),
        "license": LICENSE_TO_API.get(lic, "unknown"),
        "category_id": category_id or fm.get("category_id", ""),
    }
    if fm.get("bdrc_work_id"):
        text_payload["bdrc"] = fm["bdrc_work_id"]
    if fm.get("date"):
        text_payload["date"] = fm["date"]

    instance_payload = {
        "metadata": {
            "type": fm.get("edition_type", "critical"),
            "source": fm.get("source", ""),
        },
        "content": content,
        "annotation": [{"span": s} for s in spans],
    }
    if fm.get("bdrc_work_id"):
        instance_payload["metadata"]["bdrc"] = fm["bdrc_work_id"]

    toc_payload = {
        "type": "table_of_contents",
        "annotation": [
            {"title": s["title"], "segment_indices": s["blocks"]}
            for s in sections if s["blocks"]
        ],
    }
    return {"text": text_payload, "instance": instance_payload,
            "toc": toc_payload, "_stats": {"blocks": len(blocks),
                                           "chars": len(content),
                                           "sections": len(toc_payload["annotation"])}}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("notes", nargs="*", help="note paths (default: all of 1-SOURCES/Text/)")
    ap.add_argument("--category-id", default="",
                    help="WeBuddhist/OpenPecha category id to stamp into text.json")
    ap.add_argument("--output-dir", default="4-SYSTEM/scripts/output")
    args = ap.parse_args()

    notes = [Path(p) for p in args.notes] or sorted(Path("1-SOURCES/Text").glob("*.md"))
    outroot = Path(args.output_dir)
    total_blocks = 0
    for note in notes:
        payloads = build(note, args.category_id)
        stats = payloads.pop("_stats")
        d = outroot / note.stem
        d.mkdir(parents=True, exist_ok=True)
        for name, payload in payloads.items():
            (d / f"{name}.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8")
        total_blocks += stats["blocks"]
    print(f"{len(notes)} notes -> {outroot}/  ({total_blocks} segments total)")


if __name__ == "__main__":
    main()
