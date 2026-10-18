#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python3 -m venv .venv
.venv/bin/python -m pip install --no-cache-dir --disable-pip-version-check 'setuptools==80.9.0'
.venv/bin/python -m pip install --no-cache-dir --disable-pip-version-check --no-build-isolation --no-deps -e .
.venv/bin/python scripts/fetch_primary_sources.py
.venv/bin/python -m unittest discover -s tests -v
