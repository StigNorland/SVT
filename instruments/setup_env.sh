#!/usr/bin/env bash
# Set up the SSV Python environment on Linux/macOS.
#   Usage:  bash instruments/setup_env.sh
# Creates a virtual environment at <repo>/.venv and installs the dependencies.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PY="${PYTHON:-python3}"
echo "Using interpreter: $("$PY" --version 2>&1) ($PY)"

"$PY" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r instruments/requirements.txt

echo
echo "Done. To use this environment:"
echo "    source .venv/bin/activate"
echo "    pytest instruments/test          # run the test suite"
echo "    python instruments/paper_i/trefoil_ny_derivation.py   # run a script"
