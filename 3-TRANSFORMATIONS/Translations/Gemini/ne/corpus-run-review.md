# Nepali machine-baseline corpus review

Spot-check of the finished full-corpus Gemini Nepali run (`3-TRANSFORMATIONS/Translations/Gemini/ne/`) against the Tibetan source and the DharmaMitra English baseline, on three texts not seen in the earlier pilot (pilot covered `བློ་སྦྱོང་ཚིག་བརྒྱད་མ།` and `སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ།`).

## Deterministic numbers (from the main session's automated pass)

- 94 files, 1892/1892 blocks translated
- 191 Gemini calls in the final run
- 0 blocks without line parity
- 0 failed blocks
- 0 block-id mismatches against the Tibetan
- Researched titles stamped on every file
- Known blemish (already being fixed separately, not re-reported here): 4 lines carried the Tibetan `༈` ornament into the Nepali line before an exclamation — 3 in `གསོལ་འདེབས་ལེའུ་བདུན་མ།` (blocks ^5, ^83, ^104), 1 in `བླ་མ་རྒྱང་འབོད་མོས་གུས་སྙིང་གི་གཟེར་འདེབས་བཞུགས་སོ།`

## Texts read block-by-block for this review

1. `གསོལ་འདེབས་ལེའུ་བདུན་མ།-ne.md` — 131/131 blocks, read in full
2. `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།-ne.md` — 24/24 blocks, read in full (mantra-bearing text)
3. `ཚད་མེད་བཞི།-ne.md` — 1/1 block, read in full (short text)

## Findings by criterion

**Hindi forms instead of Nepali.** None found. Verb endings, postpositions and honorifics are consistently Nepali register throughout all three texts (e.g. `गर्दछु`, `भएका`, `हुनुभयो`, `गर्नुहोस्`, `होऊन्`). A grep for common Hindi markers (है/हैं/था/थी/के लिए/करता है/किया है/आपको) across all three files returned zero hits.

**Wrong script or stray Latin/Tibetan/Chinese.** None found. A grep for CJK codepoints and for stray Latin runs (outside the expected YAML frontmatter and the `> [!warning]` boilerplate) returned nothing in the translated body text of any of the three files.

**Mantras/dhāraṇīs translated instead of transliterated.** Handled correctly, and this is where it mattered most: `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` is built around the eight-syllable Guru mantra `ཨོཾ་ཨཱཿཧཱུྃ་བཛྲ་གུ་རུ་པདྨ་སིདྡྷི་ཧཱུྃ༔`, repeated at the end of every refrain block (^1–^24, 12 occurrences). Every occurrence is rendered identically as the Devanagari transliteration `ॐ आः हूँ वज्र गुरु पद्म सिद्धि हूँ`, never translated. The extended closing mantra in block ^24 (`...བཛྲ་ཐོད་ཕྲེང་རྩལ་བཛྲ་ས་མ་ཡ་ཛཿསིདྡྷི་ཕ་ལ་ཧཱུྃ་ཨཱ༔`) is likewise transliterated syllable-by-syllable (`वज्र थोदफ्रेङ् त्सल वज्र समय जः सिद्धि फल हूँ आः`). In `གསོལ་འདེབས་ལེའུ་བདུན་མ།`, the single-syllable exclamation `ཧཱུྃ༔` (blocks ^36, ^53) is transliterated as `हूँ`, not translated.

**Names of buddhas/deities inconsistent across blocks — real, systematic, confined to `གསོལ་འདེབས་ལེའུ་བདུན་མ།`** (the longest text, which enumerates many epithets of Guru Rinpoche and other figures repeatedly). Three separate name-consistency slips, all against a *stable* Tibetan spelling (so this is a target-side inconsistency, not something inherited from source spelling variation):
- **Oḍḍiyāna/Orgyen** — source spells it `ཨུ་རྒྱན` every time. Rendered `उर्ग्येन` in blocks ^32, ^37, ^93, but `उग्येन` in the repeating refrain of blocks ^114–^131 (18 occurrences). Two spellings for one place name.
- **Guru Rinpoche's secret name, Dorje Thötreng Tsal** (`རྡོ་རྗེ་ཐོད་འཕྲེང་རྩལ` / `པདྨ་ཐོད་འཕྲེང་རྩལ`) — three different Nepali spellings across three blocks: `थोत्रेङ त्सल` (^54), `थोथ्रेङ त्सल` (^70), `थोदफ्रेङ त्सल` (^96).
- **Chemchok Heruka** (`ཆེ་མཆོག་...ཧེ་རུ་ཀ`) — translated by meaning as `महोत्तर हेरुक` in blocks ^16 and ^17, but transliterated by sound as `छेछोग हेरुक` in blocks ^69 and ^71. Same deity, two incompatible treatments (translate vs. transliterate) within one text.

One related isolated slip (not repeating, so listed separately below): block ^17 of `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` enumerates three distinct names for Padmasambhava — `གཅིག་ནི་པདྨ་འབྱུང་གནས་ཞེས། གཅིག་ནི་པདྨ་སམྦྷ་ཝ། གཅིག་ནི་མཚོ་སྐྱེས་རྡོ་རྗེ་ཞེས།` — but Gemini collapses the first two into the identical string `पद्मसम्भव`, printed twice, losing the enumeration the source (and the DharmaMitra English, which keeps "Padmajungne" vs. "Padmasambhava" distinct) preserves.

**Optatives (ཤོག, གྱུར་ཅིག) rendered as flat statements.** Not found — optative/imperative mood is consistently preserved. `ཚད་མེད་བཞི།`'s four `...གྱུར་ཅིག` lines are all rendered with the Nepali jussive `होऊन्` ("may they be/become"), matching DharmaMitra's "may all sentient beings..." exactly in force. `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།`'s repeating `བྱིན་གྱིས་རློབས` / `སོལ` refrain (blocks ^2–^22) is rendered with consistent Nepali imperatives (`दिनुहोस्`, `गर्नुहोस्`, `हटाउनुहोस्`) every time, word-for-word identical across all 11 repeats. `གསོལ་འདེབས་ལེའུ་བདུན་མ།`'s closing refrain `བསམ་པ་ལྷུན་གྱིས་འགྲུབ་པར་བྱིན་གྱིས་རློབས` (blocks ^114–^131) is likewise consistently rendered as the imperative `इच्छाहरू स्वतः सिद्ध हुन अधिष्ठान गर्नुहोस्!`.

**Omitted or invented clauses.** None found at spot-check resolution. This matches the deterministic line-parity pass (0 failures); no block in the three texts showed a missing or extra clause relative to its Tibetan quote, and no bracketed or parenthetical commentary was inserted anywhere in the translated body text (checked by grep across all three files — the only parens/brackets present are in the YAML frontmatter and the standard `[!warning]` callout).

**Empty or duplicated lines.** None found. No blank lines appear inside any block's translation, and the repeated refrains (the mantra block in `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།`, the `ཨེ་མ་ཧོ` exclamations, and the Guru Rinpoche refrain in `གསོལ་འདེབས་ལེའུ་བདུན་མ།`) are legitimate repeats of an identical repeated Tibetan refrain, not translation artifacts.

**Commentary or bracketed glosses added.** None found (same grep as above).

## Isolated slips worth a human's eye (not systematic)

- `གསོལ་འདེབས་ལེའུ་བདུན་མ།` block ^60: `གནས་འདིར་ཐུགས་རྗེས་དགོངས་ཏེ་གཤེགས་ནས་ཀྱང་` ("having come here with compassionate intent") is rendered `यस स्थानमा करुणाले विचार गरी पालिसकेर पनि` — `पालिसकेर` ("having already nurtured/looked after") is an odd substitute for the honorific verb of motion `གཤེགས` ("come"); minor semantic drift.
- Same block ^60: `བྱང་ཆུབ་སྙིང་པོ` ("heart/essence of enlightenment," bodhimaṇḍa) is rendered as the coined compound `बोधिसार`, not standard Nepali Buddhist usage (DharmaMitra's English uses "heart of enlightenment"). Reads oddly but is comprehensible.
- `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` block ^17: the Padmajungne/Padmasambhava name-collapse described above under deity names — worth a human pass since it's a single occurrence rather than a repeating pattern.

## Verdict

**NEEDS A GLOSSARY/STYLE FIX** — specifically a small proper-noun termbase pinning the Nepali transliteration of Guru Rinpoche's alternate names and epithets (Orgyen/Urgyen, Thötreng Tsal, Chemchok Heruka, and the Padmajungne/Padmasambhava distinction) would close the one real, recurring defect found. Everything else checked — script, register (Nepali vs. Hindi), mantra transliteration, optative mood, line/clause parity, absence of added commentary — is clean, so short of that termbase fix this run is otherwise a solid machine baseline.
