#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "== RAJA AI VIDEO ENHANCER: Termux installer =="
pkg update -y
pkg install -y python ffmpeg
mkdir -p "$PROJECT_DIR/data/logs" "$PROJECT_DIR/data/reports" "$PROJECT_DIR/output"
chmod +x "$PROJECT_DIR/run.sh" "$PROJECT_DIR/termux-install.sh"
python -m py_compile "$PROJECT_DIR/raja_enhancer.py" "$PROJECT_DIR"/raja_enhancer/*.py
echo
echo "Installation checks passed."
echo "Run: bash \"$PROJECT_DIR/run.sh\""
echo "Optional: run 'termux-setup-storage' to access shared phone storage."
