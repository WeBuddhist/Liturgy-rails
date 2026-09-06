---
title: "mn — Gemini zero-shot (mongolian)"
track_type: machine-baseline
target_language: mongolian
lang_tag: mn
source_language: tibetan
generator: gemini-3.1-pro-preview
endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent
rails_used: none
termbase: none
status: draft
seeded: 2026-09-06
---

# Gemini/mn — about this track

A **machine baseline**, not a rails-governed translation track.

Every file here is raw output of Google Gemini (model `gemini-3.1-pro-preview`, recorded per
block in the ledger as `model_version`), produced by
`.claude/skills/gemini-translate/scripts/gm_translate.py`, which sends a small
batch of adjacent block IDs per call and asks for a JSON object holding one
array of lines per block. Nothing in it passed through `2-RAILS/`: no
verse-context package, no consolidated bilingual glossary, no per-track
`termbase.md`, no human review. It therefore does **not** satisfy the
Translation-track contract in
[`../../About Transformations.md`](../../About%20Transformations.md) §3, and it is
not eligible to be marked `status: complete` or to be cited by any other
transformation.

**Source.** Every block is translated from the Tibetan in `1-SOURCES/Text/`,
which is the closest thing to the original that exists. `translation_of` and the
segment alignment therefore point at the Tibetan text. If a run was given an
existing machine translation as *reference* (`--reference-track`), that fact is
recorded in the frontmatter (`reference_translation`) and on every ledger
record (`reference_used`); the reference was context, not source.

## What it is for

- A first display translation for the app in a language no track covers yet.
- A comparison baseline against which a rails-governed translation can be judged.
- A drafting aid and a source of candidate renderings for
  `2-RAILS/Bilingual-Glossaries/` (via `glossary-extract-raw`).

## What governs it

| File | Role |
| --- | --- |
| `style.md` | The style instruction, sent **verbatim** as the system prompt on every call (followed by the fixed output contract). Edit it, then re-run with `--force` to regenerate. |
| `context-header.md` | A work-NEUTRAL, track-wide preamble prepended to every call. The per-text `Work: …` line is derived from each source's own metadata and appended after it. |
| `work/<text>-mn.jsonl` | Append-only ledger, one per source text: one record per block, holding source, translation, the exact context sent, model version, token usage, line-parity result and timings. The audit trail and the resume point. |
| `<text>-mn.md` | The rendered translation, block-ID aligned to the source. |

## Line parity

The whole point of a block-ID-aligned track is that block `^N` here renders
block `^N` of the Tibetan, line for line. The script checks every block's line
count against its source before recording it; a block that comes back wrong is
re-run alone with the required count stated, and only an exact match is
accepted silently. Anything still divergent is recorded with
`line_parity: false` and listed in the run report for human attention.

Two blocks per track are allowed to differ by design: where a text opens with
the `རྒྱ་གར་སྐད་དུ། … བོད་སྐད་དུ།` bilingual title formula, `stamp_metadata.py`
replaces the machine's rendering of that title block with the researched title
from `1-SOURCES/liturgy-titles.json`. Do not "fix" those by re-translating.

Regenerate or extend with:

```bash
python3 .claude/skills/gemini-translate/scripts/gm_translate.py \
  --source "1-SOURCES/Text/<text>.md" --lang mongolian
python3 4-SYSTEM/scripts/stamp_metadata.py --ids --track-meta --titles --track "3-TRANSFORMATIONS/Translations/Gemini/mn"
```

The second command is not optional: the renderer rebuilds each file's
frontmatter from its ledger on every run and knows nothing about backend ids,
provenance keys or researched titles.

## Run history

| Date | Step | Result |
| --- | --- | --- |
| 2026-09-06 | Pilot: `བློ་སྦྱོང་ཚིག་བརྒྱད་མ།`, `སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ།` | 39/39 blocks, line parity clean; reviewed block by block in `pilot-review.md` (READY FOR FULL RUN, `style.md` unchanged) |
| 2026-09-06 | Full corpus, `gm_corpus.py --lang` (model `gemini-3.1-pro-preview`, thinking default) | 94/94 texts, 1892/1892 blocks, 206 calls in the final resumed run, 0 line-parity failures, 0 failed blocks |
| 2026-09-06 | Spot-read of three unseen texts (`corpus-run-review.md`) | content sound; one systematic defect: recurring proper names spelled inconsistently across blocks |
| 2026-09-06 | Names pinned (`gm_names.py --propose`; 47 glossary entries) and drifting blocks re-run (`--rerun`, two passes) | 15 block(s) of 452 name occurrences still lack the pinned form after the boundary-aware check — epithets or longer names containing the key, listed by `gm_names.py --check` |
| 2026-09-06 | Ornament re-run (output contract now forbids copying ༈ ། ༔) and `gm_verify.py` | OK: every file whole, block ids identical to the Tibetan, no stray script |

Every re-run is an appended ledger record produced by the same model under the
same `style.md`, with the glossary hits in context; nothing was hand-edited.
