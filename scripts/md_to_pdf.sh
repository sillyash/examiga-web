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

pandoc "$INPUT" \
  -o "$OUTPUT" \
  --pdf-engine=pdflatex \
  -V geometry:margin=2cm \
  -V fontsize=11pt

echo "wrote $OUTPUT"
