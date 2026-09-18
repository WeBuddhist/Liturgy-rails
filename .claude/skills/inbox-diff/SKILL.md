---
name: inbox-diff
description: Compare the expert-edited liturgy notes in 0-INBOX against the stamped, uploaded copies in 1-SOURCES/Text, ignoring block ids, and report per text what changed (letters, punctuation, whitespace, line breaks, re-segmentation, headings/TOC, frontmatter), which block ids and translation alignments that breaks, and which WeBuddhist v2 calls pushing it needs. Use when asked what the experts changed, whether the inbox differs from the sources or the backend, which texts need re-upload, or to plan an update of already-uploaded texts.
---

# inbox-diff

`0-INBOX/` is the experts' working copy; `1-SOURCES/Text/` is the stamped
copy that was uploaded (its `text_id`/`edition_id` live in
`4-SYSTEM/scripts/upload_ledger.json`). Once an expert edits the inbox the
two drift, and because every uploaded text id is referenced everywhere, the
backend copy has to be **updated in place**, never deleted and re-created.
This skill measures the drift and says what each text costs to push.

```
4-SYSTEM/scripts/inbox_diff.py
```

It **reads only**. Nothing here touches `0-INBOX`, `1-SOURCES` or the
backend.

## What it compares

- **Block ids are not text.** The source is run through
  `block_ids.strip_text` before comparing, so ` ^k-n` never counts as a
  change. An inbox note that carries ids of its own is stripped too and
  listed as a defect (inbox notes must not carry ids).
- **Pipeline-owned frontmatter is ignored:** `title_*`, `text_id`,
  `edition_id`, `contributor_status`, `status`, and the `[person:…]` tags
  stamped onto `author`. Every other key is an expert key and is compared.
- **Three depths of text comparison:** letters only (a real character
  change), letters + punctuation with whitespace removed (a punctuation
  edit), raw bytes (whitespace). Units are aligned old↔new on the
  letters-only key, so a split, merge, insertion or deletion of a block is
  reported as that and not as a rewrite, and re-segmenting unchanged text is
  never mistaken for a text change.
- **Block-id impact.** Ids are re-derived for the inbox body with
  `block_ids.assign_ids` and compared with the source's. A renumbered id is
  what breaks a translation alignment, so "ids kept n/m" is the number that
  decides how expensive a text is.
- **Two verdicts per text.** As of 2026-09-05 every inbox note repeats its
  title as the first body line under the H1. That one corpus-wide edit
  renumbers every text, so each text is judged twice: as it stands, and
  with that line set aside. Read the second column first.

Verdicts: `unchanged` · `metadata only` · `patch` (in-place character
edits only — `PATCH /v2/editions/{id}/content`, spans auto-shift,
alignments survive) · `rebuild` (a boundary, heading or id moved — delete
and re-post the segmentation, then re-PUT every alignment) · `blocked`
(the note cannot even be stamped; see the defects list).

## Workflow

```bash
# 1. the report (markdown + json), from the vault root
python3 4-SYSTEM/scripts/inbox_diff.py \
    --report 4-SYSTEM/inbox-diff-report.md \
    --json   4-SYSTEM/inbox-diff-report.json

# 2. optionally confirm the sources still equal the live editions (read-only GETs)
set -a; source 4-SYSTEM/scripts/.env.local; set +a
python3 4-SYSTEM/scripts/inbox_diff.py --live --report 4-SYSTEM/inbox-diff-report.md

# 3. one text in full
python3 4-SYSTEM/scripts/inbox_diff.py --only "<source stem>"
```

The report is a generated file: re-run it, never hand-edit it. Re-run
after every vault-backup merge that touches `0-INBOX` and after every
upload.

## Reading the report

1. **Summary** — verdict counts in both views, then change types by
   number of texts.
2. **The two corpus-wide edits** — the repeated title line and the added
   colophon headings (`## མཇུག་བྱང་།` / `### མཛད་བྱང་།`, spelling variants
   listed). A flat text that gains a `##` switches id scheme (`^n` →
   `^0-n`), so every id in it renumbers even though no word changed.
3. **Block-id impact** — how many texts renumber and how many alignment
   PUTs that implies, in both views.
4. **Every text** — one row each with a work code: **M** `PATCH /v2/texts`
   · **M!** edition metadata, no endpoint exists · **P*n*** *n* content
   patches · **R** delete + re-post segmentation · **A*n*** re-PUT *n*
   alignments · **T** post a table of contents · **X** blocked.
5. **Defects to hand back to the expert** — `##Heading` with no space,
   stray ids in the inbox, anything `block_ids.py` would refuse.
6. **Frontmatter changes** and **Detail** — `[-old-]{+new+}` hunks with
   context for everything beyond the two corpus-wide edits.

What the codes mean on the wire, what exists and what is missing, is in
`4-SYSTEM/backend-update-plan.md`. Keep that document in step with the
codes here.

## Rules

- Report; do not fix. A defect in an inbox note is the expert's to
  correct. Never edit `0-INBOX` to make a comparison come out clean.
- Never decide the title-line question here. Whether the repeated title
  is text (a new first block) or presentation (drop it at stamping) is
  the user's call; the two columns exist so the call can be made with the
  numbers in view.
- `--live` needs `WEBUDDHIST_API_KEY` and does GETs only. A "DIFFERS"
  line there means the source note is not what the backend holds any more
  (a local repair after upload, or a backend edit) — resolve that before
  planning any update from the source.
- Matching inbox ↔ source uses the same `norm()` rule as
  `build_review_bundle.py` (trailing shad/space dropped); inbox notes with
  no source are the backlog and are listed, not compared.
