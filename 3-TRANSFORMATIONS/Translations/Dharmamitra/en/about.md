---
title: "བློ་སྦྱོང་ཚིག་བརྒྱད་མ། — DharmaMitra zero-shot (english)"
track_type: machine-baseline
target_language: english
lang_tag: en
translation_of: 1-SOURCES/Text/བློ་སྦྱོང་ཚིག་བརྒྱད་མ།.md
generator: dharmamitra cat-translate v1
endpoint: https://dharmamitra.org/api-search/cat-translate/v1/translate
rails_used: none
termbase: none
status: draft
seeded: 2026-08-26
---

# en-dharmamitra-zeroshot — about this track

A **machine baseline**, not a rails-governed translation track.

Every file here is raw output of DharmaMitra's public `cat-translate` endpoint,
produced by
`4-SYSTEM/Skills/dharmamitra-translate/scripts/dm_translate.py`, which sends a
small batch of adjacent block IDs per call and splits the response back apart on
segment markers. (Texts translated before 2026-08-27 were sent one block per
call; each block's ledger record carries the `batch_size` it was produced under.) Nothing in it
passed through `2-RAILS/`: no verse-context package, no consolidated bilingual
glossary, no per-track `termbase.md`, no human review. It therefore does **not**
satisfy the Translation-track contract in
[`../About Transformations.md`](../About%20Transformations.md) §3, and it is not
eligible to be marked `status: complete` or to be cited by any other
transformation.

## What it is for

- A comparison baseline against which a rails-governed translation can be judged.
- A drafting aid and a source of candidate renderings for
  `2-RAILS/Bilingual-Glossaries/` (via `glossary-extract-raw`).
- A fast first look at a text in a language no track covers yet.

## What governs it

| File | Role |
| --- | --- |
| `style.md` | The `style_instruction` string, sent **verbatim** to the API on every call. Edit it, then re-run with `--force` to regenerate. |
| `context-header.md` | The fixed work-level orientation prepended to every call's `context` field. |
| `work/en.jsonl` | Append-only ledger: one record per API call — source, translation, the exact context sent, timings. The audit trail and the resume point. |
| `བློ་སྦྱོང་ཚིག་བརྒྱད་མ།-en.md` | The rendered translation, block-ID aligned to the source. |

## Provenance

- Endpoint: `https://dharmamitra.org/api-search/cat-translate/v1/translate` (public, unauthenticated)
- Source: [`1-SOURCES/Text/བློ་སྦྱོང་ཚིག་བརྒྱད་མ།.md`](1-SOURCES/Text/བློ་སྦྱོང་ཚིག་བརྒྱད་མ།.md)
- Granularity: up to 3 adjacent source block IDs per API call, never crossing a
  heading; each block still gets its own ledger record and its own block ID.
- Rolling context: the preceding translated blocks of this same document are
  threaded into each call so terminology and register stay coherent.

Regenerate or extend with:

```bash
python3 4-SYSTEM/Skills/dharmamitra-translate/scripts/dm_translate.py \
  --source "1-SOURCES/Text/བློ་སྦྱོང་ཚིག་བརྒྱད་མ།.md" --lang english
```

### A note on `context-header.md` (historic defect, now fixed)

`dm_translate.py` used to keep ONE context header per *track* and seed it from
whichever text ran first. Every English text was therefore sent
`Work: བློ་སྦྱོང་ཚིག་བརྒྱད་མ། (author: གླང་རི་ཐང་པ།)` — i.e. all 95 texts told the API
they were that one mind-training text. Verified from the ledgers, not inferred.

Fixed 2026-08-31: `context-header.md` is now a work-NEUTRAL track preamble, and
the per-text `Work: …` line is derived from each source's own metadata and
appended at call time.

**The existing English output was NOT regenerated.** A controlled re-run of
`གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` `^1`–`^4` under the corrected header was compared against
the shipped output: the differences are cosmetic (terminal punctuation,
`oṃ`/`Oṃ` capitalisation, "you act for"/"you work for") with identical
terminology, content and line structure. Regenerating all 95 texts would cost a
full day's quota (~380 calls) for no substantive gain, so it was not done.

### Why two blocks per track do not match their source's line count

`stamp_metadata.py` deliberately replaces the translation of a block that *is*
the work's title — including the `རྒྱ་གར་སྐད་དུ། … བོད་སྐད་དུ། <title>` bilingual
title formula — with the researched title from `1-SOURCES/liturgy-titles.json`,
so that the machine's own rendering of the title does not stand as a line of
translation. Those source blocks have two lines (Sanskrit, then Tibetan) and the
researched title is one line.

Affected: `བྱམས་པའི་སྨོན་ལམ།` `^1` and `འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་རྒྱལ་པོ།` `^1`.
This is intended, is re-applied on every `stamp_metadata.py --all`, and should
NOT be "fixed" by re-translating — the block id is preserved, so the segment
alignment is unaffected. Every other block in both tracks matches its source
line for line.
