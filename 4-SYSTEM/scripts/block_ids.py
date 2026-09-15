#!/usr/bin/env python3
"""Stamp Obsidian block IDs onto expert-segmented liturgy notes.

The TOC (headings) and the segmentation (blank-line-separated blocks) are
already correct in 0-INBOX — a domain expert made every judgment call.
This script adds ids and NOTHING else. It never splits, merges, reorders,
rewrites or re-wraps a single character of body text.

ID scheme
---------
    # ༄༅། །Title              ^0
    ## Section k               ^k-0        heading == "segment 0" of its section
    <segment>                  ^k-1
    ### Subsection j           ^k-j-0
    <segment>                  ^k-j-1

Flat texts (no ## at all) number segments straight through: ^1, ^2, ...
Segments sitting under the H1 *before* the first ## get ^0-1, ^0-2, ...
A text with no headings at all numbers from ^1 (its title line is segment 1).

Guarantees
----------
Frontmatter is copied byte-for-byte.  ``strip(stamp(x)) == x`` exactly,
including trailing whitespace, blank runs and a missing final newline —
``verify`` asserts it per file.  Anything the parser does not recognise
aborts that file with a reason; it is never silently rewritten.

Usage
-----
    block_ids.py plan   <path>...                 dry run, print the id plan
    block_ids.py stamp  <src>... --out-dir <dir>  write stamped copies
    block_ids.py verify <stamped>... --src-dir <dir>
    block_ids.py strip  <path>...                 print unstamped text
    block_ids.py lint   <path>...                 check already-stamped files

<path> may be a file or a directory (*.md, non-recursive).
"""

from __future__ import annotations

import argparse
import os
import re
import sys

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*)$")
ID_RE = re.compile(r" \^\d+(?:-\d+)*$")
FM_OPEN = "---\n"
FM_CLOSE = "\n---\n"


class Abort(Exception):
    """File rejected — reported, never worked around."""


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------

class Unit:
    """One heading line, or one segment (a run of consecutive content lines).

    ``lines`` holds the raw source lines verbatim. ``idx`` is the index into
    the body's line list of this unit's LAST line — the line the id is
    appended to.
    """

    __slots__ = ("kind", "level", "lines", "idx", "bid")

    def __init__(self, kind, level, lines, idx):
        self.kind = kind          # "heading" | "segment"
        self.level = level        # heading depth, or 0 for a segment
        self.lines = lines
        self.idx = idx
        self.bid = None           # assigned by assign_ids()


def split_frontmatter(raw: str, path: str):
    """Return (frontmatter, body). Frontmatter is returned verbatim."""
    if not raw.startswith(FM_OPEN):
        raise Abort("no YAML frontmatter (file must start with '---')")
    close = raw.find(FM_CLOSE, len(FM_OPEN) - 1)
    if close == -1:
        raise Abort("frontmatter is never closed")
    end = close + len(FM_CLOSE)
    return raw[:end], raw[end:]


def parse_body(body: str):
    """Tokenise the body into Units.

    A line is blank if it strips to empty — 14 lines in this corpus are a
    lone space and must count as separators or segments silently merge.
    Blank runs and their exact contents are preserved; they are simply not
    part of any unit.
    """
    lines = body.split("\n")
    units, cur, start = [], [], None

    def flush(i):
        if cur:
            units.append(Unit("segment", 0, list(cur), i - 1))
            cur.clear()

    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m:
            flush(i)
            level = len(m.group(1))
            if level > 3:
                raise Abort(f"line {i + 1}: heading depth {level} (max 3)")
            if not m.group(2).strip():
                raise Abort(f"line {i + 1}: empty heading")
            units.append(Unit("heading", level, [line], i))
        elif not line.strip():
            flush(i)
        else:
            if not cur:
                start = i
            cur.append(line)
    flush(len(lines))
    _ = start
    return lines, units


def check_structure(units):
    """Reject anything the id scheme cannot express unambiguously."""
    h1 = [u for u in units if u.kind == "heading" and u.level == 1]
    if len(h1) > 1:
        raise Abort(f"{len(h1)} H1 headings (expected at most 1)")
    if h1 and units[0] is not h1[0]:
        raise Abort("H1 is not the first unit in the body")

    seen_h2 = False
    open_h2 = None          # the current H2 Unit, or None
    h2_has_segments = False
    h2_has_h3 = False

    for u in units:
        if u.kind == "heading" and u.level == 2:
            if open_h2 is not None and h2_has_segments and h2_has_h3:
                raise Abort(
                    "an H2 has both direct segments and H3 children — the id "
                    "scheme cannot express that; give the loose segments "
                    "their own H3"
                )
            seen_h2, open_h2 = True, u
            h2_has_segments = h2_has_h3 = False
        elif u.kind == "heading" and u.level == 3:
            if not seen_h2:
                raise Abort("H3 appears before any H2")
            h2_has_h3 = True
        elif u.kind == "segment" and open_h2 is not None and not h2_has_h3:
            h2_has_segments = True

    if open_h2 is not None and h2_has_segments and h2_has_h3:
        raise Abort(
            "an H2 has both direct segments and H3 children — the id scheme "
            "cannot express that; give the loose segments their own H3"
        )


def assign_ids(units):
    """Walk the units, assigning every one its block id."""
    check_structure(units)

    sectioned = any(u.kind == "heading" and u.level == 2 for u in units)
    h2 = h3 = 0            # section counters
    n = 0                  # segment counter within the current scope

    for u in units:
        if u.kind == "heading" and u.level == 1:
            u.bid = "0"
            n = 0
        elif u.kind == "heading" and u.level == 2:
            h2 += 1
            h3 = 0
            n = 0
            u.bid = f"{h2}-0"
        elif u.kind == "heading" and u.level == 3:
            h3 += 1
            n = 0
            u.bid = f"{h2}-{h3}-0"
        else:
            n += 1
            if not sectioned:
                u.bid = str(n)              # flat text: ^1, ^2, ...
            elif h2 == 0:
                u.bid = f"0-{n}"            # orphan under the H1
            elif h3 == 0:
                u.bid = f"{h2}-{n}"
            else:
                u.bid = f"{h2}-{h3}-{n}"
    return units


# --------------------------------------------------------------------------
# transforms
# --------------------------------------------------------------------------

def is_stamped(raw: str, path: str) -> bool:
    _, body = split_frontmatter(raw, path)
    return any(ID_RE.search(line) for line in body.split("\n"))


def stamp_text(raw: str, path: str, restamp: bool = False) -> str:
    if is_stamped(raw, path):
        if not restamp:
            raise Abort(
                "already carries block ids — pass --restamp to replace them"
            )
        raw = strip_text(raw, path)

    fm, body = split_frontmatter(raw, path)
    lines, units = parse_body(body)
    assign_ids(units)
    out = list(lines)
    for u in units:
        # Appended verbatim: a line that already ends in a space keeps it, so
        # stripping the id restores the original byte-for-byte.
        out[u.idx] = out[u.idx] + " ^" + u.bid
    return fm + "\n".join(out)


def strip_text(raw: str, path: str) -> str:
    """Inverse of stamp_text. Removes ' ^id' only from unit-final lines."""
    fm, body = split_frontmatter(raw, path)
    lines, units = parse_body(body)
    out = list(lines)
    for u in units:
        out[u.idx] = ID_RE.sub("", out[u.idx])
    return fm + "\n".join(out)


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

def describe(raw: str, path: str):
    """(kind, n_segments, n_h2, n_h3, units) for a PRE-stamp file."""
    _, body = split_frontmatter(raw, path)
    _, units = parse_body(body)
    assign_ids(units)
    h1 = sum(1 for u in units if u.kind == "heading" and u.level == 1)
    h2 = sum(1 for u in units if u.kind == "heading" and u.level == 2)
    h3 = sum(1 for u in units if u.kind == "heading" and u.level == 3)
    segs = sum(1 for u in units if u.kind == "segment")
    if not h1 and not h2:
        kind = "D headless"
    elif h3:
        kind = "C h1+h2+h3"
    elif h2:
        kind = "B h1+h2"
    else:
        kind = "A flat"
    return kind, segs, h2, h3, units


def lint_text(raw: str, path: str):
    """Structural checks on an ALREADY-stamped file. Returns list of problems."""
    fm, body = split_frontmatter(raw, path)
    lines, units = parse_body(body)
    problems, seen = [], {}

    for u in units:
        last = u.lines[-1]
        m = ID_RE.search(last)
        if not m:
            problems.append(
                f"line {u.idx + 1}: {u.kind} carries no block id "
                f"({last.strip()[:40]!r})"
            )
            continue
        bid = m.group(0).strip()[1:]
        if bid in seen:
            problems.append(
                f"line {u.idx + 1}: duplicate id ^{bid} "
                f"(also line {seen[bid] + 1})"
            )
        seen[bid] = u.idx
        for j, line in enumerate(u.lines[:-1]):
            if ID_RE.search(line):
                problems.append(
                    f"line {u.idx - len(u.lines) + 1 + j + 1}: "
                    f"id stranded mid-segment"
                )

    for i, line in enumerate(lines):
        if "^" in line and not ID_RE.search(line):
            if re.search(r"\S\^\d", line):
                problems.append(
                    f"line {i + 1}: '^' with no space before it — "
                    f"Obsidian will not read it as a block id"
                )
    _ = fm
    return problems


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

# FORK(liturgy-rails): a text can be retired (a duplicate of another note, its
# backend records deleted) while its 0-INBOX copy is deliberately KEPT as the
# archival record. Without this, the next `stamp 0-INBOX` would silently walk it
# straight back into 1-SOURCES/Text and re-create everything downstream.
RETIRED_LIST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "4-SYSTEM", "retired-texts.txt")


def load_retired(path=RETIRED_LIST):
    """Stems (filename without .md) that must never be picked up from a dir."""
    if not os.path.exists(path):
        return set()
    out = set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if line:
                out.add(line[:-3] if line.endswith(".md") else line)
    return out


def collect(paths):
    retired = load_retired()
    skipped = []
    out = []
    for p in paths:
        if os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                if not f.endswith(".md"):
                    continue
                if f[:-3] in retired:
                    skipped.append(f)
                    continue
                out.append(os.path.join(p, f))
        else:
            # An explicitly named file is honoured even if retired — the guard
            # is against directory sweeps, not against a deliberate one-off.
            out.append(p)
    if skipped:
        # Never skip silently: a quiet omission reads as "nothing to do".
        print(f"retired: skipped {len(skipped)} note(s) listed in "
              f"{os.path.relpath(RETIRED_LIST)}", file=sys.stderr)
        for f in skipped:
            print(f"         {f}", file=sys.stderr)
    return out


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def cmd_plan(args):
    ok = bad = 0
    totals = {}
    for path in collect(args.paths):
        name = os.path.basename(path)
        try:
            kind, segs, h2, h3, units = describe(read(path), path)
        except Abort as exc:
            print(f"ABORT  {name}\n         {exc}")
            bad += 1
            continue
        ok += 1
        totals[kind] = totals.get(kind, 0) + 1
        print(f"{kind:<12} segs={segs:<4} h2={h2:<3} h3={h3:<3} {name}")
        if args.verbose:
            for u in units:
                head = u.lines[0] if u.kind == "heading" else u.lines[-1]
                print(f"    ^{u.bid:<8} {u.kind:<7} {head.strip()[:56]}")
    print(f"\n{ok} parsed, {bad} aborted")
    for k in sorted(totals):
        print(f"  {totals[k]:>3}  {k}")
    return 1 if bad else 0


def cmd_stamp(args):
    os.makedirs(args.out_dir, exist_ok=True)
    ok = bad = 0
    for path in collect(args.paths):
        name = os.path.basename(path)
        raw = read(path)
        try:
            stamped = stamp_text(raw, path, restamp=args.restamp)
            # The contract, asserted before every single write.
            baseline = strip_text(raw, path) if is_stamped(raw, path) else raw
            if strip_text(stamped, path) != baseline:
                raise Abort("round-trip check failed — refusing to write")
        except Abort as exc:
            print(f"ABORT  {name}\n         {exc}")
            bad += 1
            continue
        dst = os.path.join(args.out_dir, name)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(stamped)
        ok += 1
        note = "  (ids replaced)" if is_stamped(raw, path) else ""
        print(f"ok     {name}{note}")
    print(f"\n{ok} written to {args.out_dir}, {bad} aborted")
    return 1 if bad else 0


def cmd_verify(args):
    ok = bad = 0
    for path in collect(args.paths):
        name = os.path.basename(path)
        src = os.path.join(args.src_dir, name)
        if not os.path.exists(src):
            print(f"FAIL   {name}\n         no source at {src}")
            bad += 1
            continue
        stamped, original = read(path), read(src)
        try:
            problems = lint_text(stamped, path)
            # Compare unstamped-to-unstamped, so a source that was itself
            # already stamped still verifies.
            baseline = strip_text(original, src)
            if strip_text(stamped, path) != baseline:
                problems.append(f"body differs from {src} after stripping ids")
            fm_s = split_frontmatter(stamped, path)[0]
            fm_o = split_frontmatter(original, src)[0]
            if fm_s != fm_o:
                problems.append("frontmatter differs from source")
        except Abort as exc:
            problems = [str(exc)]
        if problems:
            print(f"FAIL   {name}")
            for p in problems:
                print(f"         {p}")
            bad += 1
        else:
            ok += 1
            if args.verbose:
                print(f"OK     {name}")
    print(f"\n{ok} OK, {bad} FAILED")
    return 1 if bad else 0


def cmd_strip(args):
    for path in collect(args.paths):
        text = strip_text(read(path), path)
        if args.in_place:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(f"stripped {os.path.basename(path)}")
        else:
            sys.stdout.write(text)
    return 0


def cmd_lint(args):
    ok = bad = 0
    for path in collect(args.paths):
        name = os.path.basename(path)
        try:
            problems = lint_text(read(path), path)
        except Abort as exc:
            problems = [str(exc)]
        if problems:
            print(f"FAIL   {name}")
            for p in problems:
                print(f"         {p}")
            bad += 1
        else:
            ok += 1
            if args.verbose:
                print(f"OK     {name}")
    print(f"\n{ok} OK, {bad} FAILED")
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("-v", "--verbose", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, help):
        # -v accepted on either side of the subcommand
        p = sub.add_parser(name, help=help)
        p.add_argument("-v", "--verbose", action="store_true")
        return p

    p = add("plan", "dry run: classify and print ids")
    p.add_argument("paths", nargs="+")
    p.set_defaults(fn=cmd_plan)

    p = add("stamp", "write stamped copies")
    p.add_argument("paths", nargs="+")
    p.add_argument("--out-dir", required=True)
    p.add_argument(
        "--restamp",
        action="store_true",
        help="replace ids on sources that already carry them",
    )
    p.set_defaults(fn=cmd_stamp)

    p = add("verify", "lint + byte-compare against source")
    p.add_argument("paths", nargs="+")
    p.add_argument("--src-dir", required=True)
    p.set_defaults(fn=cmd_verify)

    p = add("strip", "remove block ids")
    p.add_argument("paths", nargs="+")
    p.add_argument("--in-place", action="store_true")
    p.set_defaults(fn=cmd_strip)

    p = add("lint", "check an already-stamped file")
    p.add_argument("paths", nargs="+")
    p.set_defaults(fn=cmd_lint)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
