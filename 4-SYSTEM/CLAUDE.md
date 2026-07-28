# CLAUDE.md — agent entry point

Operational summary for an LLM working in this vault. The authoritative
documents are each folder's `About <Folder>.md`; read the relevant one
before touching that folder.

## 1. What this vault is

An Obsidian vault of the **100 most-recited Tibetan liturgy texts**,
ingested from the OpenPecha backend and prepared for upload to the
WeBuddhist library. It follows the four-stage rails layout:

```
0-INBOX/   →   1-SOURCES/   →   2-RAILS/   →   3-TRANSFORMATIONS/
raw            prepared         descriptive     per-output
intake         source notes     context         prescriptive rails
                                                + generated output
                       ▲
                       │ all driven by
                     4-SYSTEM/   scripts, docs, templates
```

Current state: `0-INBOX/` and `1-SOURCES/` are populated and upload-ready.
`2-RAILS/` and `3-TRANSFORMATIONS/` are scaffolding — read their `About`
files before laying the first rail or track.

## 2. The load-bearing facts

**Notes carry no block IDs.** `1-SOURCES/Text/*.md` contain exactly three
things: metadata frontmatter, TOC headings, and segmentation as
blank-line-separated blocks. The v2 API expresses segmentation as
character spans, so the block boundary *is* the segmentation. Do not add
`^chapter-verse` anchors.

**Consequence:** `webuddhist-library-data-pipeline/tools/parser/parser.py`
cannot read these notes — it derives spans from block IDs and returns zero
segments. Use `4-SYSTEM/scripts/build_payloads.py` instead.

**Empty metadata values are deliberate.** A key with no value means the
backend does not record one. Never fill it with a guess. Two are empty by
policy: `category_id` (the WeBuddhist target category is not yet chosen)
and `date` (the backend's `date` is an ingestion timestamp, not a
composition date).

**These texts already exist in the backend.** Their `text_id` and
`instance_id` live in `1-SOURCES/liturgy-catalog.json`, deliberately not
in the notes. Uploading edited content means **updating the existing
instance** (`PUT /v2/instances/{instance_id}`), not creating a new text.

## 3. Scripts

Both run from the vault root.

```bash
# rebuild 0-INBOX/ + 1-SOURCES/ from the fetch artifacts (rarely needed)
python3 4-SYSTEM/scripts/format_liturgy_batch.py \
    <work_list.json> <contents.json> <text_meta_all.json> [ranking.json]

# notes → OpenPecha v2 API payloads, into 4-SYSTEM/scripts/output/
python3 4-SYSTEM/scripts/build_payloads.py --category-id <CATEGORY_ID>
```

`build_payloads.py` emits, per note, `text.json` (`POST /v2/texts`),
`instance.json` (`POST /v2/texts/{text_id}/instances` — content plus span
annotations) and `toc.json` (`POST /v2/annotations/{instance_id}/annotation`,
`type: table_of_contents`). It asserts every span slices back to exactly
its source block. TOC sections reference segment *indices*; the uploader
substitutes the backend-assigned segment ids returned by the instance POST.

## 4. Working rules

- Read the folder's `About <Folder>.md` before writing into it.
- `1-SOURCES/` holds no interpretation. Interpretive claims go to `2-RAILS/`.
- Citation flows one way: `1-SOURCES/ → 2-RAILS/ → 3-TRANSFORMATIONS/`.
  Nothing downstream cites `0-INBOX/`.
- Regenerating `1-SOURCES/` from the scripts is safe and reproducible;
  hand-edits to notes are not preserved across a regeneration, so fix the
  formatter rather than the output when a formatting rule is wrong.
- The 12 `layout: prose` texts (see `liturgy-catalog.json`) have the
  least certain segment boundaries — treat their segmentation as
  provisional until a human has reviewed it.
