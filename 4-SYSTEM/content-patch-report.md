# In-place content patches — texts whose segments did not move

Generated 2026-09-16 12:37 by `4-SYSTEM/scripts/content_patch_payloads.py` with `--live`. Generated file — re-run the script rather than editing it.

The repeated title line is treated as already removed from 0-INBOX, per instruction: it is dropped from the inbox note before anything is compared. Nothing here has been sent to the backend.

## Summary

| verdict | texts | meaning |
|---|---|---|
| patch | 8 | segments identical; the character edits go in as `PATCH /v2/editions/{id}/content`, every block id and alignment survives |
| unchanged | 31 | content is byte-identical; no call at all |
| rebuild | 54 | a segment boundary or id moved; not patchable, needs delete + re-POST segmentation |
| blocked | 1 | the note cannot be stamped as it stands |
| **total** | **94** | |

**21 operations across 8 texts**, preserving 48 translation alignments. Payloads in `4-SYSTEM/scripts/payloads-content-patch/`.

## How each payload was proved safe

For every text the old edition is rebuilt from `1-SOURCES/Text/` through the uploader's own payload path, and the new one from the inbox note with ids stripped, the repeated title line dropped, then re-stamped. A text qualifies only if both have the same segments — same `reference`, same type, same number of line spans. The character difference is then reduced to minimal operations and the backend's **own** span arithmetic (`adjust_spans_for_*` in `database/span_database.py`, vendored verbatim) is replayed over the old spans. The payload is written only if the replayed spans come out equal, position for position, to the spans a fresh stamp of the new note produces.

With `--live`, each edition is also read back before being trusted: its content string, its segment shape and all its line spans must equal the local old side, so the offsets are stated against what is actually there.

## The patchable texts

| # | text | edition | chars | segments | ops | alignments kept | live checks |
|---|---|---|---|---|---|---|---|
| 1 | ཁྱུང་པོའི་སྨོན་ལམ། | `0c1XHW3suAPaH4KSpmq0E` | 1279 → 1281 | 8 | 1 | 6 | content+shape+spans ✓ |
| 2 | གསོལ་འདེབས་བར་ཆད་ལམ་སེལ། | `yMfZgziZceyB18W6it1Qh` | 6345 → 6346 | 25 | 1 | 6 | content+shape+spans ✓ |
| 3 | གསོལ་འདེབས་བསམ་པ་མྱུར་འགྲུབ་མ། | `3Oub45BTdTJaLUyBCZcNS` | 1057 → 1059 | 6 | 1 | 6 | content+shape+spans ✓ |
| 4 | གསོལ་འདེབས་ལེའུ་བདུན་མ། | `ekv4YsfghJab1lrxoHEy0` | 21565 → 21733 | 132 | 14 | 6 | content+shape+spans ✓ |
| 5 | ཇ་མཆོད་བདེ་ཆེན་ཀུན་བཟང་མ་བཞུགས་སོ། | `yqU91NSKMdzDEyMtJb9Kj` | 1194 → 1196 | 9 | 1 | 6 | content+shape+spans ✓ |
| 6 | ཐུབ་བསྟན་རིས་མེད་རྒྱས་པའི་སྨོན་ལམ། | `jMZ74sGpazU4CDbLhGoOQ` | 3692 → 3694 | 24 | 1 | 6 | content+shape+spans ✓ |
| 7 | དགའ་ལྡན་ལྷ་བརྒྱ་མ་འདོད་གསོལ་སྨོན་ལམ་དང་བཅས་པ། | `9HPXahDQ9ptYjc0QmmxjJ` | 3509 → 3511 | 23 | 1 | 6 | content+shape+spans ✓ |
| 8 | དགེ་སློང་མ་དཔལ་མོས་མཛད་པའི་འཕགས་པ་སྤྱན་རས་གཟིགས་དབང་ཕྱུག་གི་བསྟོད་པ། | `VfsjlMbI79VL5bTOtaNzV` | 1902 → 1904 | 12 | 1 | 6 | content+shape+spans ✓ |

## Every operation

`«…»` is the range the operation covers in the content as it stands now. Send them per text in the order listed — descending by position, so no offset is invalidated by an earlier call.

### ཁྱུང་པོའི་སྨོན་ལམ།

`PATCH /v2/editions/0c1XHW3suAPaH4KSpmq0E/content` × 1 · 1279 → 1281 chars · 6 alignments kept

| # | op | body | in | was → now | context |
|---|---|---|---|---|---|
| 1 | insert | `position` 22 | `^0` (title) | → `། ` | `…པོའི་སྨོན་ལམ«»།སྐུ་གསུམ་མཁ…` |

### གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།

`PATCH /v2/editions/yMfZgziZceyB18W6it1Qh/content` × 1 · 6345 → 6346 chars · 6 alignments kept

| # | op | body | in | was → now | context |
|---|---|---|---|---|---|
| 1 | insert | `position` 29 | `^0` (title) | → ` ` | `…ར་ཆད་ལམ་སེལ།«»།ཨོཾ་ཨཱཿཧཱུྃ…` |

### གསོལ་འདེབས་བསམ་པ་མྱུར་འགྲུབ་མ།

`PATCH /v2/editions/3Oub45BTdTJaLUyBCZcNS/content` × 1 · 1057 → 1059 chars · 6 alignments kept

| # | op | body | in | was → now | context |
|---|---|---|---|---|---|
| 1 | insert | `position` 34 | `^0` (title) | → `། ` | `…མྱུར་འགྲུབ་མ«»།ཨེ་མ་ཧོ།མཚོ…` |

### གསོལ་འདེབས་ལེའུ་བདུན་མ།

`PATCH /v2/editions/ekv4YsfghJab1lrxoHEy0/content` × 14 · 21565 → 21733 chars · 6 alignments kept

| # | op | body | in | was → now | context |
|---|---|---|---|---|---|
| 1 | replace | `start` 956 `end` 957 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…ྩ་བའི་བླ་མ་ལ«༴»མཆོག་དང་ཐུན་…` |
| 2 | replace | `start` 934 `end` 935 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…ང་རྣམ་རྒྱལ་ལ«༴»དྲིན་ཅན་རྩ་བ…` |
| 3 | replace | `start` 907 `end` 908 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…ན་པའི་ཉི་མ་ལ«༴»རྒྱལ་སྲས་ངག་…` |
| 4 | replace | `start` 885 `end` 886 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…ྱི་རྒྱལ་པོ་ལ«༴»མི་ཕམ་བསྟན་པ…` |
| 5 | replace | `start` 861 `end` 862 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…ི་དབང་ཕྱུག་ལ«༴»མི་ཕམ་ཆོས་ཀྱ…` |
| 6 | replace | `start` 834 `end` 835 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…ཁྲི་བཙན་པོ་ལ«༴»རིག་འཛིན་གར་…` |
| 7 | replace | `start` 811 `end` 812 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…བདུད་འཇོམས་ལ«༴»ལྷ་སྲས་མུ་ཁྲ…` |
| 8 | replace | `start` 784 `end` 785 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…ས་མཚོ་རྒྱལ་ལ«༴»སྣ་ནམ་རྡོ་རྗ…` |
| 9 | replace | `start` 757 `end` 758 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…ོང་ལྡེ་བཙན་ལ«༴»མཁའ་འགྲོ་ཡེ་…` |
| 10 | replace | `start` 729 `end` 730 | `^4` (verse) | `༴` → `་གསོལ་བ་འདེབས༔` | `…འི་སྙིང་པོ་ལ«༴»ཆོས་རྒྱལ་ཁྲི…` |
| 11 | replace | `start` 701 `end` 703 | `^4` (verse) | `༴།` → `་གསོལ་བ་འདེབས༔` | `…་འབྱུང་གནས་ལ«༴།»དགེ་སློང་ནམ་…` |
| 12 | replace | `start` 676 `end` 678 | `^4` (verse) | `༴།` → `་གསོལ་བ་འདེབས༔` | `…ུམ་མགོན་པོ་ལ«༴།»ཨུ་རྒྱན་པདྨ་…` |
| 13 | replace | `start` 645 `end` 647 | `^4` (verse) | `༴།` → `་གསོལ་བ་འདེབས༔` | `…་བ་རིགས་ལྔ་ལ«༴།»སྤྲུལ་སྐུ་རི…` |
| 14 | insert | `position` 27 | `^0` (title) | → `། ` | `…་ལེའུ་བདུན་མ«»།ཨེ་མ་ཧོ༔སྤྲ…` |

### ཇ་མཆོད་བདེ་ཆེན་ཀུན་བཟང་མ་བཞུགས་སོ།

`PATCH /v2/editions/yqU91NSKMdzDEyMtJb9Kj/content` × 1 · 1194 → 1196 chars · 6 alignments kept

| # | op | body | in | was → now | context |
|---|---|---|---|---|---|
| 1 | insert | `position` 38 | `^0` (title) | → `། ` | `…ང་མ་བཞུགས་སོ«»།རང་ལྷར་གསལ་…` |

### ཐུབ་བསྟན་རིས་མེད་རྒྱས་པའི་སྨོན་ལམ།

`PATCH /v2/editions/jMZ74sGpazU4CDbLhGoOQ/content` × 1 · 3692 → 3694 chars · 6 alignments kept

| # | op | body | in | was → now | context |
|---|---|---|---|---|---|
| 1 | insert | `position` 38 | `^0` (title) | → `། ` | `…་པའི་སྨོན་ལམ«»།སྐུ་བཞིའི་བ…` |

### དགའ་ལྡན་ལྷ་བརྒྱ་མ་འདོད་གསོལ་སྨོན་ལམ་དང་བཅས་པ།

`PATCH /v2/editions/9HPXahDQ9ptYjc0QmmxjJ/content` × 1 · 3509 → 3511 chars · 6 alignments kept

| # | op | body | in | was → now | context |
|---|---|---|---|---|---|
| 1 | insert | `position` 50 | `^0` (title) | → `། ` | `…་ལམ་དང་བཅས་པ«»།ན་མོ་གུ་རུ་…` |

### དགེ་སློང་མ་དཔལ་མོས་མཛད་པའི་འཕགས་པ་སྤྱན་རས་གཟིགས་དབང་ཕྱུག་གི་བསྟོད་པ།

`PATCH /v2/editions/VfsjlMbI79VL5bTOtaNzV/content` × 1 · 1902 → 1904 chars · 6 alignments kept

| # | op | body | in | was → now | context |
|---|---|---|---|---|---|
| 1 | insert | `position` 67 | `^0` (title) | → `། ` | `…ག་གི་བསྟོད་པ«»།པོ་བསྟོད་བཞ…` |

