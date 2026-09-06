# Corpus run review — Vietnamese machine baseline (Gemini track)

## Deterministic checks (done by the main session, reported here for the record)

- 94 files, 1892/1892 blocks translated
- 200 Gemini calls in the final run
- 0 blocks without line parity
- 0 failed blocks
- 0 block-id mismatches against the Tibetan
- no stray Tibetan or Chinese characters anywhere in the translated body text
- researched titles stamped on every file

## Texts read for this review

Pilot texts `བློ་སྦྱོང་ཚིག་བརྒྱད་མ།` and `སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ།` were skipped (already reviewed). Read in full, block by block, against the Tibetan and the DharmaMitra English baseline:

1. `གསོལ་འདེབས་ལེའུ་བདུན་མ།` (The Prayer in Seven Chapters) — 131/131 blocks, the longest text in the corpus.
2. `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` (Barche Lamsel) — 24/24 blocks; contains the Vajra Guru mantra repeated in every verse plus one extended mantra.
3. `ཚད་མེད་བཞི།` (The Four Immeasurables) — 1/1 block, all four lines optative.
4. `བདེན་ཚིག་སྨོན་ལམ།` (Words of Truth, HH the 14th Dalai Lama) — 9/9 blocks, read in addition to text 3 since the Four Immeasurables is only one block and gives too little surface area on its own for the optative/name checks.

## Findings by criterion

### 1. Missing diacritics
Not found. Checked with bare-ASCII heuristics and targeted searches for common Vietnamese function words appearing without their tone marks, across all four texts. Every genuine Vietnamese word carries full diacritics. The only ASCII-only tokens are proper names, mantra syllables, and interjections ("E Ma Ho", "Hum", "Om Ah Hum Vajra Guru Padma Siddhi Hum"), which is correct, not a diacritics defect.

### 2. Mantras / dhāraṇīs kept in romanized Sanskrit
Handled correctly and consistently everywhere checked. In `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` the Vajra Guru mantra `ཨོཾ་ཨཱཿཧཱུྃ་བཛྲ་གུ་རུ་པདྨ་སིདྡྷི་ཧཱུྃ༔` appears once per verse (blocks ^1 through ^24, 12 verses) and is rendered identically every single time as "Om Ah Hum Vajra Guru Padma Siddhi Hum" — never translated into Vietnamese meaning, never drifting in spelling. The extended closing mantra in block ^24 (`...པདྨ་ཐོད་ཕྲེང་རྩལ་བཛྲ་ས་མ་ཡ་ཛཿསིདྡྷི་ཕ་ལ་ཧཱུྃ་ཨཱ༔`) is rendered "Om Ah Hum Vajra Guru Padma Thotreng Tsal Vajra Samaya Dza Siddhi Phala Hum Ah", matching DharmaMitra's transliteration syllable for syllable (capitalization aside). In `བདེན་ཚིག་སྨོན་ལམ།` block ^1 the opening `ན་མོ་རཏྣ་ཏྲ་ཡཱ་ཡ།` is kept as "Namo Ratnatrayaya!" rather than translated. No instance was found anywhere of a mantra or dhāraṇī rendered into ordinary Vietnamese prose.

### 3. Deity/name consistency across blocks — the one systematic issue found
Confirmed systematic problem, but narrowly scoped to one stretch of one text. In `གསོལ་འདེབས་ལེའུ་བདུན་མ།`, blocks **^63 through ^99** (the guru-lineage supplication and Padmasambhava life-story section — 37 of the text's 131 blocks) render lineage-master and place names as raw, unprocessed Tibetan Wylie transliteration — capitalized syllable by syllable, apostrophes retained — instead of the natural phonetic/Sanskrit romanization the same document uses everywhere else. Examples, with block ids and the contrasting correct usage elsewhere in the *same* text:

- **^64**: "Đã ban gia trì cho Đức Kim Cang Tát Đỏa và **Dga' Rab Rdo Rje**" — Garab Dorje is spelled correctly, as "Garab Dorje", earlier in the same document at **^25** ("Con khẩn cầu Hóa thân Garab Dorje"); here it reverts to raw Wylie.
- **^66**: "Đại Đạo sư **'Jam Dpal Bshes Gnyen**" (Mañjuśrīmitra).
- **^70**: "Đã ban gia trì cho **Rdo Rje Thod 'Phreng Rtsal**" — the same figure is correctly given as "Padma Thodtreng Tsal" at **^54** ("Hỡi Đại Chí Tôn Padma Thodtreng Tsal vĩ đại").
- **^85**: "Con khẩn cầu Hóa thân **Mtsho Skyes Rdo Rje**" — should be phonetic "Tsokye Dorje", which this same corpus uses correctly in `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` **^17** ("Một hồng danh là Tsokye Dorje").
- **^86**: "Vua **Thor Cog Can**" and "vị vua có nhân duyên **In Dra Bo Dhi**" (Indrabhūti), both raw.
- **^87**: "Con khẩn cầu Đức **Shan Ta Ra Kshi Ta**" — Śāntarakṣita, a very well-known name in Buddhist historiography, left completely unromanized.
- **^88**: "**Rdo Rje Phag Mo**" (Vajravārāhī) and "**Rdo Rje Drag Po Rtsal**" both raw.
- **^92**: "Con khẩn cầu Hóa thân **Pad Ma Sam Bha**" — the same figure is "Liên Hoa Sanh" in blocks ^32, ^44, ^91, ^97 and ^114–^131. That is one figure named at least three different ways in one document: Liên Hoa Sanh / Padmasambhava / Pad Ma Sam Bha.
- **^96**: "Ngài dùng **Rdo Rje Phur Pa** tiêu diệt mọi chướng ngại ma quỷ" — Vajrakīlaya, which this same text names correctly as "Vajrakilaya" at **^21** ("Con khẩn cầu hải hội chư tôn Vajrakilaya").
- **^98–^99**: "Bsam Yas Mchims Phu", "Sgrub Chen Bka' Brgyad", "Stag Tshang Seng Ge Bsam 'Grub", "Rdo Rje Gro Lod Rtsal" — all raw Wylie.

Before block ^63 and after block ^99 — including all of `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།`, `ཚད་མེད་བཞི།`, and `བདེན་ཚིག་སྨོན་ལམ།` — names are rendered consistently and well ("Liên Hoa Sanh" for Padmasambhava throughout; "Quán Thế Âm" for Avalokiteśvara, consistent with "cõi Phổ Đà" for the Potala in `བདེན་ཚིག་སྨོན་ལམ།` ^7). A corpus-wide grep confirms the raw-Wylie apostrophe pattern (`'`) occurs 17 times in `གསོལ་འདེབས་ལེའུ་བདུན་མ།`, all inside blocks ^63–^99, and zero times in the other three texts read. This reads like a batching artifact: the dense proper-name lineage list in that stretch apparently pushed Gemini toward literal transliteration for a contiguous run of batches, while batches before and after it stayed on the established phonetic convention.

One further name-related observation that is **not** a bug: in `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` block ^17 the Tibetan itself lists four alternate/secret names of the guru side by side (པདྨ་འབྱུང་གནས་ / པདྨ་སམྦྷ་ཝ་ / མཚོ་སྐྱེས་རྡོ་རྗེ་ / གསང་མཚན་རྡོ་རྗེ་དྲག་པོ་རྩལ), and the Vietnamese correctly gives four distinct names ("Liên Hoa Sanh / Padmasambhava / Tsokye Dorje / Dorje Drakpo Tsal"), matching how the DharmaMitra English baseline splits the same four names. That block is being faithful to the source, not inconsistent.

### 4. Optatives (ཤོག / གྱུར་ཅིག) rendered as "nguyện…" rather than flat statements
Handled correctly everywhere checked. `ཚད་མེད་བཞི།` (all four lines end in གྱུར་ཅིག) comes out as four parallel "Nguyện tất cả chúng sinh…" lines — textbook-correct optative treatment. `བདེན་ཚིག་སྨོན་ལམ།` block ^9's closing ཤོག line becomes "Nguyện những lời chân nguyện của chúng con mau chóng thành tựu vô ngại," and the other seven mdzod/stsol/gsol-type request-verbs in blocks ^2–^8 of that text are all rendered with "Nguyện…" or "Xin…" formulas, never flattened into plain declaratives. `གསོལ་འདེབས་ལེའུ་བདུན་མ།` and `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` don't use ཤོག/གྱུར་ཅིག at all (their appeal verb is གསོལ་བ་འདེབས / བྱིན་གྱིས་རློབས instead), and those are consistently rendered "Con khẩn cầu…" / "Xin ban gia trì cho con…" throughout — including all 12 repetitions of the refrain in Barche Lamsel. No flattening into indicative statements was found anywhere in the sample.

### 5. Content sliding across line boundaries within a block
Not found beyond what the pilot already flagged as isolated. Line-by-line alignment against the Tibetan was checked by hand on roughly 25 blocks spread across all four texts, including the architecturally dense mandala-description blocks (^40–^51 of Le'u Dun Ma), the full 14-line block ^5 of Barche Lamsel, the refrain block of Barche Lamsel across all 12 repetitions, and both short texts in full. No case of content drifting to an adjacent line was found. Combined with the deterministic 0/1892 line-parity failures already reported and no new cases surfacing in this manual check, this looks like a genuinely rare, isolated phenomenon, not a systematic one.

### 6. Omitted or invented clauses
None found. Every block checked against the DharmaMitra English baseline carries the same propositional content, the same number of clauses, in the same order.

### 7. Empty or duplicated lines
None found. Checked programmatically for both longer texts: no runs of two or more blank lines, and the 12-times-repeated refrain block of Barche Lamsel is byte-identical on all 12 repetitions (verified by diffing all 8 refrain lines × 12 occurrences) with no accidental duplication or dropped repetition.

### 8. Commentary or bracketed glosses added
None found. No brackets or parentheses appear anywhere in the four texts' translated body text — only in YAML frontmatter and the standard machine-baseline warning banner, which are template text, not model output.

## Isolated slips worth a human's eye

- `གསོལ་འདེབས་ལེའུ་བདུན་མ།` ^62: "Con khẩn cầu dòng truyền thừa tâm ấn của chư Phật" for རྒྱལ་བ་དགོངས་པ་བརྒྱུད་པ་ལ (lit. "to the mind-lineage of the Victors") — a loose but not wrong paraphrase; could be tightened to name the "dòng tâm truyền" (mind-lineage) explicitly.
- `གསོལ་འདེབས་ལེའུ་བདུན་མ།`: the epithet "xứ Uddiyana" is appended to "Liên Hoa Sanh" in some blocks (^32, ^114 onward) but not others (^44, ^91) — a minor epithet-dropping inconsistency, much smaller in impact than the Wylie-name problem in finding 3.
- `གསོལ་འདེབས་ལེའུ་བདུན་མ།` ^87: Śāntarakṣita transliterated as "Shan Ta Ra Kshi Ta" rather than a standard spelling — the single most jarring individual instance of the block-63–99 problem, since this is a name most Vietnamese Buddhist readers would recognize on sight if romanized normally.
- A few Wylie names in that same block range (e.g. "Rdo Rje Gzhon Nu" at ^70) will read to a Vietnamese reciter as a typo rather than a name, more disruptive to recitation than a simple missing-diacritic slip would be.

## Verdict

**NEEDS A GLOSSARY/STYLE FIX** — specifically a Tibetan-name-romanization glossary for lineage-master and place names, applied at minimum to blocks ^63–^99 of `གསོལ་འདེབས་ལེའུ་བདུན་མ།` (where it would fix a real, reader-facing defect: the same deities/masters named three different ways in one document), and ideally supplied corpus-wide as a rails input to prevent recurrence in other lineage-heavy texts. Every other criterion checked in this pass — mantra fidelity, optative rendering, diacritics, line/clause integrity, absence of invented or omitted content, absence of added commentary — is at ACCEPTABLE AS MACHINE BASELINE quality, including the mantra-dense `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།`, which is clean throughout.
