---
title: "ཁྱུང་པོའི་སྨོན་ལམ — DharmaMitra zero-shot (modern chinese)"
track_type: machine-baseline
target_language: modern chinese
lang_tag: zh
translation_of: 1-SOURCES/Text/ཁྱུང་པོའི་སྨོན་ལམ།.md
generator: dharmamitra cat-translate v1
endpoint: https://dharmamitra.org/api-search/cat-translate/v1/translate
rails_used: none
termbase: none
status: draft
seeded: 2026-08-28
---

# zh-dharmamitra-zeroshot — about this track

A **machine baseline**, not a rails-governed translation track.

Every file here is raw output of DharmaMitra's public `cat-translate` endpoint,
produced in small batches of adjacent block IDs by
`4-SYSTEM/Skills/dharmamitra-translate/scripts/dm_translate.py`, then split back
apart on segment markers so each block keeps its own record. Nothing in it
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
| `work/zh.jsonl` | Append-only ledger: one record per API call — source, translation, the exact context sent, timings. The audit trail and the resume point. |
| `ཁྱུང་པོའི་སྨོན་ལམ།-zh.md` | The rendered translation, block-ID aligned to the source. |

## Provenance

- Endpoint: `https://dharmamitra.org/api-search/cat-translate/v1/translate` (public, unauthenticated)
- Source: [`1-SOURCES/Text/ཁྱུང་པོའི་སྨོན་ལམ།.md`](1-SOURCES/Text/ཁྱུང་པོའི་སྨོན་ལམ།.md)
- Granularity: up to 3 adjacent source block IDs per API call, never crossing a
  heading; each block still gets its own ledger record and its own block ID.
- Rolling context: the preceding translated blocks of this same document are
  threaded into each call so terminology and register stay coherent.

Regenerate or extend with:

```bash
python3 4-SYSTEM/Skills/dharmamitra-translate/scripts/dm_translate.py \
  --source "1-SOURCES/Text/ཁྱུང་པོའི་སྨོན་ལམ།.md" --lang modern chinese
```

---

## Status: scaffold, not yet translated

Every `*-zh.md` file here is a **scaffold**. It carries the full block structure
of its source note — every block id, every source line — with each block marked
`*[not yet translated]*`, plus the finished metadata: backend `text_id` /
`edition_id`, provenance, and the researched Chinese title as its H1. What it
does not carry is any translation. `status: scaffold`, `blocks_translated: 0`.

The one exception is the title block: where a text opens by naming itself, that
block holds the researched Chinese title rather than a placeholder, because the
title is already known and should not be machine-translated.

Seeded with `4-SYSTEM/scripts/seed_track_scaffold.sh "modern chinese" zh`, which
runs the renderer in `--render-only` mode against an empty ledger. **Zero API
calls** — nothing here was charged against the endpoint's 400-requests/day quota.

### Filling it in

```bash
python3 .claude/skills/dharmamitra-translate/scripts/dm_translate.py \
    --source "1-SOURCES/Text/<text>.md" --lang "modern chinese" --lang-tag zh \
    --out 3-TRANSFORMATIONS/Translations/Dharmamitra/zh --batch 5

python3 4-SYSTEM/scripts/stamp_metadata.py --all      # ALWAYS, afterwards
```

The second command is not optional. `dm_translate.py` rebuilds each file's
frontmatter and body from its ledger on every run and knows nothing about
backend ids, provenance or researched titles, so it reverts all of them — and
re-translates the title block. `stamp_metadata.py` restores them; it is
idempotent, so running it twice costs nothing.

Budget: ~1 900 blocks. At `--batch 5` that is roughly 400–490 calls, i.e. the
whole daily quota, so the corpus needs more than one day.

### A note on `context-header.md` (defect fixed)

This track's header deliberately named **no specific work**, because
`dm_translate.py` used to keep one context header per *track*, seeded from
whichever text ran first — which is what happened to the English track, where
all 95 texts were sent `Work: བློ་སྦྱོང་ཚིག་བརྒྱད་མ།`. This track dodged it.

Fixed 2026-08-31: the header file is now explicitly a work-NEUTRAL preamble and
the per-text `Work: …` line is derived from each source and appended at call
time. The generic preamble above is still correct — keep it work-neutral.

### Line-parity repairs

Four blocks were re-run on 2026-08-31 with a block-specific style instruction
stating the exact source line count, because the default style produced a
translation whose line count did not match its source:

| Text | Block | Before → after |
| --- | --- | --- |
| `ཁྱུང་པོའི་སྨོན་ལམ།` | `^5` | 8→9 → 8→8 |
| `དགོངས་གཏེར་སྒྲོལ་མའི་ཟབ་ཏིག་...མཎྜལ་ཆོ་ག` | `^43` | 2→4 → 2→2 |
| `འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་རྒྱལ་པོ།` | `^15` | 4→6 → 4→4 |
| `སྒྲོལ་མ་ཙིཏྟཱ་མ་ཎི་...ཐེམ་སྐས` | `^8` | 4→6 → 4→4 |

The output is still raw API output — nothing was hand-authored. Each block's
ledger record carries the exact style instruction it was produced under; the
file-level `style_instruction` shows the track default, which is what the other
blocks used.

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
