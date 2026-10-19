# Hindi corpus run — spot review

## Deterministic numbers (from the main session's full-corpus check)

- Track: `3-TRANSFORMATIONS/Translations/Gemini/hi/`
- 94 files, 1892/1892 blocks translated
- 194 Gemini calls in the final run
- 0 blocks without line parity, 0 failed blocks, 0 block-id mismatches against the Tibetan
- Researched titles stamped on every file
- Known blemish (being fixed separately, not re-reported here): 7 lines copied the Tibetan `༈` ornament literally onto "एमाहो" (6 in `གསོལ་འདེབས་ལེའུ་བདུན་མ།`, 1 in `བདེ་སྨོན་བསྡུས་པ།`)

## Texts read for this review

1. `གསོལ་འདེབས་ལེའུ་བདུན་མ།-hi.md` — full text, 131/131 blocks, read against the Tibetan in `1-SOURCES/Text/` and the DharmaMitra English baseline.
2. `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།-hi.md` — full text, 24/24 blocks, mantra-heavy (Vajra Guru mantra repeated 12×, long-form mantra once).
3. `ཚད་མེད་བཞི།-hi.md` — full text, 1/1 block (the Four Immeasurables, four optative lines).

156 blocks read line-by-line in total.

## Findings by criterion

**Script integrity.** No stray Latin, Chinese, or untransliterated Tibetan found in any translated line across all three texts (checked programmatically outside frontmatter/blockquotes). Devanagari throughout.

**Mantras/dhāraṇīs.** Correctly transliterated, never translated. In `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` the core mantra `ཨོཾ་ཨཱཿཧཱུྃ་བཛྲ་གུ་རུ་པདྨ་སིདྡྷི་ཧཱུྃ༔` is rendered identically as "ॐ आह हूँ वज्र गुरु पद्म सिद्धि हूँ।" all 12 times it recurs (blocks ^2–^24), and the closing long-form mantra `ཨོཾ་ཨཱཿཧཱུྃ་བཛྲ་གུ་རུ་པདྨ་ཐོད་ཕྲེང་རྩལ་བཛྲ་ས་མ་ཡ་ཛཿསིདྡྷི་ཕ་ལ་ཧཱུྃ་ཨཱ༔` (block ^24) is transliterated in full, not translated. This is the strongest result in the sample. (Minor note: ཨཱཿ is rendered "आह" rather than "आः"; defensible phonetic choice, not an error.)

**Optatives (ཤོག / གྱུར་ཅིག).** Correctly rendered as Hindi subjunctive/optative mood, not flattened to indicative statements. `ཚད་མེད་བཞི།` block ^1: all four `...གྱུར་ཅིག` lines use "हों" (सुख ... से युक्त **हों**, दुःख ... से मुक्त **हों**, वियुक्त न **हों**, उपेक्षा में स्थित **हों**) — matching DharmaMitra's "May all sentient beings **be**..." exactly in mood, not just lexically.

**Omitted or invented clauses.** None found. Every line of all 156 blocks maps one-to-one to its Tibetan source line and tracks the DharmaMitra English baseline in content (consistent with the deterministic 0 line-parity-failure result already verified corpus-wide).

**Empty or duplicated lines.** None found (checked programmatically for consecutive duplicate lines in all three files).

**Hindu-devotional / Christian idiom.** Not found. Register stays Buddhist-Sanskritized throughout (बुद्ध, धर्म, बोधिसत्त्व, त्रिकाय, गुरु, सुगत, आशय, अभिप्राय, विद्याधर, डाकिनी, etc.), matching the style instruction's vocabulary list. One borderline word: "मोक्ष-मार्ग" for ཐར་པའི་ལམ་ in `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` ^19 ("राजा और मन्त्रियों को मोक्ष-मार्ग पर स्थापित किया") — मोक्ष is a pan-Indian liberation term also used in Hindi Buddhist writing, not a clear Hindu-specific intrusion, but worth a glossary rule if a stricter term (मुक्ति/निर्वाण-मार्ग) is preferred.

**Commentary or bracketed glosses.** One isolated instance: `གསོལ་འདེབས་ལེའུ་བདུན་མ།` block ^98, "काग्ये (अष्ट महासाधन) के गुह्यमन्त्र मण्डल में" — a parenthetical gloss expanding "Kagyé" (བཀའ་བརྒྱད) that the style instruction says not to add. Single occurrence out of 156 blocks reviewed; not systematic.

**Names of buddhas/deities/places — consistency across blocks (systematic issue found).** The underlying identifications are always correct (e.g. the text's own alternation between Amitābha སྣང་བ་མཐའ་ཡས and Amitāyus ཚེ་དཔག་མེད is tracked correctly block by block), but the **Devanagari spelling of the same proper name drifts repeatedly** because no glossary/termbase was used (frontmatter: `glossary: none`):
- **Oḍḍiyāna/Orgyen** — three spellings in `གསོལ་འདེབས་ལེའུ་བདུན་མ།`: उड्डियान (^4, ^92), ओड्डियान (^32, ^37), उड्यियान (^114–^131, i.e. the refrain repeated 18 times). Two spellings in `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།`: ओर्ग्येन (^1) vs ओग्येन (^21).
- **Thötreng Tsal** (པདྨ་ཐོད་འཕྲེང་རྩལ) — two spellings in `གསོལ་འདེབས་ལེའུ་བདུན་མ།`: थोत्रेंग त्सल (^54, ^64) vs थोद्रेङ त्सल (^96).
- **Amitāyus epithet** — three spellings across ^74, ^91, ^105: अमितायुष, अमितायुस्, अमितायु.

This is a real, repeating pattern (not a one-off typo) and is exactly the kind of thing a per-language proper-name glossary is meant to lock down before a baseline is used downstream.

## Isolated slips worth a human's eye

- `གསོལ་འདེབས་ལེའུ་བདུན་མ།` ^57 and ^58 — last line of each block ends with a comma instead of a daṇḍa/full stop before the block marker.
- `གསོལ་འདེབས་ལེའུ་བདུན་མ།` ^92 — "पद्मसंभव" (no visarga) where every other occurrence of the same name uses "पद्मसम्भव."
- `གསོལ་འདེབས་ལེའུ་བདུན་མ།` ^98 — added parenthetical gloss "(अष्ट महासाधन)" (see above).
- `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` ^19 — "मोक्ष-मार्ग" (see Hindu-idiom note above); optional glossary call, not clearly wrong.

## Verdict

**NEEDS A GLOSSARY/STYLE FIX** — specifically a proper-name transliteration termbase for recurring epithets and toponyms (Oḍḍiyāna/Orgyen, Thötreng Tsal, the Amitāyus family of names, and similarly-structured repeating names elsewhere in the corpus) to lock one Devanagari spelling per name. Everything else checked — mantra/dhāraṇī transliteration, optative mood, script integrity, line/clause completeness, absence of Hindu-devotional or Christian idiom, absence of added commentary (bar one isolated gloss) — held up well across all 156 blocks read. The defect found is orthographic-consistency, not meaning-level, but it is systematic (recurs across 2 of the 3 texts, on 3 different names) rather than isolated, which is why it clears the bar for a fix before this baseline is used downstream.
