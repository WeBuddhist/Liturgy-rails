Pilot review — Gemini Hindi track (`hi`)

## Step 1 — run summary

`སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ།` (Praises to the Twenty-One Tārās), run 2026-09-06T18:22:15–18:24:46:

- texts attempted: 1/1
- blocks: 29/29 in ledger, 4 calls this run
- parity failures: 0
- failed blocks (no usable response): 0
- run not stopped early
- report: `work/_corpus-run-20260906T182215.json`
- track-only stamp passes ran automatically: ids, track-meta, titles (1 translation file updated each pass)

`བློ་སྦྱོང་ཚིག་བརྒྱད་མ།` (Eight Verses of Mind Training) was not re-run — it was already 10/10 and stamped before this session, per the task brief. Not touched.

## Parity tables

### Eight Verses (10 blocks)

| block | Tibetan lines | Hindi lines | match |
|---|---|---|---|
| ^1 (title formula) | 1 | 1 (researched-title substitution) | yes |
| ^2–^9 (8 verses) | 4 each | 4 each | yes |
| ^10 (colophon) | 1 | 1 | yes |

Frontmatter: `blocks_translated: 10`, `blocks_total: 10`, `line_parity_failures: 0`.

### Praises to the Twenty-One Tārās (29 blocks)

| block | Tibetan lines | Hindi lines | match |
|---|---|---|---|
| ^1 (Skt/Tib incipit couplet) | 2 | 2 | yes |
| ^2 (Oṃ homage) | 1 | 1 | yes |
| ^3–^22 (20 four-line homages) | 4 each | 4 each | yes |
| ^23 (six-line homage + mantra reference) | 6 | 6 | yes |
| ^24–^27 | 4 each | 4 each | yes |
| ^28 | 6 | 6 | yes |
| ^29 (colophon) | 1 | 1 | yes |

Frontmatter: `blocks_translated: 29`, `blocks_total: 29`, `line_parity_failures: 0`. Spot-checked by eye against the source (including the two 6-line blocks, ^23 and ^28) with no discrepancies. A stray Tibetan `ྃ` glyph present in the *source* line for `^21` (`ཀུན་ནས་གོ་ཆ་དགའ་བའི་བརྗིད་ཀྱིས། །ྃ`, an apparent OCR/typo artifact) was correctly not carried into the Hindi rendering.

## Findings by criterion

**1. Line parity** — Clean in both texts; see tables above. No blocks required a solo re-run this pass (0 calls beyond the 4 batch calls).

**2. Script** — A full character scan of every non-quoted, non-frontmatter line in both files found only Devanagari, standard punctuation, and the sacred syllable `ॐ` (used correctly for untranslated Oṃ, e.g. Tārā `^2`, `^17`). No stray Latin, Tibetan, or Chinese characters, and no leading `༈`/`༄༅` ornaments were carried over from the source lines into any Hindi line.

**3. Mantras / bīja syllables** — This text has no single standalone mantra block; the root-mantra syllables (tuttāre, hūṃ, traṭ, phaṭ, ture, tāra, hara, oṃ, svāhā) are woven through the 21 homage verses themselves, exactly as in the Tibetan and in the DharmaMitra English baseline. All are transliterated into Devanagari, never translated as ordinary words, and rendered consistently every time they recur:
  - `ཏུཏྟྭ་ར/ཏུ་ཏྟཱར` → तुत्तारे (`^7`, `^12`)
  - `ཏྲད...ཕཊ` → त्रट्...फट् (`^9`)
  - `ཏུ་རེ` → तुरे (`^10`, `^19`)
  - `ཧཱུཾ` → हूँ (`^7`, `^13`, `^16`, `^18`, `^19`)
  - `ཧ་ར...ཏུཏྟཱ་ར` → हर...तुत्तारे (`^22`)
  - `སྭཱ་ཧཱ་ཨོཾ` → स्वाहा और ॐ (`^17`)
  - `^23`'s reference to "the root mantra" (`རྩ་བའི་སྔགས་ཀྱིས་བསྟོད་པ་འདི`) is correctly rendered as a reference ("मूल मंत्र द्वारा यह स्तुति") rather than invented as a spelled-out string — the source itself never spells the full mantra out as one line, so nothing was dropped.
  No syllables were translated as ordinary vocabulary and none were omitted.

**4. Names** — तारा (Tārā) throughout, never varied. अमिताभ (Amitābha, `^14`). जिनपुत्र for "rgyal ba'i sras" (children of the Victors / bodhisattvas, `^6`) and बुद्ध for "rgyal ba" (Victorious Ones, `^25`) are both settled Buddhist-Sanskrit choices, used consistently. सम्यक् सम्बुद्ध for "yang dag par rdzogs pa'i sangs rgyas" (`^29` colophon) is precise (samyaksambuddha, not a generic "बुद्ध"). ईश्वर for "dbang phyug" (Īśvara/Maheśvara, `^8`) is a correct rendering of a Hindu deity-name that the *source itself* names as a worldly god paying homage to Tārā — not a stray borrowing. In Eight Verses, the colophon's Tibetan personal name is transliterated: "कदम्प गेशे लंगरी थंगप दोर्जे सेंगे" (`^10`).

**5. Register** — Devotional, Sanskritized Hindi throughout, natural word order rather than a syntactic calque of the Tibetan (e.g. Tārā `^8`: "उनको नमस्कार, जिनकी शक्र, अग्नि, ब्रह्मा, वायु तथा विभिन्न ईश्वरों द्वारा पूजा की जाती है" reorders the Tibetan's verb-final clause into natural Hindi passive construction). No Hindu-devotional formulas (आरती, जय हो, भगवान, प्रभु) or Christian idiom found anywhere in either file. No added honorifics, glosses, or bracketed commentary.

**6. Fidelity** — No omitted or invented clauses found in a full block-by-block read against the Tibetan and the DharmaMitra English baseline. Optatives are correctly rendered as wishes, not statements: every one of the 8 verses in Eight Verses ends its Tibetan `...ཤོག` with a genuine Hindi optative "...सकूँ" (may I be able to), e.g. `^2` "उन्हें सर्वदा प्रिय मान सकूँ।", `^9` "...आसक्ति-रहित होकर मैं बन्धनों से मुक्त हो सकूँ।". All 21 homages (`ཕྱག་འཚལ་`) in the Tārā text begin with a homage phrase — "तारा को नमस्कार" for the one verse that names her directly (`^3`) and "उनको नमस्कार" for the remaining twenty (`^4`–`^23`), correctly mirroring the source's own pattern of naming her only once.

**7. Consistency** — Recurring terms hold steady across both files: बुद्ध/धर्म/संघ, तारा, all bīja transliterations (listed under #3), and the "सकूँ" optative pattern in Eight Verses. No term was found rendered two different ways within a text.

**8. Title** — `title_translated` for each file, and the `hi_alt` entries on the same texts in `1-SOURCES/liturgy-titles.json` (not edited):

- **Tārā text**: chosen "तारा एकविंशति स्तोत्र" (Tārā Ekaviṃśati Stotra) vs. alt "एकविंशतितारा स्तोत्र" / "इक्कीस ताराओं की स्तुति". The chosen title mirrors the canonical Sanskrit incipit (as the English/Chinese registry entries do too) and is the form a Hindi Buddhist reader would expect from a puja book or scholarly source. **No change recommended.**
- **Eight Verses**: chosen "चित्तशोधन अष्टगाथा" vs. alt "चित्त प्रशिक्षण के आठ श्लोक" / "चित्तशोधन अष्टक". "लोजोंग" (blo sbyong) means mind *training*, and चित्तशोधन reads as mind *purification/cleansing* — a related but not identical sense; "चित्त प्रशिक्षण" (mind training) is the more literal and more commonly used term in Hindi Buddhist writing for this specific genre. **The alt "चित्त प्रशिक्षण के आठ श्लोक" is arguably a better title than the one currently stamped**, though "चित्तशोधन अष्टगाथा" is not wrong, just a looser rendering of "training." This is a registry-level judgment call, not a track defect; the registry was not edited per instructions.

## Step 3 — style.md

No systematic defect found (script, mantra handling, register, and parity were all clean). **`style.md` was not edited** and neither pilot text was re-run with `--force`.

## Recommendation

**READY FOR FULL RUN.**
