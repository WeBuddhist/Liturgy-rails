# 3-TRANSFORMATIONS — Prescriptive outputs

This folder holds the **generated outputs** of the vault, and the per-track
files that prescribe how each output is produced. Where `2-RAILS/` records
what the tradition *says*, this folder records what *one particular output*
does with it: this audience, this register, this locked vocabulary, this
calendar.

---

## Status: not yet built

No transformation tracks exist yet. The upload of `1-SOURCES/` to the
WeBuddhist library is the vault's current work; transformations come after.

## The three categories

Each category is a subfolder; each transformation within it is a **track** —
one coherent output stream with one set of choices, governed by:

- **`requirements.md`** — the style contract (audience, register,
  transliteration policy, which rails it depends on).
- **`termbase.md`** — the vocabulary contract: one chosen rendering per
  term, selected from the attested options in `2-RAILS/`.

### `Translations/`
One target language, one register, one audience. For liturgy the register
question is unusually sharp: a translation meant to be *chanted aloud* has
metre and breath constraints that a study translation does not, so those
belong in the track's `requirements.md` rather than being decided per text.

### `Adaptations/`
Same language, different format — a practice booklet for a specific
ceremony, an abbreviated daily-recitation set, an annotated edition for
beginners, a phonetic transliteration for non-Tibetan-reading practitioners.

### `Plans/`
Calendar-paced outputs — a daily recitation cycle, a text-per-week study
arc, a set keyed to the Tibetan ritual calendar (tsechu, full-moon days,
Losar).

## Rules

- Tracks cite `2-RAILS/`; they never reach past the rails into
  `1-SOURCES/` for interpretive decisions (they may quote the source text
  itself, which is what they are transforming).
- A new keyword rendering chosen by a track is recorded back into
  `2-RAILS/` as one more attested option, alongside every other
  translator's choice.
- Nothing here is authoritative until a human reviewer signs it off.
