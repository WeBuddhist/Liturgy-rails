#!/usr/bin/env python3
"""gm_titles.py — add a target-language title for every text to the title registry.

`1-SOURCES/liturgy-titles.json` holds each text's researched English and Chinese
titles; `stamp_metadata.py --titles` reads `<tag>_title` from it to set the
translation file's `title`, `title_translated` and H1, and
`translation_payloads.py` refuses to upload a file without `title_translated`.
A new language therefore needs a `<tag>_title` per text before its track can be
stamped or uploaded.

This script asks Gemini for that title, giving it the Tibetan title and heading,
the researched English (and Chinese) titles, and the registry notes. The result
is written as `<tag>_title`, with `<tag>_attested: false`, `<tag>_source: ""`,
`<tag>_alt` (alternatives) and `<tag>_method` recording how it was made, so the
registry stays honest: these are translated titles, not attested ones.

Idempotent: entries that already carry `<tag>_title` are skipped unless --force.
The registry is written once, at the end, only when something changed.

Usage:
    gm_titles.py --lang hindi                 # every text lacking hi_title
    gm_titles.py --lang nepali --only "ཚིག་བདུན,བློ་སྦྱོང"
    gm_titles.py --lang mongolian --dry-run   # show the request, no call
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
VAULT = HERE.parents[3]
REGISTRY = VAULT / "1-SOURCES" / "liturgy-titles.json"

sys.path.insert(0, str(HERE))
from gm_translate import (API_BASE, DEFAULT_MODEL, KEY_ENV, LANG_TAGS,  # noqa: E402
                          SAFETY_OFF)

SCRIPT_NOTES = {
    "hi": "Hindi in Devanagari, using Sanskrit-derived Buddhist vocabulary.",
    "ne": "Nepali in Devanagari (Nepali, not Hindi), using the Buddhist vocabulary current in Nepal.",
    "mn": "Mongolian in Cyrillic (Khalkha standard), using the established Mongolian Buddhist "
          "terminology and deity names (e.g. Дарь эх, Жанрайсиг, Манзушир).",
    "vi": "Vietnamese with full diacritics, using Sino-Vietnamese Buddhist vocabulary "
          "(e.g. Quán Thế Âm, Văn Thù, Liên Hoa Sanh).",
}

SCHEMA = {
    "type": "object",
    "properties": {
        "titles": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "stem": {"type": "string"},
                    "title": {"type": "string"},
                    "alt": {"type": "array", "items": {"type": "string"}},
                    "note": {"type": "string"},
                },
                "required": ["stem", "title", "alt", "note"],
            },
        }
    },
    "required": ["titles"],
}


def build_prompt(entries, lang, tag):
    rows = []
    for r in entries:
        rows.append({
            "stem": r["stem"],
            "tibetan_title": r.get("bo_title", ""),
            "tibetan_heading": r.get("bo_heading", ""),
            "english_title": r.get("en_title", ""),
            "english_alternatives": r.get("en_alt", []),
            "chinese_title": r.get("zh_title", ""),
            "notes": r.get("notes", ""),
        })
    return (
        f"You are naming Tibetan Buddhist liturgical texts in {lang} for DISPLAY in a "
        f"prayer app used by ordinary {lang}-speaking Buddhists. For each text below give "
        f"the title a reader of that app would recognise and understand at a glance:\n"
        f"1. If the text has an established, published title in {lang} (as used by "
        f"{lang}-language Buddhist centres, publishers or teachers' websites), use that "
        f"exact form.\n"
        f"2. Otherwise render the Tibetan title faithfully in plain, natural {lang}, using "
        f"the English title as a guide to its sense. Prefer the wording an ordinary reader "
        f"uses over a dense classical or Sanskritic calque: 'Eight Verses of Mind Training' "
        f"should read like a title people say aloud, not like a catalogue entry. Put any "
        f"classical/literary form in the alternatives instead.\n"
        f"{SCRIPT_NOTES.get(tag, '')} Keep it a title: concise, no explanation inside it, "
        f"no honorific padding, no 'bzhugs so' formula. Give up to two alternatives (the "
        f"classical form, a shorter form) and a one-line note saying whether the title is "
        f"an established published one or your rendering. Return JSON with one entry per "
        f"stem, same stems, same order.\n\n" + json.dumps(rows, ensure_ascii=False, indent=1)
    )


def call(prompt, model, key, timeout=240, retries=5, schema=None):
    """One JSON-schema generateContent call with retries. `schema` defaults to
    this script's title schema; gm_names.py passes its own."""
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json",
                             "responseSchema": schema or SCHEMA},
        "safetySettings": SAFETY_OFF,
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    last = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(
            f"{API_BASE}/{model}:generateContent", data=data, method="POST",
            headers={"Content-Type": "application/json", "x-goog-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            c = payload["candidates"][0]
            text = "".join(p.get("text", "") for p in c["content"]["parts"] if "text" in p)
            return json.loads(text), payload.get("modelVersion", model)
        except urllib.error.HTTPError as exc:
            last = exc
            detail = exc.read().decode("utf-8", "replace")[:300]
            if exc.code in (400, 401, 403, 404):
                raise SystemExit(f"HTTP {exc.code}: {detail}")
            wait = int(exc.headers.get("Retry-After") or 0) or min(120, 10 * attempt)
            print(f"  ! HTTP {exc.code}; waiting {wait}s ({attempt}/{retries})", file=sys.stderr)
            time.sleep(wait)
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(5 * attempt)
    raise SystemExit(f"gave up: {last}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lang", required=True)
    ap.add_argument("--lang-tag", default=None)
    ap.add_argument("--only", default=None, help="comma-separated substrings of stems")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--batch", type=int, default=20, help="texts per call")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    lang = args.lang.strip().lower()
    tag = args.lang_tag or LANG_TAGS.get(lang) or re.sub(r"[^a-z]", "", lang)[:3]
    tkey = f"{tag}_title"

    raw = REGISTRY.read_text(encoding="utf-8")
    reg = json.loads(raw)
    indent = 2 if raw.split("\n", 1)[1][:2] == "  " else 1
    texts = reg["texts"]

    # An attested title (found in a published source) is never overwritten,
    # not even with --force: the registry's whole point is to keep those.
    todo = [r for r in texts
            if (args.force or not r.get(tkey)) and not r.get(f"{tag}_attested")]
    if args.only:
        subs = [s.strip() for s in args.only.split(",") if s.strip()]
        todo = [r for r in todo if any(s in r["stem"] for s in subs)]
    print(f"{lang} ({tag}): {len(todo)} of {len(texts)} texts need {tkey}")
    if not todo:
        return 0

    key = os.environ.get(KEY_ENV, "")
    if not key and not args.dry_run:
        sys.exit(f"{KEY_ENV} is not set")

    changed = 0
    for i in range(0, len(todo), args.batch):
        chunk = todo[i:i + args.batch]
        prompt = build_prompt(chunk, lang, tag)
        if args.dry_run:
            print(prompt[:3000])
            continue
        print(f"  call {i // args.batch + 1}: {len(chunk)} text(s) … ", end="", flush=True)
        data, version = call(prompt, args.model, key)
        got = {t["stem"]: t for t in data.get("titles", [])}
        missing = [r["stem"] for r in chunk if r["stem"] not in got or not got[r["stem"]]["title"].strip()]
        print(f"{len(got)} titles back" + (f", {len(missing)} MISSING" if missing else ""))
        for r in chunk:
            t = got.get(r["stem"])
            if not t or not t["title"].strip():
                continue
            r[tkey] = t["title"].strip()
            r[f"{tag}_attested"] = False
            r[f"{tag}_source"] = ""
            r[f"{tag}_alt"] = [a.strip() for a in t.get("alt", []) if a.strip()][:3]
            r[f"{tag}_method"] = f"translated by {version} from the Tibetan and English titles; unattested"
            r[f"{tag}_note"] = t.get("note", "").strip()
            changed += 1
            print(f"     {r['stem'][:32]:34} {r[tkey]}")
        for s in missing:
            print(f"     !! no title returned for {s}", file=sys.stderr)

    if changed and not args.dry_run:
        REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=indent) + "\n",
                            encoding="utf-8")
        print(f"\nwrote {changed} {tkey} entries to {REGISTRY.relative_to(VAULT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
