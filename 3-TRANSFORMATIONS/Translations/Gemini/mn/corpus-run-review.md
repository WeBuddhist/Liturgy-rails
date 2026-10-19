# Gemini/mn full-corpus spot review — 2026-09-07

Scope: not a re-run of the deterministic checks (already done on the whole `3-TRANSFORMATIONS/Translations/Gemini/mn/` track by the main session), but a block-by-block human-style read of three texts not seen in the 2026-09-06 pilot (`བློ་སྦྱོང་ཚིག་བརྒྱད་མ།`, `སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ།`), checked against the quoted Tibetan and against the DharmaMitra English baseline (`3-TRANSFORMATIONS/Translations/Dharmamitra/en/`).

## Deterministic numbers (from the main session's corpus-wide check, reported here for the record)

- 94 files, 1892/1892 blocks translated
- 206 Gemini calls in the final run
- 0 blocks without line parity, 0 failed blocks, 0 block-id mismatches against the Tibetan
- No stray Tibetan or Chinese characters anywhere in the track
- Researched titles stamped on every file
- Glossary (`glossary.tsv`) added after the run to pin recurring proper names and the Tārā mantra syllables; drifted blocks re-translated with it in context

## Texts read for this review

1. `གསོལ་འདེབས་ལེའུ་བདུན་མ།-mn.md` — 131 blocks, read in full (longest text in the corpus)
2. `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།-mn.md` — 24 blocks, contains a 13-times-repeated mantra refrain
3. `ཚད་མེད་བཞི།-mn.md` — 1 block (the whole "Four Immeasurables" is a single block), chosen as the short text

## Findings by criterion

**1. Script.** Clean. An independent grep for any Latin/CJK/Tibetan character in a non-quote translation line, across all three files, returned nothing outside frontmatter metadata fields (`text_id:`, `source_language: tibetan`, etc., which are expected to contain Latin). No traditional Mongolian script, no leaked Tibetan or Chinese.

**2. Line parity.** Independently re-verified with a separate script (not just trusting the driver's self-report): every content block (`^1` through `^131`, `^1`–`^24`, and the single `^1`) has Mongolian line count exactly equal to Tibetan line count in all three files. No padding, trimming, or dropped/duplicated block IDs.

**3. Mantras/dhāraṇīs.** `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` repeats the guru-mantra refrain `ཨོཾ་ཨཱཿཧཱུྃ་བཛྲ་གུ་རུ་པདྨ་སིདྡྷི་ཧཱུྃ` after every one of its 12 middle stanzas plus once more in the closing block — 13 occurrences of the identical Tibetan line. 12 of the 13 render `сидди хум` (two д, matching the attested `сиди/сидди хум` recitation family); the very first occurrence, block `^1` (line 61), instead renders `... бадмэ сиди хум` (one д) — an internal inconsistency confined to this one instance of an otherwise perfectly repeated line. The extended closing mantra in block `^24` (`... падма тход-пхренг ...`) is transliterated correctly and consistently with the glossary's pinned form `төдрэнгцэл`.

`ཚད་མེད་བཞི།` and `གསོལ་འདེབས་ལེའུ་བདུན་མ།` contain no dedicated mantra lines (Le'u Dun ma uses the interjections `ཨེ་མ་ཧོ` / `ཧཱུྃ` instead — see §7 below, a related but distinct consistency issue).

**4. Names of buddhas/deities after the pinning.** Overwhelmingly consistent and a good sign the September 6 glossary fix generalized. Verified by tracing each pinned name across every one of its occurrences in the two long texts:
- `Ловон Бадамжунай` (Padmasambhava) — consistent wherever the full form is used; blocks `^114`–`^131` of Le'u Dun ma correctly drop to the short form `Бадамжунай`, but this mirrors the Tibetan itself switching to the short `པད་འབྱུང་` in those same verses, not a translation slip.
- `Аюуш` (Amitāyus) — consistent at `^22`, `^74`, `^91`, `^105`.
- `Авид` (Amitābha) — consistent at `^128`.
- `Гарабдорж`, `Ешэцожил`, `Трисон Дэцэн`, `Жанрайсиг`, `Манзушир`, `Очирваань`, `Базарсад` (Vajrasattva), `Самантабадра`, `Шагжамуни`, `Хурмаст` (Indra), `Эсрүн` (Brahma) — all consistent everywhere they recur across both texts.

Two genuine cross-block naming inconsistencies were found, both centered on Padmasambhava's wrathful "secret name" `རྡོ་རྗེ་... རྩལ`, which the pilot's proper-name pinning pass evidently didn't fully reach:
- **`རྡོ་རྗེ་ཐོད་འཕྲེང་རྩལ` (Dorje Thötreng Tsal), within one file.** Le'u Dun ma block `^70` (line 853) renders it `Дорж Тодрэнгзалд`; block `^96` (line 1159), the identical name, renders it `Дорж Тодэнзалд`. Neither matches the pinned glossary form `Төдрэнгцэл` that the *same corpus* correctly uses in the Bar-chad-lam-sel mantra (block `^24`). Root cause: the glossary's exact-match key is `ཐོད་ཕྲེང་རྩལ` (no `འ`), but both narrative occurrences in Le'u Dun ma spell the name `ཐོད་འཕྲེང་རྩལ` (with `འ`) — a source-side orthographic variant the glossary lookup doesn't catch, so pinning silently didn't fire for this text.
- **`རྡོ་རྗེ་དྲག་པོ་རྩལ` (Dorje Drakpo Tsal), across files.** Bar-chad-lam-sel `^17` renders the secret name `Дорждагвазэл`; Le'u Dun ma `^75` and `^88` render the same name `Дорж Дагбозалд` — internally consistent within Le'u Dun ma, but a different spelling from the other text. Listed as an isolated/lower-priority slip below since it's cross-document rather than within one text.

**5. `མ་ལུས་` → `үлдэлгүйгээр`.** Confirmed fixed. Zero occurrences of `мадаг`/`мадаггүй` anywhere in the three files (grepped directly). Three correct uses of `үлдэлгүйгээр` for `མ་ལུས་`/`མ་ལུས་པ` found in Le'u Dun ma (`^31`, `^33`, `^49`), all consistent with the glossary.

**6. Optatives (`ཤོག`, `གྱུར་ཅིག`) → `болтугай`.** The only Tibetan optatives in these three texts are the four `གྱུར་ཅིག` in `ཚད་མེད་བཞི།`, and all four are correctly rendered as `болтугай` wishes (`... болох болтугай`, `... хагацах болтугай`, `... үл хагацах болтугай`, `... орших болтугай`) — none flattened into statements. The two narrative texts use request/imperative verbs (`གསོལ་བ་འདེབས`, `བྱིན་གྱིས་རློབས`, `གསོལ`) rather than optative particles, and these are correctly rendered as first-person devotional acts (`... залбиран мөргөмүй`, `... адислан соёрх`) rather than mis-rendered as wishes — appropriate to the different Tibetan grammar, not an error.

**7. Recurring interjection consistency (new finding, same shape as the pilot's mantra-syllable issue).** The exclamation `ཨེ་མ་ཧོ` ("how wondrous!") appears in Le'u Dun ma as its own one-line block six times (embedded in `^1`, then standalone at `^5`, `^34`, `^61`, `^83`, `^104`, `^113`) — literally the same one-word Tibetan line each time. It surfaces as three different Mongolian spellings: `Эмахоо` (double о, blocks `^1`, `^5`), `Эмахо` (single о, blocks `^34`, `^61`, `^83`, `^104`), and `Эмахо.` (single о plus an added trailing period not in the other four identical renderings, block `^113`). Not wrong-script or mistranslated, but the same interjection should read one way throughout a single recitation text.

**8. Fidelity (omitted/invented clauses).** None found. Cross-checked Le'u Dun ma blocks `^4` (13-line lineage-supplication list), `^16`, `^54`, `^60`, `^103`, and `^131` against the DharmaMitra English baseline line by line — every clause present in both, nothing added, nothing dropped, proper-name lists fully accounted for one-to-one. Both `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།` and `ཚད་མེད་བཞི།` were read in full against their Tibetan and English baselines with no omissions or inventions found.

**9. Empty or duplicated lines.** None found. The only repeated lines in the corpus sample are Bar-chad-lam-sel's own 8-line refrain (`ཐུགས་རྗེས་བདག་ལ་བྱིན་གྱིས་རློབས...`), which recurs 12 times in the *Tibetan itself* and is correctly translated identically every time — a faithful repetition, not a padding artifact.

**10. Secular or Russian-flavored coinages.** None found. Grepped for common Russian/secular loan-roots (`медитаци-`, `религи-`, `духовн-`, `философи-`, `психологи-`, `теологи-`) across all three files — zero hits. The one incidental match, `Карма` in Le'u Dun ma `^15`, is the correct transliteration of the Karma buddha-family name (`ཀརྨ་རིགས`), parallel to the four other buddha-family names in the same passage (Vajra, Ratna, Padma, and this one) — not a mistranslated secular concept.

**11. Commentary or bracketed glosses.** None found. Grepped for brackets/parentheses in translated lines across all three files — no hits outside frontmatter.

## Isolated slips worth a human's eye (not systematic; low priority)

- `Дорждагвазэл` (Bar-chad-lam-sel `^17`) vs. `Дорж Дагбозалд` (Le'u Dun ma `^75`, `^88`) for the same secret name `རྡོ་རྗེ་དྲག་པོ་རྩལ` — cross-file only, each internally consistent within its own text.
- `Мипам номын хаан` (Le'u Dun ma `^4`) translates `མི་ཕམ་ཆོས་ཀྱི་རྒྱལ་པོ` descriptively ("Mipham, king of dharma") rather than transliterating the full name, while the adjacent line transliterates `Мипам Данбинима` for `མི་ཕམ་བསྟན་པའི་ཉི་མ`. A stylistic asymmetry, not an error — both preserve meaning.
- The poetic Amitābha epithet `སྣང་བ་མཐའ་ཡས` ("Boundless Light") is rendered descriptively as `Цаглашгүй гэрэлт(ийн)` in Bar-chad-lam-sel `^1` and Le'u Dun ma `^114`, rather than the pinned name `Авид` used elsewhere for the more common Tibetan spelling `འོད་དཔག་མེད`. Internally consistent with itself both times it occurs, and `Цаглашгүй гэрэлт` ("Infinite Light") is itself an attested Mongolian Amitābha epithet, so this reads as a defensible literal rendering of a different Tibetan name-string for the same deity, not a mistranslation — flagged only because it means the corpus names Amitābha two different ways depending on which Tibetan epithet the source text happens to use.

## Verdict

**ACCEPTABLE AS MACHINE BASELINE.** Every core criterion — script, line parity, fidelity to the Tibetan/English baseline, optative handling, absence of secular coinages or added commentary — is clean across all three texts. The only recurring issues found are narrow, glossary-fixable spelling-consistency gaps in proper names and interjections (the `сиди`/`сидди` mantra spelling, the `ཐོད་འཕྲེང་རྩལ` vs. `ཐོད་ཕྲེང་རྩལ` orthographic-variant gap in the name pinning, and the `Эмахо`/`Эмахоо` interjection), exactly the kind of issue the existing `glossary.tsv` mechanism is designed to absorb — not a defect in script, register, or overall terminology that would call for a `style.md` rewrite.
