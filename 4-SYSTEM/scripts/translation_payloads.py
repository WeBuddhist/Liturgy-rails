#!/usr/bin/env python3
"""Build WeBuddhist v2 API payloads for a machine-baseline translation track.

Emits, per translation note in 3-TRANSFORMATIONS/Translations/<track>/<lang>/:

    <stem>-<lang>.text.json       ->  POST /v2/texts
    <stem>-<lang>.edition.json    ->  POST /v2/texts/{text_id}/editions
    <stem>-<lang>.alignment.json  ->  PUT  /v2/editions/{src}/alignments/{tgt}

This is the translation-side counterpart to `liturgy_payloads.py`, which does
the same job for the Tibetan root texts in `1-SOURCES/Text/`. Three things
differ, and each is a decision rather than a detail:

1. **The title is `title_translated`, not `title`.** A translation note's
   `title` carries the track suffix — "The Four Immeasurables — DharmaMitra
   zero-shot (english)" — which names the *file*, not the work. Uploading it
   would put the generator's name in the library's title field.

2. **`translation_of` is set, and it is set ONCE.** `TextPatch` has no
   `translation_of` field, so the link cannot be added later: a text created
   without it can only be fixed by deleting and re-creating it. The value is
   the Tibetan *text_id*, cross-checked against the upload ledger so a stale
   frontmatter id cannot silently point a translation at the wrong work.

3. **Alignment comes from block-ID parity, not from transclusions.** The
   vendored `parser.build_alignment` reads Obsidian `![[...#^N]]` links; these
   notes quote their source as `>` blockquotes instead, so it returns zero
   pairs. It is not used. Instead every block id is required to appear on both
   sides, and each one becomes a pair — which is exactly what the block-ID
   contract already guarantees (see 4-SYSTEM/CLAUDE.md §2). A mismatch is an
   abort, never a partial alignment: a half-aligned translation is worse than
   an unaligned one because nothing downstream can tell it is incomplete.

`contributions` is omitted entirely. The notes carry `author:` empty by design
(machine output has no author), and the v2 API treats `contributions` as
optional, so an omitted key is a text with no contributor — not an anonymous
one. The `ai` contribution type would be the honest alternative, but it
requires a backend id for the model and the API exposes no way to mint one.

Usage:
    translation_payloads.py --category-id <ID> --out-dir <dir> <note.md>...
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.dirname(os.path.dirname(HERE))
LEDGER = os.path.join(HERE, "upload_ledger.json")
SOURCE_DIR = os.path.join(VAULT, "1-SOURCES", "Text")

LICENSES = {
    "cc0", "public", "cc-by", "cc-by-sa", "cc-by-nd", "cc-by-nc",
    "cc-by-nc-sa", "cc-by-nc-nd", "copyrighted", "unknown",
}
EDITION_TYPES = {"diplomatic", "critical", "collated"}
# None of the three EditionType values really describes a machine baseline.
# "critical" is what the Tibetan sources upload as, so the pair stays
# consistent; override per-note with `edition_type:` in the frontmatter.
DEFAULT_EDITION_TYPE = "critical"


def load_upstream_parser():
    path = os.path.join(HERE, "parser-root-text", "parser.py")
    spec = importlib.util.spec_from_file_location("wb_parser", path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    spec.loader.exec_module(mod)
    return mod


def build_text(fm, category_id, ledger, stem):
    title = (fm.get("title_translated") or "").strip()
    if not title:
        raise ValueError("title_translated missing — refusing to upload the track-suffixed title")

    lang = (fm.get("lang_tag") or "").strip()
    if not lang:
        raise ValueError("lang_tag missing")

    root_text_id = (fm.get("translation_of_text_id") or "").strip()
    if not root_text_id:
        raise ValueError("translation_of_text_id missing — the root text is not uploaded yet")

    # The ledger is the record of what the server actually assigned. If the
    # note disagrees with it, the note has been hand-edited or reverted by a
    # dm_translate run, and uploading would link to whatever that stale id is.
    recorded = ledger.get(stem, {}).get("text_id")
    if recorded != root_text_id:
        raise ValueError(
            f"translation_of_text_id {root_text_id!r} != ledger {recorded!r} for {stem!r}"
        )

    out = {
        "title": {lang: title},
        "language": lang,
        "category_id": category_id,
        "translation_of": root_text_id,
    }

    lic = (fm.get("license") or "").strip()
    if lic:
        if lic not in LICENSES:
            raise ValueError(f"license {lic!r} not one of {sorted(LICENSES)}")
        out["license"] = lic

    return out


def build_pairs(P, source_path, target_segments):
    """One alignment pair per block id, or abort.

    Block `^N` in the translation renders block `^N` in the source. That is
    the whole alignment; there is no other bookkeeping. Requiring the two
    reference lists to be *equal* — not merely overlapping — is what makes a
    renumbered source a loud failure instead of a wrong alignment silently
    uploaded against the right ids.
    """
    import pathlib
    _, source_edition = P.build_edition(pathlib.Path(source_path), None)
    source_refs = [s["reference"] for s in source_edition["segmentation"]["segments"]]
    target_refs = [s["reference"] for s in target_segments]

    if source_refs != target_refs:
        only_src = sorted(set(source_refs) - set(target_refs))
        only_tgt = sorted(set(target_refs) - set(source_refs))
        raise ValueError(
            f"block ids diverge: {len(source_refs)} source vs {len(target_refs)} target"
            f"{f'; source-only {only_src[:6]}' if only_src else ''}"
            f"{f'; target-only {only_tgt[:6]}' if only_tgt else ''}"
        )

    return [{"source_segment_reference": r, "target_segment_reference": r}
            for r in source_refs]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="+", help="translation notes")
    ap.add_argument("--category-id", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ledger", default=LEDGER)
    args = ap.parse_args(argv)

    import pathlib
    P = load_upstream_parser()
    os.makedirs(args.out_dir, exist_ok=True)
    with open(args.ledger, encoding="utf-8") as fh:
        ledger = json.load(fh)

    # The v2 API enforces ONE title per language: a second POST with a title
    # already used in that language is rejected 422. Two texts in this corpus
    # were given the same generated title and the collision only surfaced
    # mid-upload, after 61 texts were live. Catch it here instead.
    seen_titles = {}

    ok = bad = 0
    for path in args.paths:
        name = os.path.splitext(os.path.basename(path))[0]      # <stem>-<lang>
        try:
            fm, _ = P._read_source(pathlib.Path(path))
            lang = (fm.get("lang_tag") or "").strip()
            if not name.endswith(f"-{lang}"):
                raise ValueError(f"filename {name!r} does not end in -{lang}")
            stem = name[: -(len(lang) + 1)]                     # the root-text stem

            if (fm.get("file_type") or "").strip() != "translation":
                raise ValueError(f"file_type is {fm.get('file_type')!r}, not 'translation'")

            text = build_text(fm, args.category_id, ledger, stem)
            key = (text["language"], list(text["title"].values())[0].strip())
            if key in seen_titles:
                raise ValueError(
                    f"title {key[1]!r} in language {key[0]!r} is already used by "
                    f"{seen_titles[key]!r} — the API allows only one text per "
                    f"title+language; give one of them a different title")
            seen_titles[key] = name

            _, edition = P.build_edition(pathlib.Path(path), None)
            segments = edition["segmentation"]["segments"]
            content = edition["content"]
            if not content.strip():
                raise ValueError("content is empty")

            # Upstream builds the spans; this proves they slice back. A span
            # that has drifted would upload a segmentation that silently
            # mis-renders every line after it.
            for seg in segments:
                for span in seg["lines"]:
                    if not 0 <= span["start"] <= span["end"] <= len(content):
                        raise ValueError(f"segment {seg['reference']} span out of range")

            etype = (fm.get("edition_type") or DEFAULT_EDITION_TYPE).strip()
            if etype not in EDITION_TYPES:
                raise ValueError(f"edition_type {etype!r} not one of {sorted(EDITION_TYPES)}")
            meta = {"type": etype}
            src = (fm.get("source") or "").strip()
            if src:
                meta["source"] = src
            edition["metadata"] = meta

            source_path = os.path.join(SOURCE_DIR, f"{stem}.md")
            pairs = build_pairs(P, source_path, segments)

            root_edition_id = (fm.get("translation_of_edition_id") or "").strip()
            recorded = ledger.get(stem, {}).get("edition_id")
            if recorded != root_edition_id:
                raise ValueError(
                    f"translation_of_edition_id {root_edition_id!r} != ledger {recorded!r}"
                )

            alignment = {
                "source_edition_id": root_edition_id,   # consumed by the uploader,
                "alignments": pairs,                    # stripped before the PUT body
            }

            for fname, payload in ((f"{name}.text.json", text),
                                   (f"{name}.edition.json", edition),
                                   (f"{name}.alignment.json", alignment)):
                with open(os.path.join(args.out_dir, fname), "w", encoding="utf-8") as fh:
                    json.dump(payload, fh, ensure_ascii=False, indent=2)
            ok += 1
            print(f"ok     {name}")
            print(f"         {len(content)} chars | {len(segments)} segments | "
                  f"{len(pairs)} alignment pairs | -> {text['translation_of']}")
        except Exception as exc:
            print(f"ABORT  {name}\n         {type(exc).__name__}: {exc}")
            bad += 1

    print(f"\n{ok} built into {args.out_dir}, {bad} aborted")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
