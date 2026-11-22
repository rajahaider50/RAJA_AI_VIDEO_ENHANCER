#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v python >/dev/null 2>&1; then
  echo "Python is missing. Run: bash termux-install.sh"
  exit 1
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "FFmpeg is missing. Run: bash termux-install.sh"
  exit 1
fi
exec python raja_enhancer.py
