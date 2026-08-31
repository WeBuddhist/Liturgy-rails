# Data-quality findings from the title-research pass

## Acted on
1. **Title concatenation** — `1-SOURCES/Text/སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ།.md`
   `title:` read `དམིགས་བརྩེ་མ།སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ།` — the title of a
   *different* note (`དམིགས་བརྩེ་མ།.md`) fused onto the front. Present in
   0-INBOX too, so it came from the backend fetch. Filename, H1 and author
   (Śāntideva) were all correct; only the field was wrong.
   FIXED in 1-SOURCES. 0-INBOX left as the verbatim intake record.
   >> The text was UPLOADED with the bad title: text_id 17Ui1qnL3NJCnEowPZ2ZQ,
      edition_id f7qs8kKZMFZ30ynqq7cif. Backend record needs the same fix.

## Flagged, not changed
2. **Stray genitive** — `འཕགས་པ་དཀོན་མཆོག་གསུམ་རྗེས་སུ་དྲན་པའི་གྱི་མདོ།`
   `པའི་གྱི་མདོ` is a double genitive; should read `རྗེས་སུ་དྲན་པའི་མདོ`.
   Appears in title, H1, FILENAME and the upload-ledger key, so it is the join
   key between note, translation, payload and backend. Fixing it needs a
   coordinated rename in all four places + the backend record.
   text_id N4loXiCK144VPVHVSJaUG, edition_id xdOKmSRBcOgrEBDPaVBRk.

3. **Authorship: `འཕགས་པ་བཀྲ་ཤིས་བརྒྱད་པ།`** — note credits
   `སྟོན་པ་ཤཀྱཱ་ཐུབ་པ།` (Buddha Śākyamuni). The incipit is Mipham's 1896 verses,
   not the sūtra (Toh 278). Attribution call for a human.
   (Also: its bdrc id `MW1KG2118_3795EA` is an M-prefixed manifestation id,
   unlike the WA/W ids used elsewhere.)

4. **Authorship: Cittamaṇi Tārā guru yoga** — note credits Takphu V Losang
   Chökyi Wangchuk (matches BDRC WA1KG4594); the published English edition
   credits Paṇchen Losang Chökyi Gyaltsen.

5. **Wrong context header on ALL 95 English translations** — verified from the
   ledgers, not inferred: every one of the 95 texts was sent
   `Work: བློ་སྦྱོང་ཚིག་བརྒྱད་མ། (author: གླང་རི་ཐང་པ།)` as its context line.
   Cause: dm_translate.py seeds ONE track-level context-header.md from whichever
   text runs first, then every later text reads it. Will repeat on the Chinese
   run unless fixed first. Task chip queued.

## Process note
Research agents hit a 200-call WebSearch cap and Chinese search engines were
largely CAPTCHA-gated. Unattested Chinese titles reflect reachability, not a
judgement that no title exists. The `zh_attested: false` flag marks them.

6. **Authorship: Zabtik Drolchok maṇḍala ritual** —
   `དགོངས་གཏེར་སྒྲོལ་མའི་ཟབ་ཏིག་ལས་མཎྜལ་ཆོ་ག་ཚོགས་གཉིས་སྙིང་པོ།` note credits
   Jigme Lingpa; Lotsawa House attributes the Zabtik Drolchok cycle to Chokgyur
   Dechen Lingpa, arranged by Jamgön Kongtrul. The heading also reads
   `མཎྜལ་ཆོ་ག` where Lotsawa House has `ཕྱི་སྒྲུབ་...ཆོ་ག`, so this may be a
   distinct recension rather than a straight error. Human call.

7. **Not an error, but worth recording** — `ཐབས་མཁས་ཐུགས་རྗེ་མ`'s double author
   field is correct: Nāgārjuna's Twelve Acts praise prefaced by a homage verse
   traditionally credited to Jikten Sumgön. The Chinese edition
   (釋迦牟尼佛禮讚文) credits both men the same way.

8. **Near-miss to avoid** — `ཇོ་བོ་རྗེའི་བསྟོད་པ་ཕུན་སུམ་ཚོགས་པ་མ...` is NOT
   Nagtso Lotsāwa's *Eighty Verses of Praise* to Atiśa, which opens differently.
   The two are easy to conflate and a search engine will offer the wrong one.
   No titled edition found in either language; both titles are ours.

9. **BLOCK MISALIGNMENT — `རྟེན་འབྲེལ་བསྟོད་པ།` (needs action)**
   During this session the source note changed body: a stray `ˌ` (U+02CC) that
   had been sitting on its own line after `མི་འགལ་འདུ་བ་སྨོས་ཅི་དགོས། །` was
   removed and that block gained `^19`, renumbering every later block +1.
   Source went 59 -> 60 block ids. I did not make this edit; my scripts only
   write frontmatter. The file is UNTRACKED in git (`??`).

   The edit is CORRECT in itself — `0-INBOX/རྟེན་འབྲེལ་བསྟོད་པ།.md` (ground
   truth) has no `ˌ`, so 1-SOURCES had a preparation artifact and now matches
   the inbox. I kept it rather than re-introducing the corruption.

   BUT it orphans the English translation, which still has 59 ids generated
   against the old numbering. Translation `^19`..`^59` now point one block
   earlier than the source blocks of the same id — 41 blocks misaligned, and
   `མི་འགལ་འདུ་བ་སྨོས་ཅི་དགོས། །` has never been translated at all.
   `--render-only` will NOT fix this: the ledger stores the old ids too.
   Repair = renumber ledger records ^19..^59 to ^20..^60, then translate the
   one new ^19 (1 API call). See `.claude/skills/dharmamitra-translate/scripts/dm_repair.py`.

10. **Stray U+02CC elsewhere** — `ཆོ་འཕྲུལ་གྱི་བསྟོད་པ།` also contains one, at
    the END of line 38 (`...ཕྱག་འཚལ་ལོ།།ˌ ^4`) rather than on its own line, so it
    does not break a block; source and translation are both 21 ids, aligned.
    It IS present in 0-INBOX, so it is in the upstream data. Cosmetic only.


## Upload schema (settled 2026-08-28)

The library follows **WEMI**: each translation is its own Expression, so it gets
its OWN text and edition, plus a segment-level alignment back to the Tibetan.
One rule holds in every file in the vault:

    text_id / edition_id                      THIS document's own ids
    translation_of_text_id / _edition_id      what it points at

A translation therefore carries the Tibetan ids as *pointers*, and its own
`text_id` / `edition_id` stay EMPTY until upload assigns them. An earlier version
of the stamping script wrote the Tibetan ids into the bare `text_id`/`edition_id`
keys, which claimed the translation *was* the Tibetan text and edition. Fixed;
`stamp_metadata.py --ids` now enforces the rule and never overwrites an id that
has actually been assigned.

**Segment alignment is block-id parity.** Translation block `^N` renders source
block `^N`, so the alignment payload is derivable with no extra bookkeeping —
provided the ids match 1:1. Current state: zh 95/95 aligned, en 94/95.

>> Finding 9 (`རྟེན་འབྲེལ་བསྟོད་པ།`) is therefore no longer cosmetic. Uploading
   that text's English translation as-is would emit a WRONG alignment: 41
   segments (`^19`..`^59`) each mapped to the Tibetan segment one place earlier,
   and one Tibetan segment with no translation at all. Fix the ledger numbering
   before that text is uploaded.


## Resolution of findings 9 & 10 (2026-08-28)

**`རྟེན་འབྲེལ་བསྟོད་པ།` — repaired, and the BACKEND WAS NEVER WRONG.**
The stray U+02CC sat where a blank line belonged, fusing two four-line verses
into one block. Removing it split the block in two, which is why the ledger was
one block short rather than merely renumbered. The merged block's existing
translation already contained both stanzas separated by a blank line, so
`4-SYSTEM/scripts/repair_split_block.py` split it on that boundary and renumbered
the rest — **zero API calls**. The script refuses to act unless
`merged == first + second` after normalisation, so it cannot guess.

Crucially: the uploaded payload for this text already had 60 segments and no
U+02CC. The corruption existed ONLY in the 1-SOURCES markdown, introduced after
the 08-26 payload build. The backend copy has been correct all along.

**Second note defect found and fixed.** `ཕ་དམ་པ་སངས་རྒྱས་...དིང་རི་བརྒྱ་རྩ་མ`
had lost the blank line between its H1 and the first paragraph. `build_payloads.py`
segments on blank lines, so a rebuild would have produced 53 segments instead of
the 54 that are in the backend — silently merging the title into the first
paragraph. Restored. It was the only note in the corpus with this defect.

## Backend state — verified, no re-upload needed

Comparing every stored payload (built 08-26 16:10, uploaded 08-26 17:00) against
the current notes:

    segment count matches uploaded payload : 95/95
    content matches uploaded payload       : 95/95
    en / zh block-id alignment             : 95/95 each

So no Tibetan edition needs deleting or re-uploading. Deleting one would also
churn its `edition_id`, invalidating the `translation_of_edition_id` now stamped
into 190 translation files and the ledger that maps them.

**The one real backend discrepancy is a TITLE, not segmentation.**
`སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ།` was uploaded as
`{"bo": "དམིགས་བརྩེ་མ།སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ།"}` — the concatenation from
finding 1. It needs a title update on the text record
(text_id 17Ui1qnL3NJCnEowPZ2ZQ), not an edition delete.
(The other 8 title differences are not defects: `build_payloads.py` strips the
ornamental `༄༅། །` prefix by design, so the backend correctly holds the clean form.)
