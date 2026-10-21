#!/usr/bin/env python3
"""Upload prepared translation payloads to the WeBuddhist v2 API.

Per translation, three calls:

    POST /v2/texts                            <- <name>.text.json      -> text_id
    POST /v2/texts/{text_id}/editions         <- <name>.edition.json   -> edition_id
    PUT  /v2/editions/{root}/alignments/{new} <- <name>.alignment.json -> 204

The third call is what `upload_liturgy.py` has no equivalent of: it is the
segment alignment back to the Tibetan, and it is a PUT — "replace the
alignments between this pair of editions" — so unlike the two POSTs it is
idempotent on the server and safe to repeat.

Ledger keys are `<stem>-<lang>`, so translations share
`upload_ledger.json` with the root texts they point at without colliding
with them. Each entry gains an `aligned` flag once the PUT returns, because
an uploaded translation that never got its alignment is the one bad state
this script can leave behind and it is invisible from the text and edition
ids alone.

Ordering matters and is not negotiable: the root text must already be in the
ledger with both ids. `translation_of` is settable only at creation — the v2
`TextPatch` schema has no such field — so a translation POSTed without it
cannot be repaired, only deleted and re-created.

Rollback, if a run has to be undone, runs in the reverse order of creation:

    DELETE /v2/editions/{root}/alignments/{new}
    DELETE /v2/editions/{new}
    DELETE /v2/texts/{new}          # refuses while the edition still exists

Credentials come from the environment and are never written to disk:

    WEBUDDHIST_API_KEY   sent as X-API-Key       (required)
    WEBUDDHIST_APP       sent as X-Application   (optional)

`X-Application` is optional here, unlike in `upload_liturgy.py` which requires
it: none of these three operations declares the header in the v2 schema — they
are secured by `X-API-Key` alone. It is still sent when set, because that is
what the root-text run did and the pairing is known to work; it is simply
omitted rather than sent empty when it is not.

Usage:
    upload_translations.py --payloads <dir> [--only <name>] [--limit N] [--dry-run]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

# Share the ledger read/write and POST helpers with the root-text uploader
# rather than restating them; the safety property being relied on — the
# ledger is written after every single call, before the next one is made —
# lives in that module and should have exactly one implementation.
_spec = importlib.util.spec_from_file_location(
    "upload_liturgy", os.path.join(HERE, "upload_liturgy.py"))
_ul = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ul)

BASE = _ul.BASE
LEDGER = _ul.LEDGER
UploadError = _ul.UploadError
load_ledger = _ul.load_ledger
save_ledger = _ul.save_ledger


def send(method, url, body, key, app, timeout=60):
    """POST or PUT; returns the decoded body, or None for a 204.

    The alignment PUT answers 204 with no body, so the response cannot be
    parsed unconditionally the way `upload_liturgy.post` does.
    """
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-Key", key)
    if app:
        req.add_header("X-Application", app)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8")) if raw else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:800]
        raise UploadError(f"HTTP {exc.code} from {url}\n         {detail}") from None
    except urllib.error.URLError as exc:
        raise UploadError(f"network error for {url}: {exc.reason}") from None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--payloads", required=True)
    ap.add_argument("--only", help="upload just this <stem>-<lang>")
    ap.add_argument("--limit", type=int, help="stop after N translations")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ledger", default=LEDGER)
    args = ap.parse_args(argv)

    key = os.environ.get("WEBUDDHIST_API_KEY", "")
    app = os.environ.get("WEBUDDHIST_APP", "")
    if not args.dry_run and not key:
        print("WEBUDDHIST_API_KEY must be set", file=sys.stderr)
        return 2

    names = sorted({f.rsplit(".", 2)[0] for f in os.listdir(args.payloads)
                    if f.endswith(".json")})
    if args.only:
        if args.only not in names:
            print(f"no payload for {args.only!r}", file=sys.stderr)
            return 2
        names = [args.only]
    if args.limit:
        names = names[:args.limit]

    ledger = load_ledger(args.ledger)
    created = aligned_only = skipped = 0

    for name in names:
        entry = ledger.setdefault(name, {})
        if entry.get("text_id") and entry.get("edition_id") and entry.get("aligned"):
            skipped += 1
            print(f"skip   {name}  (text {entry['text_id']}, edition {entry['edition_id']}, aligned)")
            continue

        with open(os.path.join(args.payloads, f"{name}.text.json"), encoding="utf-8") as fh:
            text_body = json.load(fh)
        with open(os.path.join(args.payloads, f"{name}.edition.json"), encoding="utf-8") as fh:
            edition_body = json.load(fh)
        with open(os.path.join(args.payloads, f"{name}.alignment.json"), encoding="utf-8") as fh:
            align = json.load(fh)

        root_edition_id = align.pop("source_edition_id")   # path param, not body
        n_seg = len(edition_body["segmentation"]["segments"])
        n_chr = len(edition_body["content"])
        n_pair = len(align["alignments"])

        if args.dry_run:
            print(f"DRY    {name}")
            print(f"         POST {BASE}/v2/texts  "
                  f"({json.dumps(text_body, ensure_ascii=False)[:100]}…)")
            print(f"         POST {BASE}/v2/texts/<new>/editions  "
                  f"({n_chr} chars, {n_seg} segments)")
            print(f"         PUT  {BASE}/v2/editions/{root_edition_id}/alignments/<new>  "
                  f"({n_pair} pairs)")
            continue

        try:
            if not entry.get("text_id"):
                res = send("POST", f"{BASE}/v2/texts", text_body, key, app)
                entry["text_id"] = res["id"]
                save_ledger(args.ledger, ledger)          # persist before next call
                print(f"       {name}\n         text_id    {res['id']}")

            if not entry.get("edition_id"):
                url = f"{BASE}/v2/texts/{entry['text_id']}/editions"
                res = send("POST", url, edition_body, key, app)
                entry["edition_id"] = res["id"]
                save_ledger(args.ledger, ledger)
                print(f"         edition_id {res['id']}  "
                      f"({n_chr} chars, {n_seg} segments)")
                created += 1
            else:
                aligned_only += 1

            if not entry.get("aligned"):
                url = (f"{BASE}/v2/editions/{root_edition_id}"
                       f"/alignments/{entry['edition_id']}")
                send("PUT", url, align, key, app)
                entry["aligned"] = True
                save_ledger(args.ledger, ledger)
                print(f"         aligned    {n_pair} pairs -> {root_edition_id}")
        except UploadError as exc:
            save_ledger(args.ledger, ledger)
            print(f"FAIL   {name}\n         {exc}", file=sys.stderr)
            print(f"\nstopped on first error. ledger: {args.ledger}", file=sys.stderr)
            return 1
        time.sleep(0.15)

    if args.dry_run:
        print(f"\ndry run: {len(names)} translations, {len(names) * 3} requests, nothing sent")
    else:
        print(f"\nuploaded {created}, aligned-only {aligned_only}, "
              f"skipped {skipped}. ledger: {args.ledger}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
