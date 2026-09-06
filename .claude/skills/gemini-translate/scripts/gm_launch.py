#!/usr/bin/env python3
"""gm_launch.py — start gm_corpus.py drivers detached, one per language.

A full-corpus run takes hours, and a shell started from an agent's tool call is
killed after about an hour (observed 2026-09-06: every background driver died
at ~61 min with no STOPPED line). macOS has no `setsid` binary, so this small
launcher does the same thing with `start_new_session=True`: each driver runs in
its own session, survives the tool call that started it, appends to
<track>/work/_corpus-run.log, and can be checked with

    pgrep -fl "gm_corpus.py --lang"

A driver that is killed anyway loses at most the call in flight; the ledger is
per block and the next launch resumes. Never start two drivers for the same
language: both would translate the same blocks.

Usage:
    gm_launch.py                       # all four commissioned languages
    gm_launch.py hindi vietnamese      # some of them
    gm_launch.py --dry-run
"""

import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
VAULT = HERE.parents[3]
GM = HERE / "gm_corpus.py"

sys.path.insert(0, str(HERE))
from gm_translate import DEFAULT_TRACK_ROOT, KEY_ENV, LANG_TAGS  # noqa: E402

COMMISSIONED = ["hindi", "nepali", "mongolian", "vietnamese"]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    langs = args or COMMISSIONED
    if not os.environ.get(KEY_ENV) and not dry:
        sys.exit(f"{KEY_ENV} is not set — run `source ~/.zshrc` first")
    for lang in langs:
        tag = LANG_TAGS.get(lang)
        if not tag:
            sys.exit(f"unknown language label {lang!r}")
        if subprocess.run(["pgrep", "-f", f"gm_corpus.py --lang {lang}"],
                          capture_output=True).returncode == 0:
            print(f"{lang}: a driver is already running — not starting another")
            continue
        work = VAULT / DEFAULT_TRACK_ROOT / tag / "work"
        work.mkdir(parents=True, exist_ok=True)
        log = work / "_corpus-run.log"
        if dry:
            print(f"{lang}: would start {GM.name} --lang {lang} >> {log.relative_to(VAULT)}")
            continue
        fh = open(log, "ab")
        fh.write(b"=== detached launch (gm_launch.py) ===\n")
        p = subprocess.Popen([sys.executable, str(GM), "--lang", lang], cwd=VAULT,
                             stdout=fh, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, start_new_session=True)
        print(f"{lang}: pid {p.pid}, log {log.relative_to(VAULT)}")


if __name__ == "__main__":
    main()
