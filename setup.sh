#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -r requirements.txt
echo "Virtual environment created and dependencies installed. Activate with: source .venv/bin/activate"