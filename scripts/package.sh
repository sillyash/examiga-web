#!/usr/bin/env bash
set -euo pipefail

# Builds the frontend (as a smoke test) and packages the whole project into the
# nom_prenom_technologie.tar.gz archive format required by the assignment.
# Usage: scripts/package.sh

cd "$(dirname "$0")/.."

NAME="merienne_ashley_vuejs"
OUT="${NAME}.tar.gz"
STAGING_DIR="$(mktemp -d)"
trap 'rm -rf "$STAGING_DIR"' EXIT

echo "==> Type-checking and building the frontend (smoke test)..."
(cd web && npm run build)
rm -rf web/dist

echo "==> Staging files..."
DEST="$STAGING_DIR/$NAME"
mkdir -p "$DEST"

rsync -a \
  --exclude 'node_modules' \
  --exclude 'dist' \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '*.db' \
  --exclude '.git' \
  --exclude 'CLAUDE.md' \
  --exclude '*.tar.gz' \
  --exclude 'sujet.pdf' \
  ./ "$DEST/"

echo "==> Archiving to $OUT..."
rm -f "$OUT"
tar -czf "$OUT" -C "$STAGING_DIR" "$NAME"

SIZE_BYTES=$(stat -c%s "$OUT")
SIZE_HUMAN=$(du -h "$OUT" | cut -f1)
echo "==> Done: $OUT ($SIZE_HUMAN)"

LIMIT_BYTES=$((3 * 1024 * 1024))
if [ "$SIZE_BYTES" -gt "$LIMIT_BYTES" ]; then
  echo "WARNING: archive exceeds the 3MB limit from the assignment spec!" >&2
fi

echo "==> File counts (informational only - extra tooling/config files can be justified in the report):"
echo "    web/src (client):   $(find "$DEST/web/src" -type f | wc -l)"
echo "    api (server, code): $(find "$DEST/api" -type f ! -name '*.lock' | wc -l)"
