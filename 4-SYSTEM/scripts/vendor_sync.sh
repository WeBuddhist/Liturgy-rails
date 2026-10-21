#!/usr/bin/env bash
# Diff the vendored linter/parser against upstream, or refresh them.
#   vendor_sync.sh diff  [ref]   show what we changed vs upstream (default: main)
#   vendor_sync.sh fetch <ref>   overwrite the vendored copies from upstream
set -euo pipefail

REPO="WeBuddhist/bodhisattvacharyavatara-rails"
BASE="https://raw.githubusercontent.com/$REPO"
DIRS=(linter-root-text parser-root-text)
FILES_linter="README.md build.py constants.py languages.py lint_text_input.py lookup.py requirements.txt validate.py"
FILES_parser="README.md parser.py"
HERE="$(cd "$(dirname "$0")" && pwd)"

mode="${1:-diff}"; ref="${2:-main}"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

for d in "${DIRS[@]}"; do
  case "$d" in
    linter-root-text) files=$FILES_linter ;;
    parser-root-text) files=$FILES_parser ;;
  esac
  mkdir -p "$tmp/$d"
  for f in $files; do
    curl -sSfL "$BASE/$ref/4-SYSTEM/scripts/$d/$f" -o "$tmp/$d/$f"
  done
done

if [ "$mode" = "fetch" ]; then
  for d in "${DIRS[@]}"; do cp "$tmp/$d"/* "$HERE/$d/"; done
  echo "refreshed from $REPO@$ref — re-apply local patches and re-run the tests"
else
  for d in "${DIRS[@]}"; do
    diff -ru "$tmp/$d" "$HERE/$d" --exclude=output --exclude=__pycache__ || true
  done
fi
