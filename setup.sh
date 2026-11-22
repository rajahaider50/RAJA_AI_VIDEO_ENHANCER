#!/usr/bin/env bash
set -euo pipefail
python3 -m py_compile raja_enhancer.py raja_enhancer/*.py
python3 -m unittest discover -s tests -v
echo "Setup checks passed. Run: python3 raja_enhancer.py"
