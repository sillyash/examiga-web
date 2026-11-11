#!/usr/bin/env bash
set -euo pipefail

# Converts the markdown report into the rapport.pdf required by the assignment.
# Usage: scripts/md_to_pdf.sh [input.md] [output.pdf]

cd "$(dirname "$0")/.."

INPUT="${1:-docs/RAPPORT.md}"
OUTPUT="${2:-docs/rapport.pdf}"

if [ ! -f "$INPUT" ]; then
  echo "error: $INPUT not found" >&2
  exit 1
fi

TYP=".rapport.tmp.typ"
trap 'rm -f "$TYP"' EXIT

# Style overrides
STYLE='#set par(justify: false)
#show figure.where(kind: table): set block(breakable: true)
#show figure.where(kind: table): set align(left)
#show table: set align(left)
#show quote.where(block: true): it => block(
  width: 100%,
  fill: rgb("#fdf3f3"),
  stroke: (left: 3pt + rgb("#c81e1e")),
  inset: (x: 12pt, y: 9pt),
  radius: (right: 3pt),
  text(style: "italic", it.body),
)'

# --columns=1000 -> pandoc stops guessing column width
pandoc "$INPUT" \
  --standalone \
  --to typst \
  --columns=1000 \
  -V margin.x=1.5cm \
  -V margin.y=1.5cm \
  -V fontsize=10pt \
  -V lang=fr \
  -V papersize=a4 \
  -V mainfont="Lato" \
  -V codefont="Source Code Pro" \
  -B <(printf '%s\n' "$STYLE") \
  -o "$TYP"

# Tables: every column fits its content except the last
sed -i -E 's/^( +)columns: ([0-9]+),$/\1columns: (auto,) * (\2 - 1) + (1fr,),/' "$TYP"

typst compile --root . "$TYP" "$OUTPUT"

echo "wrote $OUTPUT"
