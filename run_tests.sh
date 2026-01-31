#!/usr/bin/env bash
echo "Running pytest"
source .venv/bin/activate
python -m pytest -q test_files
