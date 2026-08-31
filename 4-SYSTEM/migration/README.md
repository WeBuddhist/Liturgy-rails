# Liturgy ID map — old WeBuddhist MongoDB → new OpenPecha v2 backend

`liturgy-id-map.json` (full) and `liturgy-id-map.csv` (flat) map every liturgy
text in the old production database to the backend ids this vault's notes were
uploaded under.

## The two sides

**Old** — MongoDB cluster `webuddhist-prd`, database `webuddhist`, collection
`Text`, filtered to the Liturgy category (`_id 692876ae70bf66f003b07d6f`,
`pecha_collection_id dJpr4gMF72E4UpCnJ84sh`). 311 documents.
The stable identifier is `pecha_text_id`. Note that `Text._id` is a **UUID**,
and it is that UUID — not `pecha_text_id` — that `Segment.text_id` and
`TableOfContent.text_id` reference. Both are in the map (`old_pecha_text_id`,
`old_mongo_id`).

**New** — `text_id` + `edition_id` in the frontmatter of `1-SOURCES/Text/*.md`,
written when the notes were POSTed to `/v2/texts` and
`/v2/texts/{text_id}/editions`. 94 notes. Mirrored in
`4-SYSTEM/scripts/upload_ledger.json` (verified identical).

## How the join was made

Not by title. `1-SOURCES` was renamed to full titles and the Mongo titles carry
ornamental prefixes (`༄༅། །`, `༈`), so only 2 of 94 titles still match.

The join is on **content**: old segment text was rebuilt per `Text` document in
`TableOfContent` order, normalised (whitespace and Tibetan punctuation stripped),
and compared with each note body (frontmatter, headings and `^N` block ids
stripped).

Every result was cross-checked by a second, independent method — regex-probing
`Segment.content` for distinctive lines from each note. **The two methods agree
exactly**: all 86 mapped notes score ≥0.80 content similarity, and all 8
unmapped notes score <0.50 *and* return zero segment hits anywhere in the
database — not just in the Liturgy category.

> If you re-run the matcher, pass `autojunk=False` to `difflib.SequenceMatcher`.
> Its default junk heuristic discards characters appearing in >1% of a sequence
> longer than 200 chars, which for punctuation-stripped Tibetan is most of the
> alphabet, and it silently produces ratios near 0.01 for identical texts.

## What the three sections mean

| Section | Count | Meaning |
|---|---|---|
| `mapped` | 86 | Old text ⇄ new text. Migrate the id. |
| `new_only` | 8 | In the new backend, absent from the old database. Nothing to migrate; the old side has no record. |
| `old_only` | 139 | In the old database, no counterpart in this vault. **Decide before cutover**: 108 are published and 41 were in the original OpenPecha 100-text catalog. |

`311 = 86 mapped + 86 group siblings + 139 old-only.`

## Group siblings

Each mapped old text sits in a `group_id` with its other language versions —
phonetic transcriptions (`tibphono`), transliteration (`tib`), and translations
(`en`, `zh`, `lzh`). 86 such siblings hang off the 86 mapped texts and are listed
per row in `old_group_siblings`.

These have **no id on the new side**. The new backend carries its own English and
Chinese tracks under `3-TRANSFORMATIONS/Translations/`, which are DharmaMitra
machine baselines, not these. Migrating or retiring the old siblings is a
separate decision from the text mapping.

## Confidence values

| `match_method` | n | |
|---|---|---|
| `content-identical` | 15 | normalised content byte-identical |
| `content-near-identical` | 69 | ≥0.95 — whitespace/spelling level |
| `content-variant` | 2 | 0.80–0.95 — same work, minor textual differences |

The 2 variants (`content_divergent: true`) are `བསྟན་འབར་མ་བཞུགས་སོ།` (0.91) and
`སངས་རྒྱས་ཆོས་ཚོགས་མ།` (0.94). Both are the same work; worth a glance before cutover.
