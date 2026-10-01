# Updating already-uploaded texts on the WeBuddhist library — endpoints

Written 2026-09-15 against the live API (`OpenPecha API v2 2.11.2`,
`https://library.webuddhist.com/openapi.json`) and its server source
(`~/Desktop/work/webuddhist-library/openpecha-backend`, commit `cd1c205`,
2026-09-04). It explains the work codes in `4-SYSTEM/inbox-diff-report.md`
and answers three questions: which calls the update path uses today, which
existing calls it will need next, and which calls do not exist yet.

The constraint that shapes everything: the 94 `text_id`s are referenced
everywhere (translations point at them with `translation_of`, alignments
hang off their editions, the old-Mongo id map lists them), so **a changed
text is updated in place; it is never deleted and re-created.**

## 1. What the drift looks like (2026-09-15)

From `inbox-diff-report.md`, 94 texts compared:

| | as the inbox stands | with the repeated title line set aside |
|---|---|---|
| unchanged | 0 | 31 |
| patch (in-place character edits) | 0 | 8 |
| rebuild (segmentation must be re-posted) | 93 | 54 |
| blocked (note cannot be stamped) | 1 | 1 |
| backend requests to push everything | ≈ 886 | ≈ 562 |

Two edits are corpus-wide and decide the cost:

1. **Every inbox note repeats its title as a plain first line under the
   H1** (landed 2026-09-05, vault backup `f18d54a`). Stamped as-is it is a
   new block `^1`, every later id shifts by one, and the content carries
   the title twice (the H1 already becomes the `title` segment). Whether
   this is text or presentation is a decision to make *before* any update
   run: it is the difference between 93 rebuilds and 54.
2. **54 texts gained colophon headings** `## མཇུག་བྱང་།` (+ `### མཛད་བྱང་།`
   in 39). A flat text that gains a `##` switches id scheme (`^n` → `^0-n`,
   `^1-0`, `^1-1-1`), so every id renumbers although no word changed. Three
   spellings occur (`མཛད་བྱང་ས།`, `མཛུད་བྱང་།`) and one note writes
   `##མཇུག་བྱང་།` with no space, which is not a heading to any parser.

Real text edits are few: one text with 13 syllable-level changes
(`གསོལ་འདེབས་ལེའུ་བདུན་མ།`, `༴` shorthand expanded to `་གསོལ་བ་འདེབས༔`),
seven H1 punctuation/whitespace touches (`།` → `། །`), one whitespace
edit, one line-break move, and one frontmatter `title` that looks like a
paste error (`དམིགས་བརྩེ་མ།` glued in front of `སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ།`).

The live check also found one text whose backend content no longer equals
its source note: `རྟེན་འབྲེལ་བསྟོད་པ།` carries a stray `ˌ` (U+02CC) on the
backend that the vault repaired locally after upload. Resolve that text
separately; it is also the one with no live translations.

## 2. How the backend stores a text (what an update must respect)

- A **text** (`/v2/texts/{id}`) holds title, language, category, license,
  bdrc, date, contributions. Translations are separate texts linked by
  `translation_of`, settable only at creation.
- An **edition** holds `content` — one string, all lines concatenated with
  no separator — plus metadata (`type`, `source`, `colophon`,
  `incipit_title`). Everything else is an annotation over character spans
  of that string.
- The **segmentation** is one annotation per edition: segments, each with
  line spans, a `type` and a `reference` — the `reference` *is* the block
  id (`0`, `1`, `2-1`…). An edition may have at most one (`POST` answers
  409 "already has a segmentation").
- **Alignments** are relationships between `Segment` nodes of two editions,
  addressed by `reference`. `PUT` validates that every reference exists
  exactly once on each side. Because they hang off the segment nodes,
  **deleting a segmentation deletes every alignment on it** (`DETACH DELETE
  span, segment, segmentation`) with no warning. That is why a renumbered
  id is expensive: it forces the segmentation to be re-posted, which
  forces all six alignments to be re-PUT.
- A **table of contents** is another annotation: nested sections, each a
  `LocalizedString` title plus a character span. Several may exist per
  edition; there is no replace call, only add and delete. None of the 94
  has one today (the uploader never posted one).
- `PATCH …/content` applies **one** insert/delete/replace by character
  position and shifts every stored span itself (segment line spans, TOC
  spans, `content_length`). Spans that fall entirely inside a deleted or
  replaced range are dropped; a replace that covers several line spans
  collapses them into the first. Segment references are untouched, so
  alignments survive an in-place edit.

## 3. Endpoints — used, needed, missing

### 3.1 Used by the pipeline today

| call | script | purpose |
|---|---|---|
| `POST /v2/texts` | `upload_liturgy.py`, `upload_translations.py` | create text |
| `POST /v2/texts/{id}/editions` | same | create edition with content + segmentation in one body |
| `PUT /v2/editions/{src}/alignments/{tgt}` | `upload_translations.py` | replace the alignment pairs of a translation (idempotent) |
| `PATCH /v2/texts/{id}` | one-off, 2026-09-07 | re-title two translations |
| `POST /v2/languages` | one-off, 2026-09-07 | register `ne` |
| `DELETE /v2/texts/{id}`, `DELETE /v2/editions/{id}` | one-off, 2026-08-31 | retire a duplicate |
| `GET /v2/editions/{id}`, `…/content`, `…/segmentation/segments`, `…/alignments`, `GET /v2/texts/{id}` | verification, `inbox_diff.py --live` | read back |

### 3.2 Exist, not yet used, needed for updates

| call | needed for | notes |
|---|---|---|
| `PATCH /v2/editions/{id}/content` | the **patch** class (8 texts, 21 ops) and the content step of every rebuild | one op per request; positions refer to the live content at call time, so apply hunks back-to-front or re-GET between ops; `text` must be non-empty (a pure deletion is a `delete` op) |
| `DELETE /v2/editions/{id}/segmentation` | every **rebuild** | drops all alignments silently — snapshot `GET …/alignments` first |
| `POST /v2/editions/{id}/segmentation` | every rebuild | 409 unless deleted first |
| `GET /v2/editions/{id}/alignments` | every rebuild | lists the translation editions whose alignment has to be re-PUT |
| `PUT /v2/editions/{src}/alignments/{tgt}` | every rebuild × live translations | already scripted; needs pairs built from the *new* source references |
| `POST /v2/editions/{id}/table-of-contents`, `DELETE /v2/table-of-contents/{toc_id}` | the 54 texts that now carry `##` headings | the vendored parser has `build_toc`; `liturgy_payloads.py` does not emit it yet — a pipeline gap, not an API gap |
| `PATCH /v2/texts/{id}` | frontmatter `title`, `author`, `license`, `bdrc_work_id`, `date`, `category_id` | `alt_titles` and `contributions` too |

Order for a rebuild, per text (the order matters because content patches
re-shift whatever annotations still exist):

```
GET    /v2/editions/{ed}/alignments                 -> remember the 6 translation editions
DELETE /v2/table-of-contents/{toc}                  (only if one exists)
DELETE /v2/editions/{ed}/segmentation               (alignments go with it)
PATCH  /v2/editions/{ed}/content  {replace 0..len}  (or the per-hunk ops)
POST   /v2/editions/{ed}/segmentation
PUT    /v2/editions/{ed}/alignments/{tr}  × 6
POST   /v2/editions/{ed}/table-of-contents          (texts with headings)
```

Between the DELETE and the last PUT the library shows the text with no
translations. With 54 rebuilds that window is 54 × 9 requests long.

### 3.3 Missing — required for a clean in-place update, do not exist

1. **`PATCH /v2/editions/{id}`** — edition metadata (`source`, `type`,
   `colophon`, `incipit_title`) cannot be changed at all. Only `GET` and
   `DELETE` exist. Any expert edit to `source:` or `edition_type:` is
   unpushable today (none pending, but the gap is real).
2. **`PUT /v2/editions/{id}/segmentation`** — replace the segmentation in
   place, matching segments by `reference` and **keeping alignment
   relationships for references that still exist**. This is the single
   most valuable addition: with it, the 54 colophon-heading rebuilds would
   keep alignments for every block whose id survived, and a renumbered
   text would need one call instead of eight. Today `DELETE` + `POST` is
   the only route and it throws away all six alignments.
3. **`PUT /v2/editions/{id}/content`** (whole-document replace, ideally
   taking `content` + `segmentation` together, the same shape as
   `POST /v2/texts/{id}/editions`). Today the only way to replace the whole
   content is a `ReplaceOperation` over `0..len`, whose span-shifting logic
   is designed for small edits and collapses every span into the first —
   so the segmentation must be deleted before it, which is what makes the
   rebuild sequence nine calls long.
4. **Batched / atomic content operations** — `PATCH …/content` takes
   exactly one operation per request and offers no precondition (no
   `If-Match` on `content_length`). Thirteen hunks in one text are
   thirteen sequential requests, each shifting the positions of the next;
   a failure half-way leaves content and vault out of step with no
   rollback. A list of operations applied in one transaction, validated
   against the current length, would make the **patch** class safe.
5. **`PUT /v2/editions/{id}/table-of-contents`** — replace instead of
   delete + add. Minor; delete + add works.
6. Not needed for this update but known: `translation_of` is not in
   `TextPatch`, so a translation created against the wrong Tibetan text
   can only be deleted and re-created.

### 3.4 Not needed

Recordings, pagination, durchen, bibliographic, tags, persons, categories,
content-search: untouched by this update.

## 4. What the vault side must do before any of it is sent

- **Decide the title line.** If it is presentation, `block_ids.py` needs a
  documented rule to drop it at stamping (or the experts remove it); if it
  is text, every translation needs a matching first block or the new `^1`
  stays unaligned, and all 94 texts are rebuilds.
- **Alignment pairs after renumbering.** The vault's convention is that
  translation block `^N` renders source block `^N` (`translation_payloads.
  build_pairs` refuses anything else). A renumbered source therefore
  needs either the translation notes renumbered with the same map
  (old id → new id, derivable from `inbox_diff.py`'s unit pairing) or
  `build_pairs` extended to accept that map. The backend does not care
  which; it only sees reference pairs.
- **Emit a TOC payload** for texts with `##` headings
  (`liturgy_payloads.py` currently skips `build_toc`).
- **Fix the defects first**: `##མཇུག་བྱང་།` without a space in
  `གཏོར་མ་ཆ་གསུམ་བཞུགས་སོ།` (the stamper refuses the file), the stray
  block ids inside the inbox copy of `སློབ་དཔོན་ཐུགས་རྗེ་ཅན་…`, the three
  colophon-heading spellings, and the glued `title:` on
  `སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ།`.
- **Re-stamp, then re-verify**: `block_ids.py stamp --restamp`, `verify`,
  rebuild payloads, and only then an update script that follows §3.2 with
  a ledger written after every call, the way `upload_liturgy.py` does.
