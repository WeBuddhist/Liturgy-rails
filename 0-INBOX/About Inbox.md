# 0-INBOX — Raw intake

Unprocessed material. Files land here as received and leave when they have
been normalised into `1-SOURCES/`.

## What is here

The **verbatim critical-instance content** for each of the 100 texts, one
file per text, under the same filename as its prepared counterpart in
`1-SOURCES/Text/`. Keeping the raw form means any formatting decision — a
stanza boundary, a removed verse counter, a merged ornament line — can be
checked against exactly what the backend returned, without re-fetching.

The only edits applied to these files are the mechanical cleanups that
cannot lose information: null bytes stripped, non-breaking tsheg ༌ → ་,
shad-sandwiched verse counters removed, whitespace collapsed. Everything
else — segmentation, headings, metadata — happens on the way into
`1-SOURCES/`.

## Rules

- Nothing downstream cites `0-INBOX/`. Rails and transformations cite
  `1-SOURCES/`; this folder exists for verification and re-processing.
- Files here are safe to regenerate: `4-SYSTEM/scripts/format_liturgy_batch.py`
  rewrites both this folder and `1-SOURCES/` from the fetch artifacts.
