# Nepali pilot review — gemini-translate

Model: `gemini-3.1-pro-preview` (default thinking, default temperature). Track: `3-TRANSFORMATIONS/Translations/Gemini/ne/`. Reference track: none (zero-shot from Tibetan, per skill default).

## Run summary

| Text | Blocks done/total | Calls | Fallbacks | Parity failures | Failed blocks | Stopped early |
|---|---|---|---|---|---|---|
| བློ་སྦྱོང་ཚིག་བརྒྱད་མ། (Eight Verses) | 10/10 | 2 | 0 | 0 | 0 | no |
| སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ། (21 Tārās) | 29/29 | 4 | 0 | 0 | 0 | no |

Both runs completed on the first pass — no parity re-runs, no failed calls, no 429s. `line_parity_failures: 0` in both files' frontmatter.

## Parity table

Verified two ways: the ledger's own `line_parity` field per block (all `true`, `parity_attempts: 1`), and by eye against the quoted Tibetan `>` lines above each block.

**Eight Verses** — every block's Nepali line count equals its Tibetan line count (blocks `^2`–`^9`: 4 Tibetan lines → 4 Nepali lines each; `^1` and `^10`: 1 line each). `^1` is the title-formula block, correctly overwritten by the stamp pass with the researched title (single line in, single line out — no parity issue).

**21 Tārās** — every block's Nepali line count equals its Tibetan line count: the 21 homage verses (`^3`–`^22`) are 4 Tibetan lines → 4 Nepali lines each; the closing homage `^23` is 6 → 6; the benefit verses `^24`,`^25`,`^26`,`^27` are 4 → 4; `^28` is 6 → 6; `^29` (colophon) is 1 → 1. Block `^1` (the `རྒྱ་གར་སྐད་དུ། … བོད་སྐད་དུ།` bilingual-title-formula block) is 2 Tibetan lines → 2 Nepali lines; unlike the two texts named in the skill's exception list, this block was *not* replaced by the stamp pass — Gemini translated it directly, transliterating the Sanskrit-in-Tibetan-script line ("ན་མཿཏཱ་རཱ་ཨེ་ཀ...") and rendering the Tibetan line, labelled "भारत भाषामा: … / भोट भाषामा: …". This is a reasonable and accurate treatment, not a defect. Block `^0` (H1) is the title, correctly substituted with the registry's researched title. Block IDs match the source one-for-one, in order, confirmed with `diff` on both texts.

## Findings by criterion

**1. Line parity** — Pass on both texts, no exceptions beyond the two intended title substitutions (`^1`/`^0` per skill rule 8, and note above for the Tārā formula block).

**2. Script and language** — Devanagari throughout both files; checked programmatically for stray Latin, Tibetan, or CJK characters in the rendered body (excluding the quoted `>` source lines and frontmatter) — none found in either file. No leading `༈`/`༄༅` ornament was copied into any rendered title. Verb endings, postpositions and honorifics read as Nepali, not Hindi: e.g. `-नुहोस्/-सकूँ` optative forms (Eight Verses `^2`–`^9`: "...धारण गर्न सकूँ ।"), `-ले`/`-लाई`/`-को` postpositions, and Nepali-only constructions like "गरेको छु", "हुनेछ", "भएकी" throughout the Tārā text.

**3. Mantras/dhāraṇīs** — All mantra syllables embedded in the 21 homages are transliterated into Devanagari and quoted, never translated: `^7` "'तुत्तार' र 'हूँ'", `^9` "'त्रत्' र 'फट्'", `^10`/`^19`/`^23` "'तुरे'", `^12`/`^22` "'तुत्तार'", `^13`/`^16`/`^18` "'हूँ'", `^17` "'स्वाहा' र 'ॐ'", `^20` "'तारा' उच्चारण र 'फट्'", `^22` "'हर' उच्चारण र 'तुत्तार'". Spellings are consistent across recurrences (तुत्तार always तुत्तार, तुरे always तुरे). Nothing dropped.

**4. Names** — `^2` "भट्टारिका आर्या तारा" for རྗེ་བཙུན་མ་འཕགས་མ་སྒྲོལ་མ — matches the actual Sanskrit epithet of this stotra (Bhaṭṭārikā Āryā Tārā). `^6` तथागत, `^11` त्रिरत्न, `^14` अमिताभ, `^8` इन्द्र/अग्नि/ब्रह्मा/वायु, `^8` भूत/वेताल/गन्धर्व/यक्ष, `^19` सुमेरु/मन्दर/विन्ध्य — all correct, established Sanskrit forms in Devanagari, consistent every time they recur. The Eight Verses colophon `^10` transliterates the author correctly: "कदम्पा गेशे लाङ्ग्री थाङ्पा दोर्जे सेङ्गे". Neither pilot text contains "गुरु रིན་པོ་ཆེ" or "ལ་མ", so that specific style-seed vocabulary is untested by this pilot.

**5. Register** — Devotional, recitable, natural Nepali word order in both texts; Buddhist vocabulary is idiomatic (चित्तसन्तति, अष्टलोकधर्म, कल्याणमित्र, पारमिता, जिन-पुत्र, विद्या for རིག་པ). One minor gloss: Tārā `^12` renders "ཏུ་ཏྟཱར་ཡིས" (by/with Tuttāra) as "'तुत्तार' मन्त्रद्वारा" — adding the word "मन्त्र" ("by the mantra Tuttāra") where the Tibetan line itself doesn't say "mantra". It's a harmless, arguably helpful clarification (the syllable *is* a mantra element) rather than an invented clause, but it is a small addition beyond a literal per-line rendering. Isolated, not seen elsewhere.

**6. Fidelity** — No omitted or invented clauses found on a full block-by-block read against the Tibetan (cross-checked select blocks against the DharmaMitra English, e.g. Tārā `^12`, which independently glosses the same line as "the great laughter of TUTTĀRE" — same content, same minor interpretive latitude). Optatives are correctly rendered as wishes, not statements: Eight Verses `^2`–`^9` consistently end "...गर्न सकूँ" ("may I be able to..."), never a flat statement. All 21 homages (`^3`–`^23`) begin with the homage phrase "वन्दना" (verified against every block).

**7. Consistency** — Recurring terms are stable across both texts: वन्दना (ཕྱག་འཚལ), अक्षर (ཡི་གེ), चरण (ཞབས), Tibetan-transliterated mantra syllables (तुत्तार, तुरे, त्रत्, फट्, हूँ, स्वाहा). One recurring stylistic pattern worth flagging (not a defect): in most of the 21 Tārā homages (e.g. `^4`, `^9`, `^10`, `^11`–`^23`), the addressee is named twice per verse — once as "उनलाई" near the start ("वन्दना उनलाई, ...") and again as "मातालाई" ("to the mother") at the close of the same quatrain. This is a byproduct of holding one Nepali line per Tibetan line across a sentence whose Tibetan verb/epithet falls only in the last line; it is grammatically valid as apposition and not incorrect, but it reads as mildly repetitive to a fluent Nepali ear compared with verses that avoid it (`^5`–`^8`, which read cleanly with a single "उनलाई"). Worth a light touch-up pass later; not severe enough on its own to call for a style.md change before a full run.

**8. Title** — Both H1 titles were substituted from `1-SOURCES/liturgy-titles.json` by the stamp pass, as expected.
- Eight Verses: `title_translated: चित्त अभ्यासका आठ श्लोक`. Clear, accessible standard Nepali; a Nepali Buddhist reader would understand it immediately. The registry's `ne_alt` "चित्त अभ्यास अष्टक" is also defensible — "-अष्टक" is the customary Sanskritic suffix for eight-verse hymns in Nepal's devotional literature (Buddhist and Hindu alike) — but it is more classical/terse and slightly less transparent to a general reader. Verdict: current title is fine; the "-अष्टक" alt is a legitimate, arguably more liturgically idiomatic alternative, not a correction.
- 21 Tārās: `title_translated: एकविंशति तारा स्तोत्र`. This mirrors the text's actual historical Sanskrit name (Tārā-ekaviṃśati-stotra) and matches the register the body text itself uses (Sanskritic epithets like भट्टारिका आर्या तारा). Verdict: this is the better choice over the more colloquial `ne_alt` "एक्काइस ताराको स्तुति" — recommend keeping as is.

## Style.md

Not changed. No systematic defect was found — no Hindi-for-Nepali substitution, no wrong script, no translated/dropped mantra syllables, no repeated parity failures, and the register issue found (the "उनलाई...मातालाई" doubling) is a stylistic softness in roughly half the Tārā homages, not a wrong-register pattern across the corpus. Per the task's bar for a style.md edit ("systematic defect"), this does not meet it; recorded as a finding for a future polishing pass instead of forcing a `--force` re-run on 39 blocks for a non-blocking wording pattern.

## Recommendation

**READY FOR FULL RUN.**
