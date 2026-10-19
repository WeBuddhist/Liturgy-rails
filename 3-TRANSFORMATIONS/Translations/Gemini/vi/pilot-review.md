Pilot review — Vietnamese (vi) Gemini machine-baseline track

Model: gemini-3.1-pro-preview. Track: `3-TRANSFORMATIONS/Translations/Gemini/vi/`.

## Run summary

| Text | Blocks done/total | Calls | Parity failures | Failed blocks | Stopped early |
|---|---|---|---|---|---|
| བློ་སྦྱོང་ཚིག་བརྒྱད་མ། (Eight Verses) | 10/10 | 2 | 0 | 0 | no |
| སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ། (21 Tārās) | 29/29 | 4 | 0 | 0 | no |

Reports: `work/_corpus-run-20260906T182350.json` (Eight Verses), `work/_corpus-run-20260906T182453.json` (21 Tārās). Both texts re-stamped by the driver (`ids`, `track-meta`, `titles`) on completion; `title_translated` present in both files.

## Parity table

Verified independently by parsing both rendered files and comparing Tibetan quote-line counts to Vietnamese line counts per block (in addition to the driver's own `line_parity_failures: 0`).

**Eight Verses** — every block ^1 through ^10 matches (1, 1, 4, 4, 4, 4, 4, 4, 4, 1 lines respectively). Block ^1's Tibetan source is a lone repeated title line; its Vietnamese rendering ("Tu Tâm Bát Tụng") happens to equal the registry's `vi_title` because Gemini translated the same Tibetan+English title pair the registry title itself was generated from — not because of a stamp overwrite (this text is not one of the two named title-formula exceptions in the skill's rule 8).

**21 Tārās** — every block ^1 through ^29 matches, including the two 6-line blocks (^23, closing the 21st homage plus the two summary lines; ^28, the six-line "child/wealth/all desires" verse). Block ^1 (the Sanskrit/Tibetan bilingual title-formula line) is 2 Tibetan lines and 2 Vietnamese lines — "Tiếng Ấn Độ: ... / Tiếng Tây Tạng: ...". Blocks ^0 in both files show no independent parity concern; the apparent 2-line "source" my first parsing pass attributed to block ^0 was the callout box's two lines, an artifact of naive `>`-line counting, not a real block.

No line-parity problems anywhere in either text.

## Findings by criterion (with block ids and quotes)

**1. Line parity** — Clean in both texts, see table above.

**2. Script** — Full Vietnamese diacritics throughout; a targeted grep for undiacritized Vietnamese words (nguyen, duoc, cua, tat, khong, etc.) and for stray Tibetan/CJK Unicode ranges in the rendered (non-quoted) lines returned nothing except deliberately-romanized mantra syllables ("Phat", "Trat", "Tara", "Tuttara" — correct per the style) and correctly-spelled diacritic-free Vietnamese words ("Tam" in "Tam Bảo", "ban" in "được ban"). No leading `༈` ornament or other stray Tibetan/Chinese characters leaked into any Vietnamese line.

**3. Mantras/dhāraṇīs** — This pair has no standalone mantra-recitation block; the "mantra" content is the seed-syllables named inside the 21 homage verses (Tuttāra Hūṃ ^7, Traṭ/Phaṭ ^9, Ture ^10/^19, Tuttāre ^12, Hāra/Tuttāra ^22, Tāra/Phaṭ ^20). All are kept in romanized form, never translated, never dropped, e.g. ^9 "Kính lễ Độ Mẫu âm Trat và Phat," and ^20 "Tụng hai lần Tara cùng với âm Phat,". The two spelling variants the Tibetan itself uses for "tuttāra/tuttāre" (^7 vs ^12) both come out as "Tuttara" in Vietnamese — a harmless collapse of a distinction that isn't semantically load-bearing.

**4. Names and terms** — Tārā is consistently "Độ Mẫu" (Sino-Vietnamese, matches the seed style and `vi_alt`/`vi_title` usage), combined with the proper name at the invocation (^2 "Thánh nữ Độ Mẫu Tara tôn quý"). Bhagavatī in the colophon (^29, 21 Tārās) is rendered with the classical calque "Bạc-già-phạm-mẫu", and "samyaksambuddha" as "Đức Phật Chánh Đẳng Chánh Giác" — both standard Sino-Vietnamese sutra-register terms. The author colophon in Eight Verses (^10) transliterates "Langri Tangpa Dorje Senge" consistently with the English baseline. One isolated inconsistency: Eight Verses ^8 uses "quần sinh" ("Xin dâng hết thảy lợi lạc an vui cho quần sinh mẹ hiền,") where "chúng sinh" (the term used everywhere else, e.g. Eight Verses ^2, 21 Tārās ^28) would be the standard, consistent choice — one-off, not systematic.

**5. Register** — Devotional and recitable throughout; no added honorifics, brackets, or commentary in either file. The 21 Tārās verses read naturally as a chant, each opening with the same fixed homage phrase.

**6. Fidelity** — No omitted or invented clauses in either text. Eight Verses' optatives are all correctly kept as wishes ("Nguyện …") rather than statements, e.g. ^4 "Nguyện dứt khoát đối mặt và đẩy lui." and ^9 "...giải thoát mọi buộc ràng." (continuing the same "Nguyện" from line 1 of that quatrain). The benefits section of 21 Tārās (^24–^28) is correctly rendered as descriptive future/passive statements ("sẽ", "được ban", "liền có được") rather than false optatives, matching the Tibetan's own non-optative grammar there (it isn't a ཤོག/gyur-cig passage). All 21 homages (^3–^23) begin with a homage phrase — "Kính lễ" in every case, with the initial single invocation (^2) using the related but distinct "Con xin đảnh lễ" for its different Tibetan verb form (ལོ vs. the ཕྱག་འཚལ་ formula).

Two isolated cases of content sliding across a line boundary within a block (not across blocks, and not a parity or omission problem): Eight Verses ^8 puts "mẹ hiền" (mother) into line 2 as well as line 3, where the Tibetan's "མ་ཡི་" (of mothers) belongs only to line 3; 21 Tārās ^8 moves "Agni/fire-god" from the Tibetan's line 1 into the Vietnamese's line 2 ("Hỏa thần, Phong thần, Tự Tại cúng dường,"), while line 1 keeps only Indra and Brahma ("Kính lễ bậc được Đế Thích, Phạm Thiên,"). In both cases every deity/concept is still present somewhere in the block; nothing is lost.

**7. Consistency** — "Kính lễ" for all 21 homages; "Độ Mẫu" for Tārā everywhere it's used as an epithet, "Tara"/mantra-syllable forms reserved for the actual chant syllables. Two verses (^8, ^13 of 21 Tārās) address the object of homage without repeating "Độ Mẫu" explicitly (e.g. ^13 "Kính lễ hội chúng Hộ thần mặt đất,") — grammatically justified by those verses' different Tibetan syntax (they describe hosts who serve/are summoned rather than directly re-naming Tārā), but worth noting as a minor pattern variation, not an error.

**8. Title** — Both registry titles (`vi_title`) are dense, unattested, Sino-Vietnamese calques of the Chinese titles:
- Eight Verses: `vi_title` "Tu Tâm Bát Tụng" (mirrors 修心八頌) vs. `vi_alt` "Tám Bài Kệ Luyện Tâm" / "Tám Kệ Tu Tâm".
- 21 Tārās: `vi_title` "Nhị Thập Nhất Độ Mẫu Lễ Tán Văn" (mirrors 二十一度母禮讚文) vs. `vi_alt` "Tán Tụng Nhị Thập Nhất Độ Mẫu" / "Tán Tụng Hai Mươi Mốt Vị Độ Mẫu".

For an app display title aimed at a general Vietnamese Buddhist readership rather than a classically-trained Sino-Vietnamese audience, the plainer alternatives read better: "Tám Bài Kệ Luyện Tâm" is immediately transparent (native numeral "Tám" + "Bài Kệ" + "Luyện Tâm") where "Tu Tâm Bát Tụng" strings together four Han-Vietnamese morphemes with no native-Vietnamese anchor. Likewise "Tán Tụng Hai Mươi Mốt Vị Độ Mẫu" (native numeral "Hai Mươi Mốt" plus the respectful classifier "Vị") reads as a natural devotional phrase, where the registry's "Nhị Thập Nhất Độ Mẫu Lễ Tán Văn" stacks four Sino-Vietnamese compounds in a row and ends in the dry, catalogue-like "Lễ Tán Văn" ("praise-text"). Recommendation: consider the `vi_alt` forms for the app's display title in both cases; this is a title-registry decision, not something addressed by this run (the registry itself was not edited).

## Style.md

Not changed. No systematic defect was found — line parity was perfect on the first attempt for every block in both texts (no parity re-runs needed), script and diacritics were clean, mantra syllables were handled correctly and consistently, and register/fidelity held up across all 39 blocks. The two content-redistribution cases (Eight Verses ^8, 21 Tārās ^8) and the "quần sinh"/"chúng sinh" variant (Eight Verses ^8) are isolated wording choices, not a pattern that would justify rewriting the system prompt; per the runbook they are reported, not fixed.

## Recommendation

READY FOR FULL RUN.
