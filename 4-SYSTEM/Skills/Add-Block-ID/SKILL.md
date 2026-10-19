---
name: Add-Block-ID
description: Add Obsidian block IDs to a note's headings and body-text blocks, in place. Use whenever asked to run Add-Block-ID, add block ids, add obsidian block ids, or stamp block ids on a note.
---

# Add-Block-ID

Adds an addressable Obsidian block id (`^...`) to every heading and every
body-text block in a note, so any block can be linked to with `[[note#^id]]`.
General-purpose: works on any note in the vault, and writes the stamped
result back to that same file.

This is purely mechanical — it never rewrites, reorders, splits, merges, or
retitles anything. If a note's headings or paragraph breaks aren't right
yet, that's fixed by hand first; this tool only appends ids.

The script:

```
4-SYSTEM/scripts/add_block_id.py
```

## ID scheme

```
# Heading                 ^0
## Heading                ^1-0        first H2 = section 1, "segment 0"
<body text block>         ^1-1
<body text block>         ^1-2
### Heading                ^1-1-0      first H3 under section 1
<body text block>         ^1-3        still counted under the H2
## Heading                ^2-0        second H2 — counters restart
<body text block>         ^2-1
```

- `# heading` → `^0`. At most one H1, and if present it must be the first
  thing in the note.
- `## heading` → `^1-0`, `^2-0`, `^3-0`, ... — H2 sections numbered in order.
- `### heading` → `^1-1-0`, `^1-2-0`, ... — H3 numbered within its parent H2.
- **Strict rule — body-text ids are always based on the `##` heading.**
  A body-text block's id is `^<H2 number>-<n>`, always two parts. The
  counter restarts at every H2 and runs straight through any `###`
  subheadings inside it: an H3 never resets the count and never appears in
  a body-text id. Only the H3 heading line itself gets three parts
  (`^2-1-0`). Example: under `## མཇུག་བྱང་།` (`^2-0`) →
  `### མཛད་བྱང་།` (`^2-1-0`) → colophon `^2-1`, not `^2-1-1`.
- A flat note with no `##` anywhere numbers its body blocks straight
  through: `^1`, `^2`, `^3`, ...
- Body text sitting directly under the H1, before the first `##`, is
  section 0: `^0-1`, `^0-2`, ...
- A note with no headings at all numbers straight through from `^1`.
- The id is appended to the **last line** of its heading or block, preceded
  by exactly one space. Obsidian block ids allow only digits, letters and
  hyphens — never a dot (`^2-1-1`, not `^2.1.1`).
- YAML frontmatter, if the note has any, is left untouched.
- Line endings (LF or CRLF) are preserved as found.

What it refuses, rather than guessing:

- more than one H1, or an H1 that isn't the first thing in the note
- a heading deeper than `###`
- an H3 that appears before any H2
- a note that already carries block ids (unless `--restamp` is passed)

## Running it

From the vault root:

```bash
# preview the id plan without writing anything
python3 4-SYSTEM/scripts/add_block_id.py plan -v "<path/to/note.md>"

# add the ids, in place
python3 4-SYSTEM/scripts/add_block_id.py stamp "<path/to/note.md>"

# re-stamp a note that already has ids (e.g. after it was edited)
python3 4-SYSTEM/scripts/add_block_id.py stamp --restamp "<path/to/note.md>"
```

`<path>` can also be a directory, in which case every `*.md` file directly
inside it (non-recursive) is processed.

Before writing, `stamp` always checks that stripping the new ids back out
reproduces the original file byte-for-byte — so a note can never be
corrupted by a bad parse; a file that fails this check is aborted with a
reason instead of being written.

Other commands:

```bash
# remove block ids from a note (prints to stdout; add --in-place to write)
python3 4-SYSTEM/scripts/add_block_id.py strip "<path/to/note.md>"

# check an already-stamped note for problems (missing/duplicate/stranded ids)
python3 4-SYSTEM/scripts/add_block_id.py lint "<path/to/note.md>"
```

## Report back

After running: which file(s) were stamped, how many ids were added, and any
aborted file with its reason.

## Related

The liturgy pipeline has its own, more elaborate version of this
(`block-ids` skill / `4-SYSTEM/scripts/block_ids.py`), which reads
exclusively from `0-INBOX/` and writes prepared copies to
`1-SOURCES/Text/`, with a full plan → stamp → verify → lint workflow and a
retired-texts list. Use that one for the `0-INBOX` → `1-SOURCES/Text`
pipeline specifically; use Add-Block-ID for stamping any other note
in place. The H2-based body-id rule above is the vault standard; if
`block_ids.py` still numbers body blocks under an H3 (`^2-1-1`), it needs
the same change to stay consistent.
