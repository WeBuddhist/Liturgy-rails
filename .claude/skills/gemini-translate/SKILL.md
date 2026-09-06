---
name: gemini-translate
description: Produce a zero-shot, block-ID-aligned machine-baseline translation of a Tibetan source text into a new display language (Hindi, Nepali, Mongolian, Vietnamese, …) by calling Google Gemini on small batches of adjacent blocks under a JSON line schema, enforcing one target line per Tibetan line, and writing the result to its own track under 3-TRANSFORMATIONS/Translations/Gemini/<tag>/ — the same track shape as the DharmaMitra skill, so stamping and upload work unchanged. Use when asked to translate the liturgy corpus into a language DharmaMitra does not cover, to pilot a new language, or to run/resume/repair a Gemini track.
---

# gemini-translate

The sibling of `dharmamitra-translate` for languages DharmaMitra's `cat-translate` endpoint does not serve well or at all. It reuses that skill's parser, context builder and renderer (`dm_translate.py` is imported, not copied), keeps the same per-text append-only ledger and the same track layout, and therefore produces files that `stamp_metadata.py`, `translation_payloads.py` and `upload_translations.py` already understand. Two things are different, and both are the point:

- **Transport.** Gemini is asked for a JSON object holding one array of lines per block, under a response schema. No `[[n]]` marker protocol: the response is split by block *and by line* without guessing.
- **Line parity is enforced, not hoped for.** Every block's line count is checked against its source before it is recorded. A wrong count triggers a solo re-run with the required count stated (up to `--parity-attempts`, default 3). Only an exact match is accepted silently; anything still divergent is recorded with `line_parity: false` and listed in the run report.

The output is a **machine baseline**: `track_type: machine-baseline`, `rails_used: none`, `status: draft`, never cited by any other `3-TRANSFORMATIONS/` output, never promoted past draft by an LLM. It is a first display translation for the app and a drafting aid, nothing more.

---

## Source language and provenance — read this first

**The source is always the Tibetan in `1-SOURCES/Text/`.** It is the closest thing to the original that exists, so `translation_of`, `translation_of_text_id` and the segment alignment always point at the Tibetan text, and block `^N` of the output renders block `^N` of the Tibetan.

An existing machine translation may be threaded into the prompt as **reference** with `--reference-track <folder>` (e.g. the DharmaMitra English track). That helps the model disambiguate Tibetan syntax and keeps terminology consistent, and it is recorded on every ledger record (`reference_used`) and in the frontmatter (`reference_translation`), but it is context, not source: `translation_of` does not change. **Default is no reference** — a true zero-shot from the Tibetan. Decide per language after the pilot, and record the decision in the track's `about.md`.

If a language is ever translated *from* the English instead (a pivot), that is a **different track** whose `translation_of` points at the English translation's own `text_id`, and the upload must say so. This skill does not do that; do not fake it by pointing a Gemini track at the Tibetan while feeding it only English.

## Inputs

| Input | Description | Required |
|---|---|---|
| **Source file** | A block-ID'd note under `1-SOURCES/Text/`. Blocks without ` ^<id>` are skipped; headings are never sent. | yes |
| **Target language** | A language **label** (`hindi`, `nepali`, `mongolian`, `vietnamese`), not an ISO code. The tag (`hi`, `ne`, `mn`, `vi`) comes from the label table or `--lang-tag`. | yes |
| **Model** | `--model`, default `gemini-3.1-pro-preview`. `--thinking low|medium|high` (default: the model's default). Temperature is left at the model default unless `--temperature` is given — Google's guidance for Gemini 3. | no |
| **Style instruction** | `<track>/style.md`, seeded per language on first run (see below) and read back **verbatim** thereafter as the system prompt, followed by the fixed output contract. Edit the file, never the script. | no |
| **Context header** | `<track>/context-header.md`, a work-NEUTRAL preamble. The per-text `Work: <Tibetan title> (<English title>), author: …` line is derived from each source and appended at call time. | no |
| **Reference track** | `--reference-track`, see above. | no |
| **Glossary** | `<track>/glossary.tsv` (auto-loaded when present) or `--glossary`: `Tibetan term<TAB>rendering` lines; entries whose term occurs in the batch join that call's context as fixed terminology. This is how a recurring term-level error found in review is fixed without touching the style prompt. | no |

## Output

```
3-TRANSFORMATIONS/Translations/Gemini/<tag>/
├── about.md                  # what this track is and is not (seeded)
├── style.md                  # system prompt, verbatim (seeded, editable)
├── context-header.md         # work-neutral preamble (seeded, editable)
├── glossary.tsv              # optional fixed terminology, auto-loaded
├── pilot-review.md           # the pilot's block-by-block review
├── <text>-<tag>.md           # rendered, block-ID aligned, source quoted above each block
└── work/
    ├── <text>-<tag>.jsonl    # append-only ledger, one record per block
    └── _corpus-run-*.json    # per-run report from gm_corpus.py
```

Ledger records carry the DharmaMitra fields (`block_id`, `heading`, `source`, `translation`, `style_instruction`, `context`, `endpoint`, `batch_size`, `batch_block_ids`, `batch_fallback`, `elapsed_s`, `ts`) plus `model`, `model_version`, `thinking`, `temperature`, `line_parity`, `parity_attempts`, `reference_used` and token `usage`. The frontmatter adds `model`, `thinking`, `temperature`, `response_format`, `reference_translation` and `line_parity_failures`, and its `generator` is the model version that actually answered.

### Seeded style per language

| tag | Script and vocabulary the seed asks for | Mantras | Names |
|---|---|---|---|
| `hi` | Devanagari; Sanskrit-derived Hindi Buddhist vocabulary | Devanagari transliteration of the Sanskrit | Sanskrit names in Devanagari; Tibetan names transliterated |
| `ne` | Devanagari, standard Nepali (not Hindi); Nepal's Buddhist usage | Devanagari | as Hindi, plus forms current in Nepal (गुरु रिन्पोछे, लामा) |
| `mn` | Cyrillic, Khalkha; the Tibetan-derived Mongolian Buddhist lexicon (лагшин, ядам, бодь сэтгэл, буян, зориулга) | Cyrillic as recited (Ум мани бадмэ хум) | established Mongolian deity names (Дарь эх, Жанрайсиг, Манзушир, Очирваань) |
| `vi` | Vietnamese with diacritics; Sino-Vietnamese Buddhist vocabulary | romanized Sanskrit (Om Mani Padme Hum) | established Vietnamese forms (Quán Thế Âm, Văn Thù, Liên Hoa Sanh) |

These are starting points. The pilot exists to correct them; edit `style.md` and re-run the pilot blocks with `--force`.

---

## Rules

1. **Never write to `1-SOURCES/`.** The only exception is the title registry (`1-SOURCES/liturgy-titles.json`) written by `gm_titles.py`, and `stamp_metadata.py --source-titles`, both run from the main session only.
2. **Never write into an existing non-baseline track.** The script refuses a folder that holds a `file_type: translation` file without `track_type: machine-baseline`.
3. **Never guess a split.** A response whose ids or shape do not match the batch is discarded and the batch is re-run one block per call. A block whose line count is wrong is re-run alone. Line parity failures are reported, never padded or trimmed by hand.
4. **Every source block ID appears exactly once in the output**, in source order, unaltered.
5. **Source is the Tibetan.** See the provenance section. A reference track is context and is recorded as such.
6. **The ledger is append-only.** To change a rendering, edit `style.md` and re-run the block with `--force --only <id>`; the newer record supersedes at render time.
7. **Re-stamp after every run.** The renderer rebuilds frontmatter from the ledger and knows nothing about backend ids, provenance keys or researched titles. `gm_corpus.py` does this itself for its track; after a manual `gm_translate.py` run do it by hand:
   ```bash
   python3 4-SYSTEM/scripts/stamp_metadata.py --ids --track-meta --titles --track 3-TRANSFORMATIONS/Translations/Gemini/<tag>
   ```
   Use `--track` when other tracks are being written concurrently; the passes that touch `1-SOURCES/` (`--source-titles`, `--authors`) run in the main session only.
8. **Two blocks per track may legitimately differ in line count.** Where a text opens with the `རྒྱ་གར་སྐད་དུ། … བོད་སྐད་དུ།` title formula, the stamp pass replaces that block's rendering with the researched title. Do not "fix" those by re-translating (`བྱམས་པའི་སྨོན་ལམ།` `^1`, `འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་རྒྱལ་པོ།` `^1`).
9. **Rate limits are handled, quotas are not fought.** 429s back off (Retry-After, else 10 s → 180 s); a 429 naming a per-day quota aborts the run at once. The ledger makes any re-run a resume.
10. **Report a partial run as partial.** The frontmatter's `blocks_translated` / `blocks_total` must match reality, and the report must list every block without line parity and every block with no usable response.
11. **Wrathful and exorcistic texts are liturgy.** Safety thresholds are set to `BLOCK_NONE`; a `finishReason` other than `STOP` is treated as a failed call, retried singly, and reported if it still fails — never silently skipped.

---

## Procedure

Scripts live in `.claude/skills/gemini-translate/scripts/`. All commands run from the vault root with `GEMINI_API_KEY` in the environment (`source ~/.zshrc`).

### Step 1 — Confirm inputs, spend nothing

```bash
python3 .claude/skills/gemini-translate/scripts/gm_translate.py --source "1-SOURCES/Text/<text>.md" --list
python3 .claude/skills/gemini-translate/scripts/gm_translate.py --source "1-SOURCES/Text/<text>.md" --lang <label> --limit 3 --dry-run
```

`--list` parses only. `--dry-run` prints the exact request bodies (system prompt, context, JSON blocks) so the style and the `Work:` line can be read before a call is made. Confirm the language label if the user did not state one.

### Step 2 — Pilot one or two texts per language

Pick texts a reviewer can judge: well known, with published translations in the target language, with at least one mantra and one colophon between them. For this corpus the pilot pair is `བློ་སྦྱོང་ཚིག་བརྒྱད་མ།` (Eight Verses, 10 blocks) and `སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ།` (Twenty-One Tārās, 29 blocks, mantra).

```bash
python3 .claude/skills/gemini-translate/scripts/gm_titles.py --lang <label> --only "བློ་སྦྱོང་ཚིག་བརྒྱད་མ,སྒྲོལ་མ་ཉེར་གཅིག"
python3 .claude/skills/gemini-translate/scripts/gm_corpus.py --lang <label> --only "བློ་སྦྱོང་ཚིག་བརྒྱད་མ"
python3 .claude/skills/gemini-translate/scripts/gm_corpus.py --lang <label> --only "སྒྲོལ་མ་ཉེར་གཅིག"
```

Read the rendered files back and check, block by block against the Tibetan (and against the DharmaMitra English as a sanity reference):

- line parity: every block's line count equals its source's (the report says so; verify one or two by eye anyway)
- script: the right script throughout, no stray Latin/Chinese/Tibetan, no transliteration in brackets
- mantras: transliterated as the style asks, never translated, never dropped
- names: the established target-language form where one exists, transliterated otherwise, consistent across the text
- register: recitable, devotional, natural word order; no calques, no added honorifics or glosses
- fidelity: no omitted or invented clauses; imperatives/optatives (`ཤོག`, `གྱུར་ཅིག`) rendered as aspirations, not statements
- consistency: the same Tibetan term rendered the same way across blocks

Write the findings to `<track>/pilot-review.md`. Sort each finding by kind: a **systematic** defect (wrong script, mantras translated, register wrong throughout) means editing `<track>/style.md`; a **recurring term-level** error (one Tibetan term consistently mis-rendered, mantra syllables spelled inconsistently) means a line in `<track>/glossary.tsv`; an isolated wording slip is reported and left. After either edit re-run the affected blocks with `--force --only <ids>` (or the whole pilot text) and confirm the fix took; iterate here, on 39 blocks, not on 1 900.

### Step 3 — Titles for the whole corpus

```bash
python3 .claude/skills/gemini-translate/scripts/gm_titles.py --lang <label>
```

Writes `<tag>_title` (plus `_attested: false`, `_alt`, `_method`, `_note`) for every text lacking one. The prompt asks for the **display form** an ordinary reader of the app recognises — an established published title where one exists, otherwise plain natural wording — and parks classical or Sanskritic calques in `_alt`. A title marked `<tag>_attested: true` is never overwritten, not even with `--force`; when a reviewer finds the real published title, set it in the registry by hand with its URL. Run in the **main session**, one language at a time — the registry is one file. Then `stamp_metadata.py --source-titles` to put `title_<tag>` on the source notes, also from the main session.

### Step 4 — Run the corpus

```bash
python3 .claude/skills/gemini-translate/scripts/gm_corpus.py --lang <label>
```

One language per process; the four languages may run in parallel because each track is its own folder. Resumable: blocks already in a ledger are skipped. The driver re-stamps its own track when it finishes and writes `work/_corpus-run-<ts>.json`.

**A full run takes hours, and a shell started from a tool call is killed after about an hour** (observed 2026-09-06: every driver run from an agent's background Bash died at ~61 min with no STOPPED line). Start the drivers detached instead:

```bash
source ~/.zshrc; python3 .claude/skills/gemini-translate/scripts/gm_launch.py            # all four
pgrep -fl "gm_corpus.py --lang"                                                            # who is running
tail -2 3-TRANSFORMATIONS/Translations/Gemini/<tag>/work/_corpus-run.log                   # progress
```

`gm_launch.py` starts each driver in its own session (macOS has no `setsid`), refuses to start a second driver for a language that already has one, and appends to `work/_corpus-run.log`. A killed driver loses at most the call in flight; relaunching resumes. Wait for the exits with a `Monitor` that watches `pgrep` (not with a background shell, which has the same one-hour cap).

When delegating, use subagents for the **verification and spot-reading** after the run (one language each, Sonnet), not for babysitting the driver: give them the track folder, the checks in Step 5, and the instruction to report numbers and block ids. Gemini does the translating.

### Step 4b — Pin proper names, then re-run the drift

Spot-reading the first full run found the content sound but recurring names spelled several ways across blocks (Hindi Oḍḍiyāna six ways; Nepali Thötreng Tsal three ways; Vietnamese lineage names once as raw Wylie). Names are the one thing a zero-shot run cannot keep stable on its own, so the skill pins them:

```bash
python3 .claude/skills/gemini-translate/scripts/gm_names.py --lang <label> --propose   # 1 call: one spelling per name -> <track>/glossary.tsv
python3 .claude/skills/gemini-translate/scripts/gm_names.py --lang <label> --check     # no calls: blocks whose rendering lacks the pinned form
python3 .claude/skills/gemini-translate/scripts/gm_names.py --lang <label> --rerun     # re-translate exactly those blocks with the glossary in context, re-stamp, re-check
```

The proposal is the model's reading of the track's own `style.md`; read it before `--rerun` and override by hand where the track already uses a settled form (the Vietnamese track says Độ Mẫu for Tārā, so its glossary was edited to keep that). `--rerun` reports the residue afterwards; a few blocks may still drift and are listed, not hidden. Expect roughly a third of name occurrences to need a re-run on a first-pass track.

### Step 5 — Verify

```bash
python3 .claude/skills/gemini-translate/scripts/gm_verify.py --lang-tag <tag>
```

One script, no API calls: the last corpus report, every ledger's parity flags, every rendered file's counts/title/site, block ids against the Tibetan one for one, and a scan for Tibetan or CJK characters inside translation lines. Exit 0 means the track is whole. The same checks, spelled out for doing by hand:

1. `blocks_translated == blocks_total` in every file, or say which fall short:
   ```bash
   grep -L '^blocks_translated: \([0-9]*\)$' 3-TRANSFORMATIONS/Translations/Gemini/<tag>/*.md
   python3 - <<'EOF'
   import re,glob
   for f in sorted(glob.glob('3-TRANSFORMATIONS/Translations/Gemini/<tag>/*.md')):
       t=open(f).read(); a=re.search(r'^blocks_translated: (\d+)',t,re.M); b=re.search(r'^blocks_total: (\d+)',t,re.M)
       if a and b and a.group(1)!=b.group(1): print(f, a.group(1), '/', b.group(1))
   EOF
   ```
2. Block ids match the source one-for-one:
   ```bash
   diff <(grep -o '\^[A-Za-z0-9-]*$' "1-SOURCES/Text/<text>.md") <(grep -o '\^[A-Za-z0-9-]*$' "3-TRANSFORMATIONS/Translations/Gemini/<tag>/<text>-<tag>.md")
   ```
3. No `*[not yet translated]*` left; `line_parity_failures: 0` in the frontmatter, or the listed blocks reviewed.
4. `title_translated` present in every file (the stamp ran and the registry had the title).

### Step 6 — Upload (separate decision, main session)

The backend must know the language first: `GET /v2/languages` lists `hi`, `mn`, `vi` but **not `ne`** as of 2026-09-06, so Nepali needs a `POST /v2/languages {code: "ne", name: "nepali"}` before its texts can be created. Then the existing path applies unchanged:

```bash
python3 4-SYSTEM/scripts/translation_payloads.py --category-id <ID> --out-dir 4-SYSTEM/scripts/payloads-translations "3-TRANSFORMATIONS/Translations/Gemini/<tag>/"*-<tag>.md
set -a; source 4-SYSTEM/scripts/.env.local; set +a
python3 4-SYSTEM/scripts/upload_translations.py --payloads 4-SYSTEM/scripts/payloads-translations --dry-run
```

`translation_of` is the Tibetan `text_id`; the alignment is block-id parity. Uploading is outward-facing: confirm with the user before the non-dry run.

---

## Completion check

- [ ] Target language stated or confirmed; tag matches the backend's language code
- [ ] `--dry-run` request read once; `Work:` line names the text being translated
- [ ] Pilot texts read back block by block; `pilot-review.md` written; `style.md` adjusted if needed
- [ ] `<tag>_title` present in the registry for every text; `--source-titles` run from the main session
- [ ] Corpus run report: every text `blocks_done == blocks_total`, parity failures listed, failed blocks listed, not stopped early
- [ ] Names pinned (`gm_names.py --propose`, proposal read and overridden where the track already has a settled form), drift re-run, residue listed
- [ ] `gm_verify.py --lang-tag <tag>` exits 0; `about.md` carries the run history
- [ ] Every source block ID appears exactly once in every rendered file, in source order
- [ ] Track re-stamped (`--ids --track-meta --titles --track <track>`); `title_translated` present
- [ ] Frontmatter carries `track_type: machine-baseline`, `rails_used: none`, `status: draft`, and names the model version that answered
- [ ] Nothing under `1-SOURCES/` (other than the title registry / `title_<tag>` keys), `2-RAILS/`, or any other track was modified
