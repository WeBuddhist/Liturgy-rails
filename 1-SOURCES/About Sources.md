# 1-SOURCES — Ground truth

This folder holds the **prepared liturgy texts** the vault is built on: the
100 most-recited Tibetan liturgy texts, ingested from the OpenPecha backend
and normalised — metadata, heading structure, segmentation — so that
downstream rails and transformations can cite them precisely, and so that
the upload payloads can be generated mechanically.

Nothing in this folder is interpretive. Files are ingested *as received*
from their canonical instance in the backend and lightly normalised. Any
interpretive claim — a sense assignment, a commentarial reading, a
practice note — belongs in `2-RAILS/`, not here.

---

## 1. What is here

| Path | Role |
|---|---|
| `Text/` | The 100 prepared source notes, one file per text, named by Tibetan title |
| `liturgy-catalog.json` | The authoritative registry: rank ↔ file ↔ title ↔ backend ids ↔ author/license/bdrc ↔ layout |

Raw, pre-formatting content for every text is kept in [`../0-INBOX/`](../0-INBOX/)
under the same filename — the verbatim instance content, so any formatting
decision can be checked against what the backend actually returned.

## 2. Provenance

All texts come from OpenPecha category `dJpr4gMF72E4UpCnJ84sh` (Tibetan,
critical instances), fetched from `https://api-aq25662yyq-uc.a.run.app`.
The corpus of 205 was narrowed to the 100 most-recited using the backend's
own recitation ranking (`recitations_bo.json`), matched by normalised
title; `liturgy-catalog.json` preserves that rank.

**Every text already exists in OpenPecha.** Its `text_id` and `instance_id`
live in `liturgy-catalog.json` and *deliberately not* in the note
frontmatter. An upload of edited content therefore **updates the existing
instance** (`PUT /v2/instances/{instance_id}`) — it never creates a new
text.

## 3. What a note contains

Exactly three things, nothing else:

1. **Metadata** — YAML frontmatter, keys per the pipeline's root-text
   schema (`title, author, language, lang_tag, file_type, edition_type,
   category_id, license, source, bdrc_work_id, date`). Values are taken
   from the backend where present and **left empty where not** — an empty
   key is a truthful "not recorded upstream", never a guess.
2. **Table of contents** — the markdown headings: `# <title>` for the
   document, `## 1. <title>` for the section.
3. **Segmentation** — one blank-line-separated block per segment: a
   four-line verse stanza, or a single prose/mantra unit.

### No block IDs

Unlike the `bodhisattvacaryāvatāra` vault, these notes carry **no
`^chapter-verse` anchors**. The v2 API expresses segmentation as character
spans, so the blank-line block boundary *is* the segmentation and an ID
would be redundant scaffolding. The consequence to know:
`webuddhist-library-data-pipeline/tools/parser/parser.py` **cannot read
these notes** (it derives spans from block IDs);
[`../4-SYSTEM/scripts/build_payloads.py`](../4-SYSTEM/scripts/build_payloads.py)
is the parser for this format.

## 4. Normalisation applied

Null bytes stripped; non-breaking tsheg ༌ (U+0F0C) → ་ (U+0F0B);
shad-sandwiched Tibetan verse counters (`མ། ༡ །`) removed — dates, the ༧
honorific and recitation counts are never touched; whitespace collapsed.
Verse lines are split at `། །`, `༔`, `།།`, and the post-ག single-shad
ending (`ག །`).

## 5. Current state

| | |
|---|---|
| Texts | 100 (88 `layout: verse`, 12 `layout: prose`) |
| `license` | 100/100 filled |
| `bdrc_work_id` | 85/100 filled |
| `author` | 32/100 filled |
| `category_id` | empty — the WeBuddhist target category is not yet chosen |
| `date` | empty — the backend's `date` is an ingestion timestamp, not a composition date |

The `layout: prose` texts (mixed metre, mantra-interleaved ritual texts)
are the review queue: their segment boundaries are the ones most worth a
human pass before upload.

## 6. Checklist — adding a text

1. Fetch the instance content and add it verbatim to `0-INBOX/<title>.md`.
2. Add its row to `liturgy-catalog.json` (rank, file, title, `text_id`,
   `instance_id`, author/license/bdrc as the backend reports them).
3. Generate the prepared note into `Text/` — normally by re-running
   `4-SYSTEM/scripts/format_liturgy_batch.py`, which does all three steps
   for the whole corpus.
4. Check the segmentation: verse texts should show clean four-line
   stanzas; prose texts one recitation unit per block.
5. Rebuild payloads and confirm the note parses:
   `python3 4-SYSTEM/scripts/build_payloads.py`.
