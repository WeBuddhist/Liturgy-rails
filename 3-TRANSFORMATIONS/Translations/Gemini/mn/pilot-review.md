# Gemini/mn pilot review — 2026-09-06

Pilot texts: `བློ་སྦྱོང་ཚིག་བརྒྱད་མ།` (Eight Verses of Mind Training) and `སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ།` (Praises to the Twenty-One Tārās). Model `gemini-3.1-pro-preview`, no reference track, no glossary.

## Run summary

| Text | Blocks done/total | Calls | Parity failures | Failed blocks | Stopped |
|---|---|---|---|---|---|
| བློ་སྦྱོང་ཚིག་བརྒྱད་མ། | 10/10 | 2 | 0 | 0 | no |
| སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ། | 29/29 | 4 | 0 | 0 | no |

Both runs completed in one pass, no re-runs needed, no 429s. `stamp_metadata.py` track-only passes (`--ids --track-meta --titles`) ran automatically after each and updated both files.

## Parity tables (verified independently, not just from the driver report)

**བློ་སྦྱོང་ཚིག་བརྒྱད་མ།** — every content block (`^1`–`^10`) has Mongolian line count == Tibetan line count (1, then eight blocks of 4, then 1). `^0` is the H1 heading, not a content block.

**སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ།** — every block `^1`–`^29` matches exactly: `^1`=2, `^2`=1, `^3`–`^22`=4 each, `^23`=6, `^24`–`^27`=4 each, `^28`=6, `^29`=1. `^0` is the H1 heading.

No padding, no trimming, no dropped or duplicated block IDs in either file.

## Findings by criterion

**1. Line parity** — clean in both texts, confirmed by independent script, not just the driver's self-report.

**2. Script** — Cyrillic throughout in every translation line of both files; a character-by-character scan of every non-quote, non-heading line found zero non-Cyrillic, non-digit characters. No traditional Mongolian script, no stray Latin/Chinese/Tibetan leaked into any rendered line. (Quoted Tibetan `>` source lines are of course Tibetan, as intended — that's the source citation, not the translation.)

**3. Mantras/dhāraṇīs — the one real issue found.** Unlike a text with one dedicated mantra line, this Tārā praise embeds the seed-syllables of *oṃ tāre tuttāre ture svāhā* one or two at a time inside each homage verse ("Homage to the letters tuttāra hūṃ...", "Homage to trad and phaṭ...", "Homage to ture..."). Gemini transliterated these but was **inconsistent with itself**, and mostly diverges from the living Mongolian recitation form (confirmed by web search: Mongolian practitioners write this mantra "Ум дарэ дүдарэ дүрэ суухаа" / "...дүри суха"):

  | Syllable | Attested Mongolian form | Blocks in this file | What was rendered |
  |---|---|---|---|
  | tāre/tāra | дарэ | `^20` | Дара |
  | tuttāre/tuttāra | дүдарэ | `^7`, `^12`, `^22` | Туддара (`^7`) vs Дуддара (`^12`, `^22`) — inconsistent with itself |
  | ture | дүрэ | `^10`, `^19`, `^23` | Дүрэ (`^10`, matches) vs Дурэ (`^19`, `^23`, doesn't) |
  | phaṭ | (пад/фад, either heard) | `^9`, `^20` | Пад (`^9`) vs Фад (`^20`) — inconsistent with itself |
  | svāhā | суха | `^17` | Сууха |

  This is confined to these embedded seed-syllables — it does not affect the deity names, the homage refrain, or general vocabulary — and it is a narrow, mechanically-fixable issue (a glossary entry for this one mantra, or a worked example added to `style.md`), not a wrong-script or translated-mantra defect. **Not treated as grounds for a style.md rewrite**, but should be fixed (e.g. via a glossary) before this text is run for real, and watched for in any other text that scatters mantra syllables through verse rather than giving one mantra line.

**4. Names and terms** — `Дарь эх` (Tārā) used consistently in both files, title through colophon. In the Tārā text the model correctly supplied established Mongolian deity names that were **not** in the style seed list: `Хурмаст` (Indra, བརྒྱ་བྱིན), `Эсрүн` (Brahma, ཚངས་པ), consistent with real Mongolian Buddhist usage — a good sign the underlying knowledge is sound, not just pattern-matching the seed. `Ланританба Доржсэнгэ` (Langri Thangpa Dorje Senge) and `Гаадамбын` (Kadampa) in the Eight Verses colophon (`^10`) follow the traditional Mongolian convention of rendering Tibetan unaspirated `ka`/`ta` with `г`/`д` (the same convention that gives classical Mongolian `Гагьу` for bKa'-brgyud, `Гармаба` for Karmapa) — plausible, not an error.

**5. Register** — devotional, recitable, verb-final word order throughout; no added honorifics or glosses; no editorializing. One found match to living practice: block `^28`'s "Хоёр, гурав, долоонтоо" (two, three, or seven times) for `གཉིས་གསུམ་བདུན་དུ`, which is exactly the phrasing used in a Mongolian Buddhist source describing this same recitation practice (buddhism.mn) — a strong sign the register lands correctly for a real audience.

**6. Fidelity** — no omitted or invented clauses found in either text against the Tibetan or the DharmaMitra English baseline. Optatives (`ཤོག`, `གྱུར་ཅིག`) are consistently rendered as wishes with `болтугай` in the Eight Verses text (`^2`–`^9`), never as flat statements. One recurring mistranslation found: `མ་ལུས་` ("without exception/remainder") is rendered `мадаггүй` in the Tārā text at `^6`, `^10`, `^11`, `^20` — `мадаг` is a real Mongolian word but means "mistake/flaw," so `мадаггүй` means "flawless/without error," not "without exception." Confirmed consistent (same wrong word every time), so it reads as one term-level error to fix, not four separate wording slips — a candidate for a glossary entry (`མ་ལུས་` → `үлдэлгүйгээр`/`бүгдийг`) rather than a style.md change, since it is one specific phrase, not a register-wide problem.

**7. Consistency** — the 21 homage verses (`^3`–`^23`) **all** open with `Мөргөмүй` for `ཕྱག་འཚལ`, with no variation — good. The two consistency problems found are the mantra-syllable spellings (§3) and the `мадаггүй` mistranslation (§6), both listed above with block ids.

**8. Title verdict.**
- **Eight Verses** — stamped title `Оюун судлах найман бадагт` (registry `mn_title`). Web search for the real Mongolian Buddhist usage of this exact text (studybuddhism.com/mn, FPMT Mongolia, and the Dalai Lama's own Mongolian-language site all use it) turned up the actual attested title: **`Оюун судлахуйн найман шад шүлэг`** (or the shortened `Оюун судлахуйн найман шүлэг`). The registry's `судлах` root is right, but neither the stamped title nor either `mn_alt` entry (`Оюун судлах найман мөрт`, `Оюуныг судлах найман бадагт`) matches this attested real-world form — all three use `бадаг`/`мөрт` (stanza/line) where actual usage says `шүлэг` (verse/poem), and the genitive `судлахуйн` construction rather than bare `судлах`. Per the hard rules this registry entry was **not** edited; flagging it here for a future correction pass with the attested source noted.
- **Twenty-One Tārās** — stamped title `Хорин нэгэн Дарь эхийн магтаал`. Web search corroborates `магтаал` as the correct genre word in real Mongolian Buddhist usage (buddhism.mn: "Хорин нэгэн дарь эхийн ачлал" and other sources use `магтаал`/`мөргөлт магтаал` for this text), and the registry's own note calls this "the highly established traditional title in Mongolia." No better form was found among the `mn_alt` entries or in search; this title is fine as stamped.

## Was style.md changed?

**No.** Every issue found (§3 mantra-syllable spelling, §6 `мадаггүй`) is a narrow, specific, recurring-term problem best fixed with a glossary entry, not a defect in script, register, mantra-vs-translation handling, or overall terminology — the bar in the task for editing `style.md` and re-running. `style.md` is unchanged from its seeded form.

## Recommendation

**READY FOR FULL RUN**, with two follow-up items to fix via glossary (not style.md) at some point before or after the corpus run, since neither blocks correctness of the current pilot output:
1. `མ་ལུས་` should map to `үлдэлгүйгээр`/`бүгдийг` ("without exception"), not `мадаггүй` ("flawless").
2. The scattered *tāre/tuttāre/ture/phaṭ/svāhā* mantra syllables (when a text weaves them through verse rather than giving one mantra line) should map consistently to the attested recitation forms `дарэ`/`дүдарэ`/`дүрэ`/`пад`/`суха`.
