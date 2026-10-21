#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""format_liturgy_batch.py — batch-format OpenPecha liturgy texts into vault notes.

Reads the fetched texts (work_list.json + contents.json from the
webuddhist-library-data-pipeline fetch of category dJpr4gMF72E4UpCnJ84sh)
and writes, for each text:

    0-INBOX/<title>.md        raw instance content, verbatim (plus the
                               ornament spacing fix below — nothing else)
    1-SOURCES/Text/<title>.md  the prepared source note — metadata
                               frontmatter, the TOC headings, and the
                               segmentation (one blank-line-separated block
                               per segment). No block IDs.
    1-SOURCES/liturgy-catalog.json  the catalog (rank ↔ file ↔ backend ids)

With a ranking file as the 4th argument, only the top 100 recitations in it
are written (matched to the corpus by normalised title), in rank order.

Formatting rules (from webuddhist-library-data-pipeline
docs/reference/conventions.md and the tested Tibetan formatting of
bodhisattvacharyavatara-rails' bo notes):

- Unit split: the continuous text is split after every shad pair "། །",
  terma shad "༔", double shad "།།", and space+single-shad "␣།" (the
  post-ག orthography: a final ག takes one shad, so verse lines end "ག ।" —
  the same pattern the tested fix_midverse.py splits on). Each unit is one
  verse line or one prose sentence.
- Verse-counter removal: shad-sandwiched Tibetan numerals ("མ། ༡ །…" —
  per-stanza counters from the source edition) are removed, restoring the
  shad pair. Digits NOT between shads (dates, the ༧ honorific, recitation
  counts) are never touched.
- Verse detection: per text, the dominant syllable count d is computed over
  all units; units whose count is within ±1 of d are verse lines when d is
  a plausible metre (5–15 syllables). Runs of ≥ 4 consecutive verse lines
  form a verse region, grouped into 4-line stanzas (one line per output
  line, the stanza as one segment).
- Everything else is prose: each unit (one shad-pair-delimited sentence or
  mantra — the natural recitation segment in liturgy) becomes its own
  segment, so every recitation unit stays addressable.
- Segments are separated by a blank line and carry NO block IDs: the v2 API
  expresses segmentation as character spans, so the blank-line boundary is
  the segmentation. 4-SYSTEM/scripts/build_payloads.py turns it into spans.
- Cleaning applied to both outputs: null bytes stripped; the non-breaking
  tsheg ༌ (U+0F0C) replaced with ་ (U+0F0B); runs of whitespace collapsed.

Frontmatter follows webuddhist-library-data-pipeline
docs/reference/frontmatter-schema.md (root-text required keys). Values come
from the OpenPecha category listing metadata (text_meta_all.json): author
(contributions with role=author, "Name [bdrc:ID]" format), license
(Public Domain Mark → public), bdrc_work_id, date. Keys with no available
value are left empty. Backend ids (text_id / instance_id / category_id
values) are deliberately NOT written into notes — they live only in
1-SOURCES/liturgy-catalog.json.

Usage:
    python3 scripts/format_liturgy_batch.py <work_list.json> <contents.json> <text_meta_all.json>
Run from the vault root (Liturgy-rails/).
"""

import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

CATEGORY_ID = "dJpr4gMF72E4UpCnJ84sh"
SOURCE_NOTE = "OpenPecha production API (critical instance content)"

SPLIT_RE = re.compile(r"(?<=། །)|(?<=༔)|(?<=།།)(?!།| །)|(?<= །)(?=[^\s།])")
PUNCT_RE = re.compile(r"[།༔༄༅༈༎༏༐༑ ]+")
COUNTER_RE = re.compile(r"(?<=།)\s?[༠-༩]+\s?(?=།)")


def clean(text: str) -> str:
    text = text.replace("\x00", "").replace("༌", "་")
    text = COUNTER_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_title(t: str) -> str:
    t = re.sub(r"^[༄༅༈།༔\s]+", "", t)
    t = re.sub(r"[།༔\s]+$", "", t)
    return re.sub(r"\s+", " ", t).strip()


def filename_for(title: str, text_id: str, used: set) -> str:
    """Title as note name, truncated at a tsheg to <=120 bytes, deduped."""
    name = title
    while len(name.encode()) > 120:
        cut = name[: len(name) - 1]
        idx = cut.rfind("་")
        name = cut[:idx] if idx > 10 else cut
    name = name.rstrip("་ ")
    if name in used:
        name = f"{name} ({text_id[:6]})"
    used.add(name)
    return name


LETTER_RE = re.compile(r"[ཀ-ཬྐ-ྼ]")


def units_of(content: str):
    raw = [u.strip() for u in SPLIT_RE.split(content) if u.strip()]
    # merge punctuation-only fragments: opening ornaments (༄…) glue onto the
    # following unit; stray trailing shads glue onto the preceding unit —
    # otherwise they become meaningless standalone blocks
    merged, prefix = [], ""
    for u in raw:
        if not LETTER_RE.search(u):
            if merged and not u.startswith("༄"):
                merged[-1] = f"{merged[-1]} {u}"
            else:
                prefix += u + " "
            continue
        merged.append((prefix + u).strip())
        prefix = ""
    if prefix:
        if merged:
            merged[-1] = f"{merged[-1]} {prefix.strip()}"
        else:
            merged.append(prefix.strip())
    return merged


def syllables(unit: str) -> int:
    bare = PUNCT_RE.sub(" ", unit)
    return len([s for s in re.split(r"[་\s]+", bare) if s])


def dominant_count(counts):
    from collections import Counter
    plausible = [c for c in counts if 5 <= c <= 15]
    if not plausible:
        return None
    top, n = Counter(plausible).most_common(1)[0]
    # require the metre to actually dominate the text
    return top if n >= max(4, len(counts) * 0.4) else None


def blocks_of(content: str):
    """Return list of (kind, lines) blocks; kind in {'verse', 'prose'}."""
    units = units_of(content)
    counts = [syllables(u) for u in units]
    d = dominant_count(counts)
    is_verse = [d is not None and abs(c - d) <= 1 for c in counts]

    # runs of >=4 verse units count as verse regions; short runs become prose
    blocks, i = [], 0
    while i < len(units):
        if is_verse[i]:
            j = i
            while j < len(units) and is_verse[j]:
                j += 1
            run = units[i:j]
            if len(run) >= 4:
                for k in range(0, len(run), 4):
                    blocks.append(("verse", run[k:k + 4]))
            else:
                for u in run:
                    blocks.append(("prose", [u]))
            i = j
        else:
            j = i
            while j < len(units) and not is_verse[j]:
                j += 1
            for u in units[i:j]:
                blocks.append(("prose", [u]))
            i = j
    return blocks


def is_colophon(block) -> bool:
    text = " ".join(block[1])
    return "རྫོགས་ས" in text or text.startswith("ཞེས")


LICENSE_MAP = {
    "Public Domain Mark": "public", "CC0": "cc0", "CC BY": "cc-by",
    "CC BY-SA": "cc-by-sa", "CC BY-ND": "cc-by-nd", "CC BY-NC": "cc-by-nc",
    "CC BY-NC-SA": "cc-by-nc-sa", "CC BY-NC-ND": "cc-by-nc-nd",
    "under copyright": "copyrighted", "unknown": "unknown",
}


def author_string(tm: dict) -> str:
    parts = []
    for c in tm.get("contributions") or []:
        if c.get("role") != "author":
            continue
        names = c.get("person_name") or {}
        name = names.get("bo") or names.get("sa") or names.get("en") or ""
        if not name:
            continue
        if c.get("person_bdrc_id"):
            name = f"{name} [bdrc:{c['person_bdrc_id']}]"
        parts.append(name)
    return "; ".join(parts)


def format_note(title: str, content: str, meta: dict, tm: dict) -> str:
    """Note = metadata frontmatter + TOC heading + segmentation. No block IDs.

    Segmentation is carried by the blank-line boundaries alone: each blank-line
    -separated block is one segment (a 4-line stanza, or one prose/mantra
    unit), which is exactly what the parser turns into character spans. The
    single `## 1. <title>` heading is the TOC section.
    """
    blocks = blocks_of(content)

    out = []
    fm = {
        "title": title,
        "author": author_string(tm),
        "language": "Tibetan",
        "lang_tag": "bo",
        "file_type": "root-text",
        "edition_type": "critical",
        "category_id": "",
        "license": LICENSE_MAP.get(tm.get("license") or "", ""),
        "source": "https://api-aq25662yyq-uc.a.run.app",
        "bdrc_work_id": tm.get("bdrc") or "",
        # OpenPecha's `date` is the ingestion timestamp, NOT the composition
        # date the schema means — left empty rather than filled wrongly
        "date": "",
    }
    out.append("---")
    for k, v in fm.items():
        out.append(f"{k}: {v}".rstrip())
    out.append("---")
    out.append("")
    out.append(f"# ༄༅། །{title}།")
    out.append("")
    out.append(f"## 1. {title}།")
    out.append("")

    for kind, lines in blocks:
        out.extend(lines)
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def norm_title(t: str) -> str:
    """Normalise a title for cross-source matching (ranking file ↔ vault)."""
    t = re.sub(r"^[༄༅༈།༔\s]+", "", t or "")
    t = re.sub(r"[།༔\s་]+$", "", t)
    return re.sub(r"\s+", "", t)


def main():
    work_list, contents_path, meta_path = sys.argv[1], sys.argv[2], sys.argv[3]
    ranking_path = sys.argv[4] if len(sys.argv) > 4 else None
    work = json.load(open(work_list))
    contents = json.load(open(contents_path))
    all_meta = json.load(open(meta_path))

    # Optional ranking filter: keep only the top-N recitations, in rank order.
    if ranking_path:
        import difflib
        recs = json.load(open(ranking_path))["recitations"][:100]
        rank = {norm_title(r["title"]): i for i, r in enumerate(recs)}
        seg = {norm_title(r["title"]): re.sub(r"\s", "", r["first_segment"]["content"])
               for r in recs if r.get("first_segment")}

        # group candidates by rank; the corpus has a few same-title variants
        groups = {}
        for w in work:
            k = norm_title(w["title"])
            if k in rank:
                groups.setdefault(k, []).append(w)

        chosen = []
        for k, cands in groups.items():
            if len(cands) > 1 and k in seg:
                # pick the variant whose opening actually matches the ranking's
                # own first_segment — the version WeBuddhist recites
                def score(w):
                    body = re.sub(r"\s", "", clean(contents.get(w["text_id"], "")))
                    return difflib.SequenceMatcher(
                        None, seg[k], body[: len(seg[k]) + 40]).ratio()
                cands = sorted(cands, key=score, reverse=True)
                print(f"  variant tiebreak for {cands[0]['title'][:30]}: "
                      f"kept {cands[0]['text_id']}, dropped "
                      f"{', '.join(c['text_id'] for c in cands[1:])}")
            chosen.append(cands[0])

        work = sorted(chosen, key=lambda w: rank[norm_title(w["title"])])
        print(f"ranking filter: {len(work)}/{len(recs)} top recitations matched")

    root = Path(".")
    used = set()
    manifest = {"source": SOURCE_NOTE, "category_id": CATEGORY_ID,
                "fetched": date.today().isoformat(), "texts": []}
    stats = {"verse_blocks": 0, "prose_blocks": 0, "colophons": 0}

    for w in work:
        tid = w["text_id"]
        raw = contents.get(tid)
        if raw is None:
            continue
        title = clean_title(w["title"])
        name = filename_for(title, tid, used)
        cleaned = clean(raw)

        (root / "0-INBOX" / f"{name}.md").write_text(cleaned + "\n", encoding="utf-8")
        tm = all_meta.get(tid, {})
        note = format_note(title, cleaned, w, tm)
        (root / "1-SOURCES" / "Text" / f"{name}.md").write_text(note, encoding="utf-8")

        stats["verse_blocks"] += note.count("^1-") - note.count("^1-0") - sum(
            1 for c in "abcdefgh" if f"^1-{c}" in note)
        stats["colophons"] += sum(1 for c in "abcdefgh" if f"^1-{c}" in note)
        import re as _re
        has_stanzas = bool(_re.search(r"^[^\n]+། །$", note.split("^1-0", 1)[-1], _re.M))
        manifest["texts"].append({
            "rank": len(manifest["texts"]) + 1,
            "file": f"{name}.md", "title": title, "text_id": tid,
            "instance_id": w["instance_id"], "openpecha_type": w["text_type"],
            "layout": "verse" if has_stanzas else "prose",
            "author": author_string(tm),
            "license": LICENSE_MAP.get(tm.get("license") or "", ""),
            "bdrc": tm.get("bdrc") or "",
        })

    json.dump(manifest, open(root / "1-SOURCES" / "liturgy-catalog.json", "w"),
              ensure_ascii=False, indent=1)
    print(f"wrote {len(manifest['texts'])} source+text pairs")
    print(f"blocks: ~{stats['verse_blocks']} content, {stats['colophons']} colophon")


if __name__ == "__main__":
    main()
