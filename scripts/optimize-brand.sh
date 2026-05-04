#!/usr/bin/env bash
set -euo pipefail

# Optimize the repository's brand.webp.
#
# Requirements:
#   - ImageMagick (magick)
#   - libwebp tools (dwebp, cwebp)
#
# Usage:
#   ./scripts/optimize-brand.sh [--max-width 512] [--quality 80]

MAX_WIDTH=512
QUALITY=80

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-width)
      MAX_WIDTH="$2"
      shift 2
      ;;
    --quality)
      QUALITY="$2"
      shift 2
      ;;
    -h|--help)
      sed -n '1,120p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IN_FILE="$ROOT_DIR/brand.webp"

if [[ ! -f "$IN_FILE" ]]; then
  echo "ERROR: $IN_FILE not found" >&2
  exit 1
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

PNG_IN="$TMP_DIR/brand.png"
PNG_RESIZED="$TMP_DIR/brand.resized.png"
WEBP_OUT="$TMP_DIR/brand.optimized.webp"

# Decode WebP -> PNG for resizing
if ! command -v dwebp >/dev/null 2>&1; then
  echo "ERROR: dwebp not found (install libwebp tools)" >&2
  exit 1
fi
if ! command -v cwebp >/dev/null 2>&1; then
  echo "ERROR: cwebp not found (install libwebp tools)" >&2
  exit 1
fi
if ! command -v magick >/dev/null 2>&1; then
  echo "ERROR: magick not found (install ImageMagick)" >&2
  exit 1
fi

dwebp "$IN_FILE" -o "$PNG_IN" >/dev/null

# Resize *down* only (never upscale)
magick "$PNG_IN" -resize "${MAX_WIDTH}x${MAX_WIDTH}>" "$PNG_RESIZED"

# Re-encode as WebP
# -q: quality
# -m 6: best compression method (slowest)
# -alpha_q 100: preserve alpha quality
# -metadata none: strip metadata
cwebp -q "$QUALITY" -m 6 -alpha_q 100 -metadata none "$PNG_RESIZED" -o "$WEBP_OUT" >/dev/null

# Replace the original file atomically
cp "$WEBP_OUT" "$IN_FILE"

echo "Optimized $IN_FILE" 

echo "Settings:" 
echo "  max width: $MAX_WIDTH" 
echo "  quality:   $QUALITY"

echo "Sizes:" 
# Use platform-specific stat format
if stat -c %s "$IN_FILE" >/dev/null 2>&1; then
  SIZE_BYTES=$(stat -c %s "$IN_FILE")
else
  SIZE_BYTES=$(stat -f %z "$IN_FILE")
fi

echo "  output:    ${SIZE_BYTES} bytes"
