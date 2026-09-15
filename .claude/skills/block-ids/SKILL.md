---
name: block-ids
description: Stamp Obsidian block IDs onto the expert-segmented liturgy notes in 0-INBOX and write the prepared copies to 1-SOURCES/Text. Use when asked to add block ids, add TOC/section ids, stamp the inbox, prepare source notes, or health-check the ids on already-stamped texts.
---

# Block IDs

`0-INBOX/` holds liturgy notes whose **TOC (headings) and segmentation
(blank-line-separated blocks) are already correct** — a domain expert made
every judgment call. The only thing missing is an addressable id per
heading and per segment. That job is fully mechanical, so it is a script,
not a judgment call, and not a subagent:

```
4-SYSTEM/scripts/block_ids.py
```

**Never edit the text.** No splitting, merging, reordering, re-wrapping,
retitling, renumbering, or "fixing" of the expert's segmentation or
headings — not even something that looks like an obvious defect. If a file
looks wrong, report it and stop; correcting it is the expert's call, made
outside this pipeline.

## Format

```
# ༄༅། །Title              ^0
## Section k               ^k-0     a heading is "segment 0" of its section
<segment>                  ^k-1
### Subsection j           ^k-j-0
<segment>                  ^k-j-1
```

- Flat texts (no `##` anywhere) number straight through: `^1`, `^2`, …
- Segments under the H1 *before* the first `##` get `^0-1`, `^0-2`, …
- A text with no headings at all numbers from `^1` (its title line is
  simply segment 1).
- The id goes on the **last line** of its unit, preceded by exactly one
  space, appended verbatim — a line already ending in a space keeps it, so
  the id is exactly reversible.
- Obsidian block ids allow **only digits, letters and hyphens**. Never a
  dot. `^2-1-1`, not `^2.1.1`.

## Workflow

Run from the vault root. Confirm the tree is clean first — the Obsidian
git plugin auto-commits every few minutes, so pin a baseline rather than
trusting floating HEAD:

```bash
git status --porcelain -- 0-INBOX/ 1-SOURCES/Text/
BASE=$(git rev-parse HEAD)
```

**1. Plan (writes nothing).** Classify every file and confirm the counts
match what the expert expects:

```bash
python3 4-SYSTEM/scripts/block_ids.py plan 0-INBOX
```

Add `-v` to print the full id map for one file. Any `ABORT` line is a file
the parser refuses — read the reason, resolve it with the user, and never
force it through.

**2. Stamp.** Sources are read-only; stamped copies are written to
`1-SOURCES/Text/`:

```bash
python3 4-SYSTEM/scripts/block_ids.py stamp 0-INBOX --out-dir 1-SOURCES/Text
```

`stamp` asserts the round-trip *before every individual write* and skips
any file that fails, so a bad parse can never produce a written file. A
source that already carries ids is refused unless you pass `--restamp`.

**3. Verify.** Non-negotiable, every run:

```bash
python3 4-SYSTEM/scripts/block_ids.py verify 1-SOURCES/Text --src-dir 0-INBOX
```

Must print `0 FAILED`. It checks that frontmatter is byte-identical to the
source, that the body is byte-identical once ids are stripped, that every
heading and segment is stamped exactly once, and that no id is duplicated
or stranded mid-segment. On failure, delete the output and fix the script
— never hand-edit a stamped file.

**4. Report.** Per run: files stamped, type breakdown, total ids, verify
result, and any aborted file with its reason.

## The contract

`strip(stamp(x)) == x`, byte for byte — trailing whitespace, blank runs,
and a missing final newline all preserved. This is what makes "the
segmentation is intact" a proven property rather than a promise, and it is
why `strip` exists as a command. To re-check it by hand at any time:

```bash
python3 4-SYSTEM/scripts/block_ids.py strip "1-SOURCES/Text/<name>.md" \
  | diff - "0-INBOX/<name>.md" && echo IDENTICAL
```

## Linting after human edits

Experts do edit stamped notes in Obsidian, and vault-backup commits sync
those edits in. That easily breaks ids — stranded mid-block, deleted, or
missing the space before `^`. `lint` finds it without needing a source:

```bash
python3 4-SYSTEM/scripts/block_ids.py lint 1-SOURCES/Text
```

Report what it finds. Never silently re-stamp: if the expert resegmented a
text, every downstream id shifts, and whether to accept that renumbering
is their decision.

## What the script refuses, and why

Each of these aborts one file with a reason rather than guessing:

- more than one H1, or an H1 that is not the first thing in the body
- an H3 before any H2, or a heading deeper than `###`
- an H2 with **both** direct segments and H3 children — the id scheme
  cannot express that unambiguously; the fix is to give those loose
  segments their own `###`
- missing or unterminated frontmatter
- a source that already carries ids (without `--restamp`)

## Corpus state (surveyed 2026-08-26)

103 files, 2,039 segments, 128 headings → **2,167 ids**. Every file has at
most one H1 and it is always the title, so real TOC levels are `##` and
`###` only; nesting never goes deeper than `###`.

| Type | Shape | Files |
|---|---|---|
| A | H1 title only, no TOC | 95 |
| B | H1 + H2 | 5 |
| C | H1 + H2 + H3 | 2 |
| D | no headings at all | 1 |

Quirks that are **source truth, not defects** — preserve them:

- ~1,225 lines carry trailing whitespace, spread across all line
  positions. Genuine source noise. Never `rstrip`.
- 14 "blank" lines are a lone space; they must count as separators.
- 27 separators are double-blank; they must not create empty segments.
- 85 of 103 files have no final newline.
- `བཀའ་ཐང་བསྡུས་པ།` has a legitimate 79-line segment.

## Downstream, not yet updated

**`4-SYSTEM/CLAUDE.md` §2 currently instructs agents "Notes carry no block
IDs … Do not add `^chapter-verse` anchors."** That directive is superseded
by this skill and will otherwise cause an agent to undo this work — it
needs rewriting. `README.md` ("What a source note contains") and
`4-SYSTEM/scripts/build_payloads.py` say the same thing and are equally
stale. Note that block ids are what the pipeline repo's
`tools/parser/parser.py` derives spans from, so stamping them is what
makes that standard parser able to read these notes at all.
`1-SOURCES/liturgy-catalog.json`
is also stale — 100 entries, none of whose `file` values match the current
103 inbox filenames (the catalog stores names truncated before the final
`།`). Flag both before any upload; do not quietly rewrite them as part of
a stamping run.
