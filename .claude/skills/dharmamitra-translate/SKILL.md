---
name: dharmamitra-translate
description: Produce a zero-shot machine-baseline translation of a block-ID'd source text by calling DharmaMitra's public cat-translate API on small batches of adjacent block IDs, threading the document's own preceding translations back in as context, and writing the result to a new machine-baseline track under 3-TRANSFORMATIONS/Translations/ — never replacing an existing translation.
---

# dharmamitra-translate

Translates a source file from `1-SOURCES/` into any target language by calling DharmaMitra's public `cat-translate` endpoint on **a small batch of adjacent block IDs** — three stanzas, say — and threading the preceding blocks of the same document back into each call as context, so terminology and register stay coherent across the text. Batched blocks are separated by `[[n]]` marker lines that the model echoes back, and the response is split apart on those markers; each block still gets its own ledger record and its own block ID. The output is a **machine baseline**: raw API output, block-ID aligned, no `2-RAILS/` involvement and no termbase, written to its own track folder and marked `status: draft`. It never touches `1-SOURCES/` and never overwrites a rails-governed or human translation.

Correct output is a track folder whose translation file carries one target-language block per source block ID, in source order, with every block ID preserved exactly; plus an append-only JSONL ledger recording the exact request behind every line, so any rendering can be traced to the call that produced it.

The failure mode it prevents: silently mixing machine output into the vault's cited translation chain. Everything this skill writes is labelled `track_type: machine-baseline`, `rails_used: none`, and is explicitly ineligible to be cited by any `3-TRANSFORMATIONS/` output or marked `complete`.

---

## Inputs

| Input | Description | Required |
|---|---|---|
| **Source file** | A block-ID'd file under `1-SOURCES/` — root text or commentary. Every translatable block must end in ` ^<id>`. Blocks without an ID are skipped. | yes |
| **Target language** | A free-form language **label**, not an ISO code: `english`, `german`, `modern chinese`, `hindi`. Passed verbatim to the API as `target_language`. | yes |
| **Source language** | Which `input_*` field the blocks fill: `tibetan` (default), `sanskrit`, `chinese`, `pali`. | no |
| **Style instruction** | Free-form prose read **verbatim** by the API model. Lives at `<track>/style.md`; seeded on first run and human-editable thereafter. | no |
| **Context header** | Fixed work-level orientation prepended to every call's `context`. Lives at `<track>/context-header.md`; seeded from the source's frontmatter. | no |
| **Glossary** *(optional)* | A file of `source term<TAB>target rendering` lines. Entries whose source term appears in the current block are added to that call's context. A consolidated `2-RAILS/Bilingual-Glossaries/<src>-<tgt>.md` can be reduced to this shape by hand. | no |

If the target language is not stated in the user's request, ask before running. Do not default to English silently.

## Output

One track folder per target language:

```
3-TRANSFORMATIONS/Translations/<lang-tag>-dharmamitra-zeroshot/
├── about.md                    # what this track is, and what it is not (seeded)
├── style.md                    # the style_instruction sent verbatim (seeded, editable)
├── context-header.md           # fixed work-level context (seeded, editable)
├── <text-slug>-<lang-tag>.md   # the rendered block-ID-aligned translation
└── work/
    └── <lang-tag>.jsonl        # append-only ledger: one record per API call
```

Example: `3-TRANSFORMATIONS/Translations/en-dharmamitra-zeroshot/praise-of-the-twenty-one-taras-en.md`.

---

## Output file format

The rendered translation file:

````markdown
---
title: "<English title of work> — DharmaMitra zero-shot (<language>)"
file_type: translation
track_type: machine-baseline
translation_of: 1-SOURCES/Text/<source file>.md
source_language: tibetan
target_language: english
lang_tag: en
generator: dharmamitra cat-translate v1
endpoint: "https://dharmamitra.org/api-search/cat-translate/v1/translate"
focus: tibetan
context_blocks: 3
batching: "<=3 blocks/call, <=900 src chars, <=6000 payload chars"
style_instruction: "<verbatim string sent to the API>"
rails_used: none
generated: YYYY-MM-DD
blocks_translated: 29
blocks_total: 29
status: draft
---

> [!warning] Machine baseline — not a rails-governed translation.
> Every line below is raw DharmaMitra `cat-translate` output, produced in small
> batches of adjacent blocks with no termbase, no verse-context rails, and no
> human review. …

# <source title line, reproduced>

## <source heading> ^I-0

> <source line 1>
> <source line 2>

<translation line 1>
<translation line 2> ^I-1
````

Rules the render obeys:

- Source headings are reproduced verbatim with their `^N-0` anchors; headings are **not** sent to the API.
- Each source block appears as a blockquote (`--layout parallel`, the default) immediately above its translation; `--layout translation-only` drops the blockquotes.
- The block ID sits at the end of the **last line** of its translation — the same position the source uses.
- A block present in the source but absent from the ledger renders as `*[not yet translated]* ^<id>`, never as a silent gap.

One ledger record **per block** (`work/<text>-<lang-tag>.jsonl`) — batching never collapses two blocks into one record — holding `block_id`, `heading`, `source`, `translation`, `target_language`, `focus`, `style_instruction`, the exact `context` string sent, `endpoint`, `elapsed_s`, `ts`, plus `batch_size`, `batch_block_ids` and `batch_fallback` recording which call produced it. `elapsed_s` is the elapsed time of the call the block came from, so it is shared across a batch — read it together with `batch_size`.

---

## Batching

DharmaMitra's own agent chunks source into **3–5 sentences (~80–150 source words)** per `cat-translate` call, one sentence per line. This skill follows that guidance at block granularity.

Latency is nearly all fixed overhead — measured against the live endpoint, one block takes ~8 s and five blocks ~7.6 s — so the batch size, not the text length, decides how long a run takes. On this corpus (1 900 blocks, median 152 chars / 4 lines each) `--batch 3` turns a ~2.5 h full-corpus run into roughly 50 minutes.

Batching also decides whether the work is **possible at all**, not merely faster: the endpoint allows 400 requests/day, so 1 900 blocks one-per-call would need four days of quota. At `--batch 5` the same corpus costs ~390 calls and fits inside a single day. Treat the call count, not the wall clock, as the budget.

| Knob | Default | What it bounds |
|---|---|---|
| `--batch` | 3 | Blocks per call. `1` = one call per block. 5 is DharmaMitra's stated ceiling. |
| `--batch-max-chars` | 900 | Source characters in one batch — roughly their 80–150 source words in Tibetan. |
| `--batch-max-lines` | 32 | Source lines in one batch; caps how long the *output* can run, which is what risks the 100 s upstream cap. |
| `--payload-cap` | 6000 | **context + style_instruction + source** for the whole call. The prompt is charged against the batch, not ignored: the effective character cap is `payload-cap − context-cap − len(style)`, so a longer `style.md` or a bigger `--context-blocks` automatically shrinks the batch rather than silently inflating the request. |

A batch is also closed at a **heading boundary** — sections are never mixed — and any block that alone busts a cap is sent on its own. Both are automatic; the run prints the plan before it starts:

```
batching   : 44 calls for 131 blocks (<=3 blocks, <=900 chars, <=32 lines per call)
[1/44] ^1,^2,^3  (3 blk, 588 src, 1452 payload) … 4.4s  Emaho!
```

**When to lower `--batch`.** If the end-of-run report lists many blocks whose translation line count diverges from the source's, or if a text is long continuous prose rather than discrete stanzas, drop to `--batch 2` or `1` for that text. Raising to `--batch 5` is within DharmaMitra's guidance and is worth it on long, regular verse texts.

**Marker protocol.** For a batch of more than one block the source is sent as `[[1]]`, block, `[[2]]`, block, … and a clause is appended to the style instruction telling the model to reproduce every marker verbatim on its own line. A solo call sends `style.md` **verbatim**, with no marker clause, exactly as before. The marker clause is transport, not style: it is appended for the call and never written into `style.md` or the output frontmatter.

---

## Rules

1. **Never write to `1-SOURCES/`.** This skill reads it and nothing more.
2. **Never write into an existing translation track.** Output goes only to a `*-dharmamitra-zeroshot` track (or an explicit `--track` the user named for this purpose). If the target folder already holds a non-baseline translation, stop and report it.
3. **Batch small, and never guess a split.** Up to `--batch` blocks (default 3) go in one call, separated by `[[n]]` marker lines. A batch never crosses a heading and never exceeds the character, line or payload caps. If the markers do not come back as exactly `[[1]]`…`[[N]]`, in order, each followed by non-empty text, the script **discards that response** and re-runs the batch one block per call. Alignment is never inferred from line counts or blank lines. Never split one block across calls. `--batch 1` restores one call per block.
4. **Every block ID in the source appears exactly once in the output**, in source order, unaltered. Block IDs are never renumbered, merged, or invented.
5. **This output is never cited.** It is not a rail, it may not be cited by any other `3-TRANSFORMATIONS/` output, and it must not be promoted past `status: draft` by an LLM. Its renderings may feed `2-RAILS/Bilingual-Glossaries/` only through `glossary-extract-raw`, which re-checks them against the sources.
6. **`target_language` is a label, never an ISO code** (`"german"`, not `"de"`). The lang **tag** (`de`) is used only for folder and file naming.
7. **Do not lower the 90 s timeout.** The endpoint is synchronous, 1–8 s typical; a Cloudflare cap at 100 s surfaces as HTTP 524.
8. **Respect the rate limit — it is a DAILY quota.** The endpoint is public, unauthenticated and shared, and enforces **400 requests per day** (observed 2026-08-27: `{"error":"Rate limit exceeded: 400 per 1 day"}`). It also throttles short bursts. Two consequences:

   - **Budget the day before starting.** Count calls, not blocks: at `--batch 5` this corpus's 1 900 blocks cost ~490 calls, so a full re-translation does **not** fit in one day, while an incremental run usually does. `--report-only`/`--dry-run` print the call count without spending any.
   - **A daily 429 aborts immediately.** Backing off seconds against a daily quota is useless and keeps pounding a service that has already said no, so `call_api` raises `DailyQuotaExceeded` the moment the body says `per 1 day`. Short-burst 429s still back off 20 s → 180 s. Never work around either by running several instances in parallel.

   Every retry, including a failed one, spends quota. Repairs are the expensive case: up to 4 calls per block.
9. **The ledger is append-only.** Never hand-edit it. To change a rendering, edit `style.md` and re-run that block with `--force --only <id>`.
10. **Report a partial run as partial.** If the run stops early, say which block it stopped at and how many blocks are done — the frontmatter's `blocks_translated` / `blocks_total` must match reality.

---

## Procedure

### Step 1 — Confirm the inputs

1. Confirm the source file exists under `1-SOURCES/` and its blocks carry `^<id>` markers:
   ```bash
   python3 4-SYSTEM/Skills/dharmamitra-translate/scripts/dm_translate.py \
     --source "1-SOURCES/Text/<file>.md" --list
   ```
   This parses only — it makes no API calls. Check the block count against the vault annex's addressing scheme before going further.
2. Confirm the target language with the user if they did not state one.
3. Confirm the target track folder does not already hold a non-baseline translation.

### Step 2 — Smoke-test six blocks

```bash
python3 4-SYSTEM/Skills/dharmamitra-translate/scripts/dm_translate.py \
  --source "1-SOURCES/Text/<file>.md" --lang <language> --limit 6
```

Six rather than three, so the smoke test exercises **two real batches** and not just one. Check the printed plan line first: if it reports one call per block, the caps are squeezing the batch — usually a long `style.md` against `--payload-cap`.

This seeds `about.md`, `style.md` and `context-header.md` in the track folder on first run. Read the three translations back before continuing:

- Does the line count of each translation match its source block? (Verse should stay verse.)
- Are mantra syllables and proper names transliterated rather than translated?
- Is the register what the user asked for?
- Did the run report any marker fallback or line-count divergence? A fallback now and then is the safety net working; a fallback on most batches means the style instruction is fighting the marker clause — simplify `style.md`.

If any answer is wrong, edit `<track>/style.md` — its text goes verbatim to the API — and re-run the same three blocks with `--force`. Iterate here, not after 29 blocks.

### Step 3 — Run the remaining blocks

```bash
python3 4-SYSTEM/Skills/dharmamitra-translate/scripts/dm_translate.py \
  --source "1-SOURCES/Text/<file>.md" --lang <language>
```

Blocks already in the ledger are skipped, so this command is also the resume command — resumed blocks are re-batched from whatever is left, which is safe because each block is translated and recorded independently. If it stops on a rate limit, wait a minute and run it again, or raise `--sleep`.

### Step 4 — Verify the render

1. Confirm `blocks_translated == blocks_total` in the output frontmatter, or state the shortfall.
2. Confirm no `*[not yet translated]*` markers remain (or list the blocks that still carry them), and that no `[[n]]` marker leaked into the rendered text:
   ```bash
   grep -n '\[\[[0-9]\+\]\]' "3-TRANSFORMATIONS/Translations/<track>/<file>.md" || echo "no stray markers"
   ```
3. Spot-check that block IDs in the output match the source one-for-one:
   ```bash
   diff <(grep -o '\^[A-Za-z0-9-]*$' "1-SOURCES/Text/<file>.md") \
        <(grep -o '\^[A-Za-z0-9-]*$' "3-TRANSFORMATIONS/Translations/<track>/<file>.md")
   ```
4. Re-render at any time without re-calling the API: add `--render-only`.

### Step 5 — Report

Tell the user: blocks done / total, calls made (batching is what makes the run affordable — say how many calls covered how many blocks), the track path, the style instruction in force, any batch that fell back to one-block calls, and any block where the API's line count diverged from the source's. Do not mark anything `complete`; a domain specialist owns that decision, and for a machine baseline the answer is normally that it stays `draft` permanently.

### Adding another language

Re-run Step 2–4 with a different `--lang`. Each language gets its own track folder, its own `style.md`, and its own ledger; no other track is touched.

---

## Completion check

- [ ] `--list` block count matches the source's addressing scheme in the vault annex
- [ ] Target language was stated by the user or explicitly confirmed
- [ ] Six-block smoke test (two batches) was read back and the style instruction adjusted if needed
- [ ] The batching plan line was checked, and any marker fallbacks or line-count divergences reported to the user
- [ ] Track folder contains `about.md`, `style.md`, `context-header.md`, the rendered translation, and `work/<lang-tag>.jsonl`
- [ ] Every source block ID appears exactly once in the rendered file, in source order
- [ ] `blocks_translated` / `blocks_total` in the frontmatter match the ledger and were reported honestly
- [ ] Output frontmatter carries `track_type: machine-baseline`, `rails_used: none`, `status: draft`
- [ ] Nothing under `1-SOURCES/`, `2-RAILS/`, or any other translation track was modified
