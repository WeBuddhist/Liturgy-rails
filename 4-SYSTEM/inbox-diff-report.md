# 0-INBOX vs 1-SOURCES/Text — what the experts changed

Generated 2026-09-15 15:30 by `4-SYSTEM/scripts/inbox_diff.py` at vault commit `2034652`. Block ids are stripped before comparing; pipeline-owned frontmatter keys are ignored. Generated file — re-run the script rather than editing it.

## Summary

| verdict | as the inbox stands | with the repeated title line set aside |
|---|---|---|
| unchanged | 0 | 31 |
| patch | 0 | 8 |
| rebuild | 93 | 54 |
| blocked | 1 | 1 |
| **compared** | 94 | 94 |

Not compared: 33 inbox notes with no source note (the backlog) and 1 retired note.

- **unchanged** — no heading, block, line or character differs once ids are stripped (at most the bytes of a blank line), and no expert-owned frontmatter key differs.
- **patch** — only in-place character edits. The backend takes each as one content operation and shifts every span itself; the six translation alignments survive.
- **rebuild** — a block boundary, heading or block id moved. The segmentation has to be deleted and re-posted, which drops every alignment on the edition until each is PUT again.
- **blocked** — the inbox note cannot be stamped as it stands; see *Defects*.

### Change types, by number of texts affected

| change | texts |
|---|---|
| title repeated as first body line | 94 |
| heading added | 55 |
| H1 punctuation | 18 |
| H1 whitespace | 4 |
| segment added | 1 |
| text changed (letters) | 1 |
| line breaks moved | 1 |
| punctuation only | 1 |
| whitespace only | 1 |
| frontmatter (expert-owned keys) | 1 |

### The two corpus-wide edits

**Title repeated as the first body line — 94 of 94 texts.** Under the `# ༄༅། །Title` heading the inbox now carries the same title again as a plain one-line segment. If stamped as-is it becomes a new block (`^1` in flat texts, `^0-1` under a heading), every later id shifts by one, and the uploaded content would carry the title twice (the H1 already becomes the `title` segment). The second column of every table below shows what remains once this edit is set aside.

**Colophon headings added — 55 texts.** A flat text that gains a `##` heading switches id scheme (`^n` → `^0-n`, `^1-0`, `^1-1-1`…), so every id in it is renumbered even though not one word changed. Variants seen:

| headings added | texts |
|---|---|
| `## མཇུག་བྱང་།` + `### མཛད་བྱང་།` | 39 |
| `## མཇུག་བྱང་།` | 13 |
| `### མཛད་བྱང་།` | 1 — གཏོར་མ་ཆ་གསུམ་བཞུགས་སོ། |
| `## མཇུག་བྱང་།` + `### མཛད་བྱང་ས།` | 1 — ཆོ་འཕྲུལ་གྱི་བསྟོད་པ། |
| `## མཇུག་བྱང་།` + `### མཛུད་བྱང་།` | 1 — བོད་ཡུལ་བདེ་བའི་སྨོན་ལམ། |

### Block-id impact — as the inbox stands

- 94 of 94 texts get different ids if 0-INBOX is re-stamped (ids are the segment references the translation alignments point at).
- 54 texts change id scheme (flat `^n` → sectioned `^k-n`).
- Alignments to re-PUT: 558.

### Block-id impact — with the title line set aside

- 55 of 94 texts get different ids if 0-INBOX is re-stamped (ids are the segment references the translation alignments point at).
- 54 texts change id scheme (flat `^n` → sectioned `^k-n`).
- Alignments to re-PUT: 330.

1 inbox note(s) would be refused by `block_ids.py stamp` as they stand — see *Defects*.

### Live check — `GET /v2/editions/{id}/content` against the source note

- matches source: 93
- DIFFERS from source (6975 vs 6974 chars): …ས་ཅི་དགོས། །[-ˌ-]བརྟེན་ནས་འབྱ…: 1

## Every text

Backend-work codes: **M** `PATCH /v2/texts` for metadata · **M!** edition metadata, no endpoint · **P*n*** *n* content patches, alignments kept · **R** delete + re-post segmentation · **A*n*** re-PUT *n* translation alignments · **T** post a table of contents · **X** blocked by a defect.

| # | text (source stem) | verdict | what changed | ids kept | work | verdict w/o title line | ids kept | work |
|---|---|---|---|---|---|---|---|---|
| 1 | གཏོར་མ་ཆ་གསུམ་བཞུགས་སོ། | blocked | title repeated as first body line; segment added; heading added | 0/48 | X | blocked | 0/48 | X |
| 2 | ཆགས་མེད་བདེ་སྨོན། | rebuild | heading added ×2; H1 whitespace; title repeated as first body line | 1/86 | R+A6 T | rebuild | 1/86 | R+A6 T |
| 3 | ཆོ་འཕྲུལ་གྱི་བསྟོད་པ། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/21 | R+A6 T | rebuild | 1/21 | R+A6 T |
| 4 | ཇ་མཆོད་གཙུག་གི་ནོར་བུ་བཞུགས་སོ། ། | rebuild | heading added ×2; title repeated as first body line | 1/13 | R+A6 T | rebuild | 1/13 | R+A6 T |
| 5 | ཏཱ་ཡི་སི་ཏུ་རིམ་པར་བྱོན་པ་རྣམས་ཀྱི་གསོལ་འདེབས། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/12 | R+A6 T | rebuild | 1/12 | R+A6 T |
| 6 | ཐབས་མཁས་ཐུགས་རྗེ་མ་བཞུགས་སོ། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/20 | R+A6 T | rebuild | 1/20 | R+A6 T |
| 7 | ཐུབ་པའི་བསྟོད་པ་གང་ཚེ་རྐང་གཉིས་མ། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/9 | R+A6 T | rebuild | 1/9 | R+A6 T |
| 8 | ཐུབ་པའི་བསྟོད་པ་ཐུབ་རྣམས་སྤངས་རྟོགས། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/19 | R+A6 T | rebuild | 1/19 | R+A6 T |
| 9 | ཐུབ་པའི་མཛད་པ་བཅུ་གཉིས་ལ་བསྟོད་པ་ཞེས་བྱ་བ། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/17 | R+A6 T | rebuild | 1/17 | R+A6 T |
| 10 | ཐོག་མཐའ་མ་བཞུགས་སོ། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/33 | R+A6 T | rebuild | 1/33 | R+A6 T |
| 11 | དགོངས་གཅིག་ལྷན་ཐབས་བཞུགས་སོ། | rebuild | heading added ×2; H1 whitespace; title repeated as first body line | 1/18 | R+A6 T | rebuild | 1/18 | R+A6 T |
| 12 | དཔལ་གསང་བ་འདུས་པའི་བསྒོམ་བཟླས་རྒྱུན་འཁྱེར་བཞུགས་སོ། ། | rebuild | heading added ×2; title repeated as first body line | 1/24 | R+A6 T | rebuild | 1/24 | R+A6 T |
| 13 | དཔལ་ནཱ་ལེནྡྲའི་པཎ་གྲུབ་བཅུ་བདུན་གྱི་གསོལ་འདེབས། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/27 | R+A6 T | rebuild | 1/27 | R+A6 T |
| 14 | དཔལ་ལྡན་ས་གསུམ་མ། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/40 | R+A6 T | rebuild | 1/40 | R+A6 T |
| 15 | དཔལ་ས་སྐྱ་པའི་བསྟན་པ་དར་ཞིང་རྒྱས་པའི་སྨོན་ལམ་འཇམ་དབྱངས་བླ་མ་དགྱེས་པའི་ཞལ་ལུང་ཞེས་བྱ་བ་བཞུགས་སོ། ། | rebuild | heading added ×2; title repeated as first body line; line breaks moved; punctuation only | 1/29 | R+A6 T | rebuild | 1/29 | R+A6 T |
| 16 | དབང་སྡུད་གསོལ་འདེབས། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/9 | R+A6 T | rebuild | 1/9 | R+A6 T |
| 17 | དབྱངས་ཅན་མའི་བསྟོད་པ་བཞུགས་སོ། | rebuild | heading added ×2; H1 punctuation; title repeated as first body line | 1/6 | R+A6 T | rebuild | 1/6 | R+A6 T |
| 18 | དུས་མཁྱེན་གྱི་རྣམ་ཐར་བསྟོད་པ། | rebuild | heading added ×2; title repeated as first body line | 1/19 | R+A6 T | rebuild | 1/19 | R+A6 T |
| 19 | པདྨ་མཁའ་འགྲོའི་རིགས་བྱེད་རྩལ་གྱི་བསང་མཆོད་པདྨའི་དྲྭ་བ་བཞུགས་སོ། | rebuild | heading added ×2; title repeated as first body line | 1/17 | R+A6 T | rebuild | 1/17 | R+A6 T |
| 20 | ཕ་དམ་པ་སངས་རྒྱས་ཀྱི་ཞལ་གདམས་དིང་རི་བརྒྱ་རྩ་མ་བཞུགས་སོ། | rebuild | heading added ×2; H1 whitespace; title repeated as first body line | 1/54 | R+A6 T | rebuild | 1/54 | R+A6 T |
| 21 | ཕྱག་ཆེན་བརྒྱུད་པའི་གསོལ་འདེབས་ནི། | rebuild | heading added ×2; title repeated as first body line | 1/21 | R+A6 T | rebuild | 1/21 | R+A6 T |
| 22 | བཀའ་ཐང་བསྡུས་པ། | rebuild | title repeated as first body line; heading added | 1/26 | R+A6 T | rebuild | 1/26 | R+A6 T |
| 23 | བདུད་བཟློག་གསང་བའི་མན་ངག | rebuild | title repeated as first body line; heading added | 1/9 | R+A6 T | rebuild | 1/9 | R+A6 T |
| 24 | བདེ་སྨོན་བསྡུས་པ། | rebuild | title repeated as first body line; heading added | 1/6 | R+A6 T | rebuild | 1/6 | R+A6 T |
| 25 | བསྔོ་བ་དང་སྨོན་ལམ་བསྡུས་པ་བཞུགས་སོ། | rebuild | heading added ×2; title repeated as first body line | 1/13 | R+A6 T | rebuild | 1/13 | R+A6 T |
| 26 | བོད་ཡུལ་བདེ་བའི་སྨོན་ལམ། | rebuild | heading added ×2; title repeated as first body line | 1/7 | R+A6 T | rebuild | 1/7 | R+A6 T |
| 27 | བོད་སྐྱོང་ལྷ་སྲུང་གི་འཕྲིན་བསྐུལ། | rebuild | heading added ×2; title repeated as first body line | 1/7 | R+A6 T | rebuild | 1/7 | R+A6 T |
| 28 | བྱང་ཆུབ་སེམས་དཔའི་ལྟུང་བ་བཤགས་པ། | rebuild | title repeated as first body line; heading added | 1/10 | R+A6 T | rebuild | 1/10 | R+A6 T |
| 29 | བྱམས་པའི་སྐུ་གཟུགས་མ་བཞུགས་སོ།། | rebuild | heading added ×2; title repeated as first body line | 1/9 | R+A6 T | rebuild | 1/9 | R+A6 T |
| 30 | བྱིས་པའི་གདོན་ཆེན་བཅོ་ལྔ་ཞི་བར་བྱེད་པའི་གཟུངས་བཞུགས་སོ། | rebuild | title repeated as first body line; heading added | 1/44 | R+A6 T | rebuild | 1/44 | R+A6 T |
| 31 | བྱིས་པའི་འབུམ་ཆུང་བཞུགས་སོ།། | rebuild | title repeated as first body line; heading added | 1/10 | R+A6 T | rebuild | 1/10 | R+A6 T |
| 32 | བླ་མ་རྒྱང་འབོད་མོས་གུས་སྙིང་གི་གཟེར་འདེབས་བཞུགས་སོ། | rebuild | heading added ×2; title repeated as first body line | 1/55 | R+A6 T | rebuild | 1/55 | R+A6 T |
| 33 | བློ་སྦྱོང་ཚིག་བརྒྱད་མ། | rebuild | heading added ×2; title repeated as first body line | 1/11 | R+A6 T | rebuild | 1/11 | R+A6 T |
| 34 | མཁས་གྲུབ་རྗེའི་བསྟོད་པ། | rebuild | heading added ×2; title repeated as first body line | 1/9 | R+A6 T | rebuild | 1/9 | R+A6 T |
| 35 | མགོན་པོ་ཕྱག་དྲུག་པའི་བསྟོད་པ་མྱུར་མཛད་མ། | rebuild | heading added ×2; title repeated as first body line | 1/7 | R+A6 T | rebuild | 1/7 | R+A6 T |
| 36 | ཚེ་རབས་རྗེས་འཛིན་བཞུགས་སོ། | rebuild | heading added ×2; title repeated as first body line | 1/9 | R+A6 T | rebuild | 1/9 | R+A6 T |
| 37 | ཚེས་བཅུའི་ཕན་ཡོན་གསོལ་འདེབས། | rebuild | heading added ×2; title repeated as first body line | 1/15 | R+A6 T | rebuild | 1/15 | R+A6 T |
| 38 | ཞབས་བརྟན་གསོལ་འདེབས་འཆི་མེད་གྲུབ་པ་ཞེས་བྱ་བ་བཞུགས་སོ། | rebuild | heading added ×2; title repeated as first body line | 1/16 | R+A6 T | rebuild | 1/16 | R+A6 T |
| 39 | ཞབས་བརྟན་ནུབ་ཕྱོགས་བདེ་ལྡན་མ་བཞུགས་སོ།། | rebuild | heading added ×2; title repeated as first body line | 1/7 | R+A6 T | rebuild | 1/7 | R+A6 T |
| 40 | འཆི་ཁར་ཕན་པའི་གདམས་ངག་ཉམས་ལེན་གྱི་སྙིང་པོ་ཞེས་བྱ་བ་བཞུགས་སོ།། | rebuild | heading added ×2; title repeated as first body line | 1/10 | R+A6 T | rebuild | 1/10 | R+A6 T |
| 41 | འཇམ་དཔལ་རྫོགས་པ་ཆེན་པོའི་སྨོན་ལམ། | rebuild | heading added ×2; title repeated as first body line | 1/22 | R+A6 T | rebuild | 1/22 | R+A6 T |
| 42 | འཕགས་པ་བཟང་པོ་སྤྱོད་པའི་སྨོན་ལམ་གྱི་རྒྱལ་པོ། | rebuild | title repeated as first body line; heading added | 1/67 | R+A6 T | rebuild | 1/67 | R+A6 T |
| 43 | རི་བོ་བསངས་མཆོད་བཞུགས་སོ༔ | rebuild | title repeated as first body line; heading added | 1/18 | R+A6 T | rebuild | 1/18 | R+A6 T |
| 44 | རྒྱ་ནག་པོའི་སྐག་ཟློག་ཅེས་བྱ་བ་བཞུགས་སོ།། | rebuild | title repeated as first body line; heading added | 1/50 | R+A6 T | rebuild | 1/50 | R+A6 T |
| 45 | རྒྱལ་ཁམས་བདེ་བའི་སྨོན་ལམ། | rebuild | heading added ×2; title repeated as first body line | 1/5 | R+A6 T | rebuild | 1/5 | R+A6 T |
| 46 | རྒྱལ་བའི་དབང་པོ་ཀློང་ཆེན་རབ་འབྱམས་ལ་བསྟོད་པ། | rebuild | heading added ×2; title repeated as first body line | 1/16 | R+A6 T | rebuild | 1/16 | R+A6 T |
| 47 | རླུང་རྟ་ཡར་བསྐྱེད་བསངས་མཆོད་བཞུགས་སོ། | rebuild | title repeated as first body line; heading added | 1/16 | R+A6 T | rebuild | 1/16 | R+A6 T |
| 48 | ལམ་གཙོ་རྣམ་གསུམ། | rebuild | heading added ×2; title repeated as first body line | 1/17 | R+A6 T | rebuild | 1/17 | R+A6 T |
| 49 | ལམ་རིམ་སྨོན་ལམ་བཞུགས་སོ། | rebuild | heading added ×2; title repeated as first body line | 1/9 | R+A6 T | rebuild | 1/9 | R+A6 T |
| 50 | སྒྲོལ་བསྟོད་སྐྱབས་བདུན་མ། | rebuild | heading added ×2; title repeated as first body line | 1/9 | R+A6 T | rebuild | 1/9 | R+A6 T |
| 51 | སྒྲོལ་མ་ཉེར་གཅིག་ལ་བསྟོད་པ། | rebuild | heading added ×2; title repeated as first body line | 1/30 | R+A6 T | rebuild | 1/30 | R+A6 T |
| 52 | སྒྲོལ་མ་ཙིཏྟཱ་མ་ཎི་ལ་བརྟེན་པའི་ཐུན་མོང་མ་ཡིན་པའི་བླ་མའི་རྣལ་འབྱོར་ཐར་པར་བགྲོད་པའི་ཐེམ་སྐས་ཞེས་བྱ་བ་བཞུགས་སོ། ། | rebuild | title repeated as first body line; heading added | 1/12 | R+A6 T | rebuild | 1/12 | R+A6 T |
| 53 | སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ། | rebuild | title repeated as first body line; heading added; metadata: title | 1/57 | M R+A6 T | rebuild | 1/57 | M R+A6 T |
| 54 | སྨོན་ལམ་རྡོ་རྗེའི་རྒྱ་མདུད་ནི། | rebuild | heading added ×2; title repeated as first body line; whitespace only | 1/11 | R+A6 T | rebuild | 1/11 | R+A6 T |
| 55 | ཨོ་རྒྱན་རིན་པོ་ཆེའི་ཞལ་ཆེམས་གསོལ་འདེབས་བཞུགས༔ | rebuild | title repeated as first body line; heading added | 1/9 | R+A6 T | rebuild | 1/9 | R+A6 T |
| 56 | ཁྱུང་པོའི་སྨོན་ལམ། | rebuild | H1 punctuation; title repeated as first body line | 1/8 | R+A6 | patch | 8/8 | P1 |
| 57 | གསོལ་འདེབས་བར་ཆད་ལམ་སེལ། | rebuild | H1 whitespace; title repeated as first body line | 1/25 | R+A6 | patch | 25/25 | P1 |
| 58 | གསོལ་འདེབས་བསམ་པ་མྱུར་འགྲུབ་མ། | rebuild | H1 punctuation; title repeated as first body line | 1/6 | R+A6 | patch | 6/6 | P1 |
| 59 | གསོལ་འདེབས་ལེའུ་བདུན་མ། | rebuild | H1 punctuation; title repeated as first body line; text changed (letters) | 1/132 | R+A6 | patch | 132/132 | P14 |
| 60 | ཇ་མཆོད་བདེ་ཆེན་ཀུན་བཟང་མ་བཞུགས་སོ། | rebuild | H1 punctuation; title repeated as first body line | 1/9 | R+A6 | patch | 9/9 | P1 |
| 61 | ཐུབ་བསྟན་རིས་མེད་རྒྱས་པའི་སྨོན་ལམ། | rebuild | H1 punctuation; title repeated as first body line | 1/24 | R+A6 | patch | 24/24 | P1 |
| 62 | དགའ་ལྡན་ལྷ་བརྒྱ་མ་འདོད་གསོལ་སྨོན་ལམ་དང་བཅས་པ། | rebuild | H1 punctuation; title repeated as first body line | 1/23 | R+A6 | patch | 23/23 | P1 |
| 63 | དགེ་སློང་མ་དཔལ་མོས་མཛད་པའི་འཕགས་པ་སྤྱན་རས་གཟིགས་དབང་ཕྱུག་གི་བསྟོད་པ། | rebuild | H1 punctuation; title repeated as first body line | 1/12 | R+A6 | patch | 12/12 | P1 |
| 64 | ཇོ་བོ་རྗེའི་བསྟོད་པ་ཕུན་སུམ་ཚོགས་པ་མ་བཞུགས་སོ། | rebuild | title repeated as first body line | 1/37 | R+A6 | unchanged | 37/37 | — |
| 65 | ཐུགས་རྗེ་ཆེན་པོའི་བསྒོམ་བཟླས་འགྲོ་དོན་མཁའ་ཁྱབ་མ་བཞུགས་སོ། ། | rebuild | title repeated as first body line | 1/26 | R+A6 | unchanged | 26/26 | — |
| 66 | དགོངས་གཏེར་སྒྲོལ་མའི་ཟབ་ཏིག་ལས་མཎྜལ་ཆོ་ག་ཚོགས་གཉིས་སྙིང་པོ། | rebuild | title repeated as first body line | 1/50 | R+A6 | unchanged | 50/50 | — |
| 67 | དམིགས་བརྩེ་མ། | rebuild | title repeated as first body line | 1/2 | R+A6 | unchanged | 2/2 | — |
| 68 | བདེན་ཚིག་སྨོན་ལམ། | rebuild | title repeated as first body line | 1/10 | R+A6 | unchanged | 10/10 | — |
| 69 | བསམ་པ་ལྷུན་གྲུབ་མ་བཞུགས་སོ། | rebuild | title repeated as first body line | 1/19 | R+A6 | unchanged | 19/19 | — |
| 70 | བསྟན་འབར་མ་བཞུགས་སོ། | rebuild | title repeated as first body line | 1/20 | R+A6 | unchanged | 20/20 | — |
| 71 | བྱམས་པའི་སྨོན་ལམ། | rebuild | title repeated as first body line | 1/28 | R+A6 | unchanged | 28/28 | — |
| 72 | མཎྜལ། | rebuild | title repeated as first body line | 1/8 | R+A6 | unchanged | 8/8 | — |
| 73 | མར་མེའི་སྨོན་ལམ། | rebuild | title repeated as first body line | 1/4 | R+A6 | unchanged | 4/4 | — |
| 74 | མི་ཁའི་བཟློག་བསྒྱུར། | rebuild | title repeated as first body line | 1/76 | R+A6 | unchanged | 76/76 | — |
| 75 | མྱུར་མཛད་རྣམ་གསུམ་བཞུགས་སོ། | rebuild | title repeated as first body line | 1/10 | R+A6 | unchanged | 10/10 | — |
| 76 | ཚད་མེད་བཞི། | rebuild | title repeated as first body line | 1/2 | R+A6 | unchanged | 2/2 | — |
| 77 | ཚིག་བདུན་གསོལ་འདེབས། | rebuild | title repeated as first body line | 1/2 | R+A6 | unchanged | 2/2 | — |
| 78 | འཇམ་དབྱངས་ཀྱི་བསྟོད་པ་གང་བློ་མ་བཞུགས་སོ། | rebuild | title repeated as first body line | 1/6 | R+A6 | unchanged | 6/6 | — |
| 79 | འཇམ་མགོན་བླ་མ་ཙོང་ཁ་པ་ཆེན་པོས་མཛད་པའི་བློ་སྦྱོང་སྙན་ངག་སྒྲ་རྒྱན་བཞུགས་སོ། | rebuild | title repeated as first body line | 1/28 | R+A6 | unchanged | 28/28 | — |
| 80 | འཕགས་པ་ཐུགས་རྗེ་ཆེན་པོ་ལ་བསྟོད་ཅིང་གསོལ་བ་འདེབས་པ་ཕན་བདེའི་ཆར་འབེབས་ཞེས་བྱ་བ་བཞུགས་སོ། | rebuild | title repeated as first body line | 1/28 | R+A6 | unchanged | 28/28 | — |
| 81 | འཕགས་པ་དཀོན་མཆོག་གསུམ་རྗེས་སུ་དྲན་པའི་གྱི་མདོ། | rebuild | title repeated as first body line | 1/5 | R+A6 | unchanged | 5/5 | — |
| 82 | འཕགས་པ་བཀྲ་ཤིས་བརྒྱད་པ། | rebuild | title repeated as first body line | 1/11 | R+A6 | unchanged | 11/11 | — |
| 83 | འཕགས་པ་སྤྱན་རས་གཟིགས་ཀྱི་མཚན་སྔགས། | rebuild | title repeated as first body line | 1/4 | R+A6 | unchanged | 4/4 | — |
| 84 | ཡན་ལག་བདུན་པ། | rebuild | title repeated as first body line | 1/13 | R+A6 | unchanged | 13/13 | — |
| 85 | ཡོན་ཏན་གཞིར་གྱུར་མ་བཞུགས་སོ། | rebuild | title repeated as first body line | 1/15 | R+A6 | unchanged | 15/15 | — |
| 86 | རྒྱན་དྲུག་མཆོག་གཉིས་ཀྱི་བསྟོད་པ་མཁའ་མཉམ་མ། | rebuild | title repeated as first body line | 1/11 | R+A6 | unchanged | 11/11 | — |
| 87 | རྒྱལ་བ་ཚེ་དཔག་མེད་ཀྱི་མཚན་སྔགས། | rebuild | title repeated as first body line | 1/4 | R+A6 | unchanged | 4/4 | — |
| 88 | རྗེ་གསང་བའི་རྣམ་ཐར། | rebuild | title repeated as first body line | 1/52 | R+A6 | unchanged | 52/52 | — |
| 89 | རྟེན་འབྲེལ་བསྟོད་པ། | rebuild | title repeated as first body line | 1/60 | R | unchanged | 60/60 | — |
| 90 | ལྷ་མོར་བསྟོད་པ་ཡན་ལག་བདུན་པ། | rebuild | title repeated as first body line | 1/8 | R+A6 | unchanged | 8/8 | — |
| 91 | སངས་རྒྱས་ཆོས་ཚོགས་མ། | rebuild | title repeated as first body line | 1/2 | R+A6 | unchanged | 2/2 | — |
| 92 | སྟོན་པ་ཐུབ་པའི་དབང་པོར་བསྟོད་པ། | rebuild | title repeated as first body line | 1/23 | R+A6 | unchanged | 23/23 | — |
| 93 | སློབ་དཔོན་ཐུགས་རྗེ་ཅན་གྱི་ཐུགས་དམ་གནད་ནས་སྐུལ་བའི་གདུང་དབྱངས་གསོལ་འདེབས་བཞུགས་སོ། ། | rebuild | title repeated as first body line | 1/9 | R+A6 | unchanged | 9/9 | — |
| 94 | སློབ་དཔོན་རིན་པོ་ཆེའི་མཚན་སྔགས། | rebuild | title repeated as first body line | 1/4 | R+A6 | unchanged | 4/4 | — |

## Defects to hand back to the expert

- **གཏོར་མ་ཆ་གསུམ་བཞུགས་སོ།** — line 206: heading without a space after the hashes: '##མཇུག་བྱང་།'
- **གཏོར་མ་ཆ་གསུམ་བཞུགས་སོ།** — block_ids would refuse to stamp this file: H3 appears before any H2
- **སློབ་དཔོན་ཐུགས་རྗེ་ཅན་གྱི་ཐུགས་དམ་གནད་ནས་སྐུལ་བའི་གདུང་དབྱངས་གསོལ་འདེབས་བཞུགས་སོ། །** — inbox note carries block ids of its own (stripped before comparing; 0-INBOX notes must not carry ids)

## Frontmatter changes

| text | key | change | old | new | goes to |
|---|---|---|---|---|---|
| སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ། | `title` | changed | སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ། | དམིགས་བརྩེ་མ།སྤྱོད་འཇུག་སྨོན་ལམ་བཞུགས་སོ། | text |

## Detail — everything beyond the two corpus-wide edits

`[-old-]{+new+}` inside a dozen characters of context; `⏎` is a line break. The repeated title line and the added colophon headings are not repeated here.

### ཁྱུང་པོའི་སྨོན་ལམ།

inbox `ཁྱུང་པོའི་སྨོན་ལམ། །.md` · verdict **rebuild** (w/o title line: **patch**) · ids kept 1/8

- heading `^0` H1 punctuation: `༄༅། །ཁྱུང་པོའི་སྨོན་ལམ།` → `༄༅། །ཁྱུང་པོའི་སྨོན་ལམ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…ོའི་སྨོན་ལམ།{+ །+}…` |

### གཏོར་མ་ཆ་གསུམ་བཞུགས་སོ།

inbox `གཏོར་མ་ཆ་གསུམ་བཞུགས་སོ། །.md` · verdict **blocked** (w/o title line: **blocked**) · ids kept 0/48

- segment added (`—`, 1 line(s)): “##མཇུག་བྱང་།”

### གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།

inbox `གསོལ་འདེབས་བར་ཆད་ལམ་སེལ། །.md` · verdict **rebuild** (w/o title line: **patch**) · ids kept 1/25

- heading `^0` H1 whitespace: `༄༅། །གསོལ་འདེབས་བར་ཆད་ལམ་སེལ།།` → `༄༅། །གསོལ་འདེབས་བར་ཆད་ལམ་སེལ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | whitespace | `…ར་ཆད་ལམ་སེལ།{+ +}།…` |

### གསོལ་འདེབས་བསམ་པ་མྱུར་འགྲུབ་མ།

inbox `གསོལ་འདེབས་བསམ་པ་མྱུར་འགྲུབ་མ། །.md` · verdict **rebuild** (w/o title line: **patch**) · ids kept 1/6

- heading `^0` H1 punctuation: `༄༅། །གསོལ་འདེབས་བསམ་པ་མྱུར་འགྲུབ་མ།` → `༄༅། །གསོལ་འདེབས་བསམ་པ་མྱུར་འགྲུབ་མ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…ྱུར་འགྲུབ་མ།{+ །+}…` |

### གསོལ་འདེབས་ལེའུ་བདུན་མ།

inbox `གསོལ་འདེབས་ལེའུ་བདུན་མ། །.md` · verdict **rebuild** (w/o title line: **patch**) · ids kept 1/132

- heading `^0` H1 punctuation: `༄༅། །གསོལ་འདེབས་ལེའུ་བདུན་མ།` → `༄༅། །གསོལ་འདེབས་ལེའུ་བདུན་མ། །`
- `^4` text changed (letters) (now `^5`) — “ཆོས་སྐུ་ཀུན་ཏུ་བཟང་པོ་ལ་གསོལ་བ་འདེབས༔ ⏎ ལོངས་སྐུ…”

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…ལེའུ་བདུན་མ།{+ །+}…` |
| ^4 | text | `…་བ་རིགས་ལྔ་ལ[-༴། -]{+་གསོལ་བ་འདེབས༔+}⏎སྤྲུལ་སྐུ་ར…` |
| ^4 | text | `…ུམ་མགོན་པོ་ལ[-༴། -]{+་གསོལ་བ་འདེབས༔+}⏎ཨུ་རྒྱན་པདྨ…` |
| ^4 | text | `…་འབྱུང་གནས་ལ[-༴། -]{+་གསོལ་བ་འདེབས༔+}⏎དགེ་སློང་ནམ…` |
| ^4 | text | `…འི་སྙིང་པོ་ལ[-༴ -]{+་གསོལ་བ་འདེབས༔+}⏎ཆོས་རྒྱལ་ཁྲ…` |
| ^4 | text | `…ོང་ལྡེ་བཙན་ལ[-༴ -]{+་གསོལ་བ་འདེབས༔+}⏎མཁའ་འགྲོ་ཡེ…` |
| ^4 | text | `…ས་མཚོ་རྒྱལ་ལ[-༴ -]{+་གསོལ་བ་འདེབས༔+}⏎སྣ་ནམ་རྡོ་ར…` |
| ^4 | text | `…བདུད་འཇོམས་ལ[-༴ -]{+་གསོལ་བ་འདེབས༔+}⏎ལྷ་སྲས་མུ་ཁ…` |
| ^4 | text | `…ཁྲི་བཙན་པོ་ལ[-༴ -]{+་གསོལ་བ་འདེབས༔+}⏎རིག་འཛིན་གར…` |
| ^4 | text | `…ི་དབང་ཕྱུག་ལ[-༴ -]{+་གསོལ་བ་འདེབས༔+}⏎མི་ཕམ་ཆོས་ཀ…` |
| ^4 | text | `…ྱི་རྒྱལ་པོ་ལ[-༴-]{+་གསོལ་བ་འདེབས༔+}⏎མི་ཕམ་བསྟན་…` |
| ^4 | text | `…ན་པའི་ཉི་མ་ལ[-༴ -]{+་གསོལ་བ་འདེབས༔+}⏎རྒྱལ་སྲས་ངག…` |
| ^4 | text | `…ང་རྣམ་རྒྱལ་ལ[-༴ -]{+་གསོལ་བ་འདེབས༔+}⏎དྲིན་ཅན་རྩ་…` |
| ^4 | text | `…ྩ་བའི་བླ་མ་ལ[-༴ -]{+་གསོལ་བ་འདེབས༔+}⏎མཆོག་དང་ཐུན…` |

### ཆགས་མེད་བདེ་སྨོན།

inbox `ཆགས་མེད་བདེ་སྨོན། །.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/86 · scheme flat → sectioned

- heading `^0` H1 whitespace: `རྣམ་དག་བདེ་ཆེན་ཞིང་གི་སྨོན་ལམ་རཱ་ག་ཨ་སྲས་མཛད་པ་བཞུགས་སོ།།` → `རྣམ་དག་བདེ་ཆེན་ཞིང་གི་སྨོན་ལམ་རཱ་ག་ཨ་སྲས་མཛད་པ་བཞུགས་སོ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | whitespace | `…་པ་བཞུགས་སོ།{+ +}།…` |

### ཆོ་འཕྲུལ་གྱི་བསྟོད་པ།

inbox `ཆོ་འཕྲུལ་གྱི་བསྟོད་པ། །.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/21 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །ཆོ་འཕྲུལ་གྱི་བསྟོད་པ། ` → `༄༅། །ཆོ་འཕྲུལ་གྱི་བསྟོད་པ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…ྱི་བསྟོད་པ། {+།+}…` |

### ཇ་མཆོད་བདེ་ཆེན་ཀུན་བཟང་མ་བཞུགས་སོ།

inbox `ཇ་མཆོད་བདེ་ཆེན་ཀུན་བཟང་མ་བཞུགས་སོ། །.md` · verdict **rebuild** (w/o title line: **patch**) · ids kept 1/9

- heading `^0` H1 punctuation: `༄༅། །ཇ་མཆོད་བདེ་ཆེན་ཀུན་བཟང་མ་བཞུགས་སོ། ` → `༄༅། །ཇ་མཆོད་བདེ་ཆེན་ཀུན་བཟང་མ་བཞུགས་སོ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…མ་བཞུགས་སོ། {+།+}…` |

### ཏཱ་ཡི་སི་ཏུ་རིམ་པར་བྱོན་པ་རྣམས་ཀྱི་གསོལ་འདེབས།

inbox `ཏཱ་ཡི་སི་ཏུ་རིམ་པར་བྱོན་པ་རྣམས་ཀྱི་གསོལ་འདེབས། །.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/12 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །ཏཱ་ཡི་སི་ཏུ་རིམ་པར་བྱོན་པ་རྣམས་ཀྱི་གསོལ་འདེབས།` → `༄༅། །ཏཱ་ཡི་སི་ཏུ་རིམ་པར་བྱོན་པ་རྣམས་ཀྱི་གསོལ་འདེབས། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་གསོལ་འདེབས།{+ །+}…` |

### ཐབས་མཁས་ཐུགས་རྗེ་མ་བཞུགས་སོ།

inbox `ཐབས་མཁས་ཐུགས་རྗེ་མ་བཞུགས་སོ། །.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/20 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །ཐབས་མཁས་ཐུགས་རྗེ་མ་བཞུགས་སོ།` → `༄༅། །ཐབས་མཁས་ཐུགས་རྗེ་མ་བཞུགས་སོ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་མ་བཞུགས་སོ།{+ །+}…` |

### ཐུབ་པའི་བསྟོད་པ་གང་ཚེ་རྐང་གཉིས་མ།

inbox `ཐུབ་པའི་བསྟོད་པ་གང་ཚེ་རྐང་གཉིས་མ། །.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/9 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །ཐུབ་པའི་བསྟོད་པ་གང་ཚེ་རྐང་གཉིས་མ།` → `༄༅། །ཐུབ་པའི་བསྟོད་པ་གང་ཚེ་རྐང་གཉིས་མ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་རྐང་གཉིས་མ།{+ །+}…` |

### ཐུབ་པའི་བསྟོད་པ་ཐུབ་རྣམས་སྤངས་རྟོགས།

inbox `ཐུབ་པའི་བསྟོད་པ་ཐུབ་རྣམས་སྤངས་རྟོགས། །.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/19 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །ཐུབ་པའི་བསྟོད་པ་ཐུབ་རྣམས་སྤངས་རྟོགས།` → `༄༅། །ཐུབ་པའི་བསྟོད་པ་ཐུབ་རྣམས་སྤངས་རྟོགས། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་སྤངས་རྟོགས།{+ །+}…` |

### ཐུབ་པའི་མཛད་པ་བཅུ་གཉིས་ལ་བསྟོད་པ་ཞེས་བྱ་བ།

inbox `ཐུབ་པའི་མཛད་པ་བཅུ་གཉིས་ལ་བསྟོད་པ་ཞེས་བྱ་བ། །.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/17 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །ཐུབ་པའི་མཛད་པ་བཅུ་གཉིས་ལ་བསྟོད་པ་ཞེས་བྱ་བ།` → `༄༅། །ཐུབ་པའི་མཛད་པ་བཅུ་གཉིས་ལ་བསྟོད་པ་ཞེས་བྱ་བ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་པ་ཞེས་བྱ་བ།{+ །+}…` |

### ཐུབ་བསྟན་རིས་མེད་རྒྱས་པའི་སྨོན་ལམ།

inbox `ཐུབ་བསྟན་རིས་མེད་རྒྱས་པའི་སྨོན་ལམ། །.md` · verdict **rebuild** (w/o title line: **patch**) · ids kept 1/24

- heading `^0` H1 punctuation: `༄༅། །ཐུབ་བསྟན་རིས་མེད་རྒྱས་པའི་སྨོན་ལམ།` → `༄༅། །ཐུབ་བསྟན་རིས་མེད་རྒྱས་པའི་སྨོན་ལམ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…པའི་སྨོན་ལམ།{+ །+}…` |

### ཐོག་མཐའ་མ་བཞུགས་སོ།

inbox `ཐོག་མཐའ་མ་བཞུགས་སོ། །.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/33 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །ཐོག་མཐའ་མ་བཞུགས་སོ།` → `༄༅། །ཐོག་མཐའ་མ་བཞུགས་སོ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་མ་བཞུགས་སོ།{+ །+}…` |

### དགའ་ལྡན་ལྷ་བརྒྱ་མ་འདོད་གསོལ་སྨོན་ལམ་དང་བཅས་པ།

inbox `དགའ་ལྡན་ལྷ་བརྒྱ་མ་འདོད་གསོལ་སྨོན་ལམ་དང་བཅས་པ། །.md` · verdict **rebuild** (w/o title line: **patch**) · ids kept 1/23

- heading `^0` H1 punctuation: `༄༅། ། དགའ་ལྡན་ལྷ་བརྒྱ་མ་འདོད་གསོལ་སྨོན་ལམ་དང་བཅས་པ།` → `༄༅། ། དགའ་ལྡན་ལྷ་བརྒྱ་མ་འདོད་གསོལ་སྨོན་ལམ་དང་བཅས་པ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…ལམ་དང་བཅས་པ།{+ །+}…` |

### དགེ་སློང་མ་དཔལ་མོས་མཛད་པའི་འཕགས་པ་སྤྱན་རས་གཟིགས་དབང་ཕྱུག་གི་བསྟོད་པ།

inbox `དགེ་སློང་མ་དཔལ་མོས་མཛད་པའི་འཕགས་པ་སྤྱན་རས་གཟིགས་དབང་ཕྱུག་གི་བསྟོད་པ། །.md` · verdict **rebuild** (w/o title line: **patch**) · ids kept 1/12

- heading `^0` H1 punctuation: `དགེ་སློང་མ་དཔལ་མོས་མཛད་པའི་འཕགས་པ་སྤྱན་རས་གཟིགས་དབང་ཕྱུག་གི་བསྟོད་པ།` → `དགེ་སློང་མ་དཔལ་མོས་མཛད་པའི་འཕགས་པ་སྤྱན་རས་གཟིགས་དབང་ཕྱུག་གི་བསྟོད་པ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་གི་བསྟོད་པ།{+ །+}…` |

### དགོངས་གཅིག་ལྷན་ཐབས་བཞུགས་སོ།

inbox `དགོངས་གཅིག་ལྷན་ཐབས་བཞུགས་སོ།.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/18 · scheme flat → sectioned

- heading `^0` H1 whitespace: `དགོངས་གཅིག་ལྷན་ཐབས་བཞུགས་སོ།།` → `དགོངས་གཅིག་ལྷན་ཐབས་བཞུགས་སོ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | whitespace | `…བས་བཞུགས་སོ།{+ +}།…` |

### དཔལ་ནཱ་ལེནྡྲའི་པཎ་གྲུབ་བཅུ་བདུན་གྱི་གསོལ་འདེབས།

inbox `དཔལ་ནཱ་ལེནྡྲའི་པཎ་གྲུབ་བཅུ་བདུན་གྱི་གསོལ་འདེབས།.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/27 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །དཔལ་ནཱ་ལེནྡྲའི་པཎ་གྲུབ་བཅུ་བདུན་གྱི་གསོལ་འདེབས།` → `༄༅། །དཔལ་ནཱ་ལེནྡྲའི་པཎ་གྲུབ་བཅུ་བདུན་གྱི་གསོལ་འདེབས། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་གསོལ་འདེབས།{+ །+}…` |

### དཔལ་ལྡན་ས་གསུམ་མ།

inbox `དཔལ་ལྡན་ས་གསུམ་མ།.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/40 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །དཔལ་ལྡན་ས་གསུམ་མ།` → `༄༅། །དཔལ་ལྡན་ས་གསུམ་མ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…ྡན་ས་གསུམ་མ།{+ །+}…` |

### དཔལ་ས་སྐྱ་པའི་བསྟན་པ་དར་ཞིང་རྒྱས་པའི་སྨོན་ལམ་འཇམ་དབྱངས་བླ་མ་དགྱེས་པའི་ཞལ་ལུང་ཞེས་བྱ་བ་བཞུགས་སོ། །

inbox `དཔལ་ས་སྐྱ་པའི་བསྟན་པ་དར་ཞིང་རྒྱས་པའི་སྨོན་ལམ་འཇམ་དབྱངས་བླ་མ་དགྱེས་པའི་ཞལ་ལུང་ཞེས་བྱ་བ་བཞུགས་སོ། །.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/29 · scheme flat → sectioned

- `^28` line breaks moved: 1 → 2 lines — “ཅེས་པའང་འཇམ་དབྱངས་ཆོས་ཀྱི་བློ་གྲོས་པས་ཆུ་རྟ་སྨལ་…”
- `^28` punctuation only (now `^1-1-1`) — “ཅེས་པའང་འཇམ་དབྱངས་ཆོས་ཀྱི་བློ་གྲོས་པས་ཆུ་རྟ་སྨལ་…”

| unit | kind | change |
|---|---|---|
| ^28 | punctuation | `…{+་⏎+}ཅེས་པའང་འཇམ་…` |

### དབང་སྡུད་གསོལ་འདེབས།

inbox `དབང་སྡུད་གསོལ་འདེབས།.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/9 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །དབང་སྡུད་གསོལ་འདེབས།` → `༄༅། །དབང་སྡུད་གསོལ་འདེབས། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་གསོལ་འདེབས།{+ །+}…` |

### དབྱངས་ཅན་མའི་བསྟོད་པ་བཞུགས་སོ།

inbox `དབྱངས་ཅན་མའི་བསྟོད་པ་བཞུགས་སོ།.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/6 · scheme flat → sectioned

- heading `^0` H1 punctuation: `༄༅། །དབྱངས་ཅན་མའི་བསྟོད་པ་བཞུགས་སོ།` → `༄༅། །དབྱངས་ཅན་མའི་བསྟོད་པ་བཞུགས་སོ། །`

| unit | kind | change |
|---|---|---|
| heading ^0 | punctuation | `…་པ་བཞུགས་སོ།{+ །+}…` |

### ཕ་དམ་པ་སངས་རྒྱས་ཀྱི་ཞལ་གདམས་དིང་རི་བརྒྱ་རྩ་མ་བཞུགས་སོ།

inbox `ཕ་དམ་པ་སངས་རྒྱས་ཀྱི་ཞལ་གདམས་དིང་རི་བརྒྱ་རྩ་མ་བཞུགས་སོ།.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/54 · scheme flat → sectioned

- heading `^0` H1 whitespace: `༄༅། །ཕ་དམ་པ་སངས་རྒྱས་ཀྱི་ཞལ་གདམས་དིང་རི་བརྒྱ་རྩ་མ་བཞུགས་སོ།། ` → `༄༅། །ཕ་དམ་པ་སངས་རྒྱས་ཀྱི་ཞལ་གདམས་དིང་རི་བརྒྱ་རྩ་མ་བཞུགས་སོ།།`

| unit | kind | change |
|---|---|---|
| heading ^0 | whitespace | `…མ་བཞུགས་སོ།།[- -]…` |

### སྨོན་ལམ་རྡོ་རྗེའི་རྒྱ་མདུད་ནི།

inbox `སྨོན་ལམ་རྡོ་རྗེའི་རྒྱ་མདུད་ནི།.md` · verdict **rebuild** (w/o title line: **rebuild**) · ids kept 1/11 · scheme flat → sectioned

- `^10` whitespace only (now `^1-1-1`) — “ཅེས་པའང་རིག་པ་འཛིན་པ་འགྱུར་མེད་རྡོ་རྗེས་སོ། །”

| unit | kind | change |
|---|---|---|
| ^10 | whitespace | `…ོ་རྗེས་སོ། །[- -]…` |

## Inbox notes without a source (not compared)

The backlog (`status: segmented`) and the retired note; none has been stamped or uploaded.

- 01 ༧རྒྱལ་བ་ཡིད་བཞིན་ནོར་བུའི་ཞབས་བརྟན་བཞུགས་སོ།.md
- 02 འབྲི་གུང་༧སྐྱབས་མགོན་ཉི་ཟླ་གཟུང་གི་ཞབས་བརྟན་བཞུགས་སོ།.md
- 03 དཔལ་༧རྒྱལ་དབང་འབྲུག་པ་བཅུ་གཉིས་པའི་ཞབས་བརྟན་བཞུགས་སོ།.md
- 04 གོང་མ་ཁྲི་ཆེན་རིན་པོ་ཆེའི་ཞབས་བརྟན་བཞུགས་སོ།.md
- 05 རྣམ་དག་བདེ་ཆེན་ཞིང་གི་སྨོན་ལམ་རྣམ་གྲོལ་མ་བཞུགས་སོ།.md
- 06 རྣམ་དག་བདེ་ཆེན་ཞིང་གི་སྨོན་ལམ་བཞུགས་སོ།.md
- 07 ཐང་སྟོང་རྒྱལ་པོའི་གསུང་སྐྱབས་འགྲོ་ནས་གཟིགས་ཀྱི་སྒོམ་བཟླས།.md
- 08 པོ་བསྟོད།.md
- 09 རྡོ་རྗེ་སེམས་དཔའི་མཚན་སྔགས།.md
- 10 ཡིག་བརྒྱ།.md
- 11 ཚེ་དཔག་མེད་ཀྱི་གཟུངས།.md
- 12 གུ་རུ་ཐོལ་ཤགས།.md
- ༄༅། ། མར་མེ་སྨོན་ལམ་གྱི་དབུ་ཕྱོགས་བྷི་ཧ་ར།།.md
- ཀརྨ་པའི་གསོལ་འདེབས་རྒྱལ་ཀུན་ཕྲིན་ལས་གཟུགས་ཅན་མ་བཞུགས་སོ། །.md
- ཀླུ་བསངས་ནོར་བུ་དགོས་འདོད་ཀུན་འབྱུང་ཞེས་བྱ་བ་བཞུགས་སོ། །.md
- གངས་ཅན་ཤིང་རྟ་ཉེར་ལྔའི་གསོལ་འདེབས། །.md
- གནས་བཅུའི་བསྟོད་པ་བཞུགས་སོ། །.md
- གཙོ་རྒྱལ་མ་བཞུགས་སོ། །.md
- གུ་རུ་ཐོལ་ཤགས།.md
- གོང་མ་ཁྲི་ཆེན་རིན་པོ་ཆེའི་ཞབས་བརྟན་བཞུགས་སོ།.md
- ཐང་སྟོང་རྒྱལ་པོའི་གསུང་སྐྱབས་འགྲོ་ནས་གཟིགས་ཀྱི་སྒོམ་བཟླས།.md
- དཔལ་༧རྒྱལ་དབང་འབྲུག་པ་བཅུ་གཉིས་པའི་ཞབས་བརྟན་བཞུགས་སོ།.md
- པོ་བསྟོད།.md
- བཅོམ་ལྡན་འདས་མ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པའི་སྙིང་པོ།.md
- ཚེ་དཔག་མེད་ཀྱི་གཟུངས།.md
- འབྲི་གུང་༧སྐྱབས་མགོན་ཉི་ཟླ་གཟུང་གི་ཞབས་བརྟན་བཞུགས་སོ།.md
- ཡིག་བརྒྱ།.md
- རྒྱལ་བ་ཡིད་བཞིན་ནོར་བུའི་ཞབས་བརྟན་བཞུགས་སོ།.md
- རྗེ་བཙུན་སྒྲོལ་དཀར་གྱི་བསྟོད་པ་མཁྱེན་བརྩེ་དྲི་མེད་མ།.md
- རྡོ་རྗེ་སེམས་དཔའི་མཚན་སྔགས།.md
- རྣམ་དག་བདེ་ཆེན་ཞིང་གི་སྨོན་ལམ་བཞུགས་སོ།.md
- རྣམ་དག་བདེ་ཆེན་ཞིང་གི་སྨོན་ལམ་རྣམ་གྲོལ་མ་བཞུགས་སོ།.md
- སངས་རྒྱས་སྨན་བླའི་གཟུངས།.md
- སྣང་སྲིད་དབང་དུ་སྡུད་པའི་གསོལ་འདེབས་བྱིན་རླབས་སྤྲིན་ཆེན།.md (retired)
