#!/usr/bin/env bash
# POSIX setup script — create venv and install requirements
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
