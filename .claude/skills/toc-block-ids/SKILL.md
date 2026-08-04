---
name: toc-block-ids
description: Insert TOC headings and stamp block IDs into 1-SOURCES/Text liturgy notes, then verify byte-invariance. Use when asked to run the TOC pipeline, add block ids, process liturgy texts for TOC, or extend the toc-pilot to more texts.
---

# TOC + block-ID pipeline

Adds a heading tree and Obsidian block IDs to liturgy source notes in
`1-SOURCES/Text/`, without touching frontmatter or segmentation. The
mechanical work lives in `4-SYSTEM/scripts/toc_pipeline.py`; the only
judgment step — deciding the section tree — is delegated to one subagent
per text. Run everything from the vault root.

## Target format (fixed — do not improvise)

```
# ༄༅། །<full title>། ^0                       H1 gets ^0

## 0. <preamble title> ^I-0                    optional, only if text has
                                               front matter before ch. 1
## 1. <chapter title> ^1-0                     content chapters: Arabic
## 2. <chapter title> ^2-0                     numeral prefix at ## ONLY

### <subsection> ^1-1-0                        ###/####: no numeral prefix
#### <sub-subsection> ^1-1-2-0

## <colophon title> ^a-0                       colophons: unnumbered,
## <colophon title> ^b-0                       letter prefixes
```

Every content block gets ` ^<prefix>-<n>` appended to its **last line**.

**Block-ID depth cap (hard rule):** block IDs have at most 3 segments
(`^3-2-9`). Blocks are numbered against the nearest enclosing `##` or
`###` — never a `####`. A `####` heading keeps its own deeper heading id
and consumes a number from the same shared counter, so ids stay unique
and no block id is a prefix of a heading id. The script enforces this;
never hand-write ids.

Other invariants the script enforces:

- Frontmatter is byte-identical to the original.
- Body is byte-identical to the original once headings and ids are
  stripped. Blocks are never split, merged, or reordered.
- The formatter wrapper heading `## 1. <full title>` (duplicate of the
  H1) is removed automatically.
- A file that already carries ids is refused — `git restore` it first.

## Workflow

Work on a dedicated branch; git is the only rollback.

### 1. Select and extract

Pick the target files (skip any already processed — check for `^` ids).
For each:

```bash
python3 4-SYSTEM/scripts/toc_pipeline.py extract "1-SOURCES/Text/<name>.md" <scratch>/blocks_<i>.txt
```

This writes the content blocks with `[[N]]` index markers.

### 2. TOC plan (one subagent per text, run them in parallel)

Each subagent reads its `blocks_<i>.txt` and writes
`<scratch>/plan_<i>.json`:

```json
{"sections": [
  {"level": 2, "title": "<Tibetan phrase>", "before_block": 0, "kind": "preamble"},
  {"level": 2, "title": "<Tibetan phrase>", "before_block": 4, "kind": "content"},
  {"level": 3, "title": "<Tibetan phrase>", "before_block": 4, "kind": "content"},
  {"level": 2, "title": "<Tibetan phrase>", "before_block": 150, "kind": "colophon"}
]}
```

Instructions to give every subagent (adapt the text-specific hints):

- `before_block` = index of the FIRST block of the section; the heading
  is inserted immediately before it. First listed section MUST start at
  block 0.
- Boundaries come from the text's own inline announcements
  ("…ལ་ཐོག་མར་X་ནི།", enumerations དང་པོ་/གཉིས་པ་…, ༈ or ཨེ་མ་ཧོ༔ marks,
  chapter colophons "…ལེའུ་སྟེ་…པའོ" which close a chapter, never open
  the next). Titles are Tibetan phrases drawn from the text, no numbers
  (numbering is mechanical).
- Levels: 2 = major division, 3/4 only where the text itself nests.
  Every level-3 must fall inside a level-2, level-4 inside a level-3; a
  parent may share `before_block` with its first child. Follow the
  text's structure — no heading per stanza, no invented granularity.
- Opening homage/title/frame-story → kind `preamble`; author/translator/
  terma colophons at the end → kind `colophon`.
- Report judgment calls and ambiguous boundaries back in the reply.

**At most ONE level-2 preamble per text** (the `^I-` prefix is single).
If an agent returns two, restructure: one `## 0.` parent, the parts as
level-3 children (see plan_2 handling in the pilot).

### 3. Review the plans

Sanity-check every plan before applying: parents precede children,
`before_block` values are in order, chapter counts match the text's own
enumeration (a ལེའུ་བདུན་མ must yield 7 chapters), colophons are at the
end. Cross-check 2–3 boundaries against the blocks file.

### 4. Apply + verify

```bash
python3 4-SYSTEM/scripts/toc_pipeline.py apply  "1-SOURCES/Text/<name>.md" <scratch>/plan_<i>.json
python3 4-SYSTEM/scripts/toc_pipeline.py verify "1-SOURCES/Text/<name>.md" "1-SOURCES/Text/<name>.md"
```

`verify` must print `OK` for every file. It checks: frontmatter
byte-equal to `HEAD`, body byte-equal after stripping structure, every
block stamped exactly once, ids unique, no block id deeper than 3
segments. If it fails, `git restore` the file, fix the plan, re-apply —
never hand-edit the output.

Line-count sanity: new = old + 2×(headings inserted) − 2 (removed
wrapper).

### 5. Report

Per text: headings inserted, tree depth, blocks stamped, line delta,
verify result, and the subagent's flagged ambiguities (mid-block
boundaries etc.) for human review. Stage the files; commit only when
asked.

## Known caveats

- Boundaries land on block edges. When a section starts mid-block the
  heading goes before the block where the section's first words occur;
  resegmentation is out of scope — flag these for review.
- `4-SYSTEM/CLAUDE.md` §2 and `build_payloads.py` still describe the
  pre-id format; they need updating before processed texts are uploaded.
- Pilot reference (conventions + 4 processed texts): branch
  `toc-pilot-6texts`, texts བླ་མ་མཆོད་པའི་ཆོ་ག, ཨོ་རྒྱན་པདྨས་བཀའ་བསྡུས,
  གསོལ་འདེབས་ལེའུ་བདུན་མ, ཆགས་མེད་བདེ་སྨོན.
