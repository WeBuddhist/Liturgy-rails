#!/usr/bin/env bash
# Seed an empty translation track: one scaffold file per source note, every
# block present and marked *[not yet translated]*, ready for the
# dharmamitra-translate skill to fill in later.
#
#   4-SYSTEM/scripts/seed_track_scaffold.sh "modern chinese" zh
#
# Runs dm_translate.py --render-only, which renders from the (absent) ledger
# and makes ZERO API calls, so this costs nothing against the endpoint's
# 400-requests/day quota. Re-running is safe: each file is re-rendered from the
# same empty ledger.
#
# Afterwards run   python3 4-SYSTEM/scripts/stamp_metadata.py --all
# to stamp the backend ids, the track provenance metadata and the researched
# titles onto what this produced — the renderer writes its own frontmatter and
# knows nothing about them.
set -euo pipefail

LANG_LABEL="${1:?usage: seed_track_scaffold.sh <language label> <lang tag> [track dir]}"
LANG_TAG="${2:?usage: seed_track_scaffold.sh <language label> <lang tag> [track dir]}"
TRACK="${3:-3-TRANSFORMATIONS/Translations/Dharmamitra/$LANG_TAG}"

VAULT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$VAULT"

DM=".claude/skills/dharmamitra-translate/scripts/dm_translate.py"
[ -f "$DM" ] || { echo "missing $DM" >&2; exit 1; }

mkdir -p "$TRACK"
n=0
for src in 1-SOURCES/Text/*.md; do
    python3 "$DM" --source "$src" \
        --lang "$LANG_LABEL" --lang-tag "$LANG_TAG" \
        --out "$TRACK" --render-only >/dev/null
    n=$((n + 1))
done

# The renderer always stamps `status: draft` and today's date, which reads as
# "a translation was produced" for a file that holds no translation at all.
# Say what these actually are until the real run overwrites them.
python3 - "$TRACK" <<'PY'
import os, re, sys
track = sys.argv[1]
fixed = 0
for name in sorted(os.listdir(track)):
    if not name.endswith(".md") or name in {"about.md", "style.md", "context-header.md"}:
        continue
    path = os.path.join(track, name)
    text = open(path).read()
    if not re.search(r"^blocks_translated: 0$", text, re.M):
        continue                      # real content: leave it alone
    new = re.sub(r"^status: draft$", "status: scaffold", text, count=1, flags=re.M)
    new = re.sub(r"^generated: .*$", "generated:", new, count=1, flags=re.M)
    if new != text:
        open(path, "w").write(new)
        fixed += 1
print(f"marked {fixed} untranslated files as status: scaffold")
PY

echo "seeded $n scaffold files into $TRACK"
