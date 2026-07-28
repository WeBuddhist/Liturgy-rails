# 2-RAILS — Descriptive interpretive layer

This folder distills the material in `1-SOURCES/` into **original-language
descriptive context** at every level a transformation might need. Every
claim cites a specific source (a text file, a segment). The authority of a
rail comes from the tradition it compiles, not from the LLM that compiled
it.

Rails *describe* what the sources say. They do not *prescribe* how a
particular output should be made — that is `3-TRANSFORMATIONS/`.

---

## Status: not yet built

`1-SOURCES/` is populated and upload-ready; no rails have been laid yet.
This file records what belongs here so the first rail lands in the right
shape.

## What belongs here for a liturgy corpus

The rails a liturgy corpus needs differ from a single-treatise vault like
`bodhisattvacaryāvatāra-rails`, where the unit of work is a verse of one
long text. Here the corpus is 100 short, independent, *performed* texts,
so the useful descriptive units are:

- **`Texts/`** — one package per liturgy: what it is, which tradition and
  lineage recite it, its ritual function (refuge, offering, praise,
  aspiration, dedication, protection), when it is recited (daily practice,
  specific dates, life-cycle events), and what it is usually recited
  alongside. This is the rail most transformations will need first.
- **`Sections/`** — for the longer, multi-part ritual texts: what each
  section does within the rite, and which sections are commonly omitted in
  abbreviated recitation.
- **`Local-Wiki/`** — per-term articles for the recurring vocabulary of
  liturgy (deity names, ritual implements, formulaic phrases such as
  ཕྱག་འཚལ་ལོ།, བཞུགས་སོ།, སྭཱ་ཧཱ།). Liturgical formulae repeat heavily
  across the corpus, so a term article is amortised over many texts.
- **`Bilingual-Glossaries/`** — attested renderings per term, per target
  language, drawn from existing published translations of these liturgies.
- **`termbases/`** — the consolidated per-language term inventories that
  transformation tracks draw their locked choices from.

## Rules

- Every rail cites the `1-SOURCES/` file and segment it derives from.
- Rails are descriptive: record what is attested, including disagreement
  between traditions, rather than choosing one reading.
- A rail is not authoritative until a human reviewer marks it `complete`.
- Rails never reach past `1-SOURCES/` into the raw `0-INBOX/` intake.
