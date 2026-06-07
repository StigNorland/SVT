#!/usr/bin/env bash
set -euo pipefail

# Prepared high-resolution #108 scaling run.
#
# Default strategy: many independent trajectories, one FFT thread each.
# This usually uses CPU better than threaded FFTs inside one trajectory.
#
# Tunables:
#   WORKERS=6          process workers for independent trajectories
#   FFT_WORKERS=1      scipy.fft workers inside each trajectory
#   SNAPSHOTS=65       saved frames per trace
#   DURATION=0.10      physical trace duration
#
# Example:
#   WORKERS=8 ./instruments/paper_ii/run_tube_pinch_scaling_48_64.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

WORKERS="${WORKERS:-6}"
FFT_WORKERS="${FFT_WORKERS:-1}"
SNAPSHOTS="${SNAPSHOTS:-65}"
DURATION="${DURATION:-0.10}"

python instruments/paper_ii/tube_pinch_cap_harness.py \
  --scaling \
  --workers "$WORKERS" \
  --fft-workers "$FFT_WORKERS" \
  --scaling-duration "$DURATION" \
  --scaling-snapshots "$SNAPSHOTS" \
  --scaling-n 48 \
  --scaling-n 64 \
  --scaling-lambda 0.5 \
  --scaling-lambda 1.0 \
  --scaling-lambda 1.4 \
  --scaling-lambda 2.0 \
  --scaling-lambda 2.8 \
  --scaling-lambda 4.0 \
  --scaling-json-output papers/SSV-II/data/tube-pinch-cap-scaling-48-64-issue108.json \
  --scaling-note-output papers/SSV-II/results/reconnection/tube-pinch-cap-scaling-48-64-issue108.md
