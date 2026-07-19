#!/usr/bin/env bash
# Convenience wrapper: loads .env (OLLAMA_API_KEY + VENV_ACTIVATE), activates the
# venv named there, and runs the experiment + analysis pipeline.
#
# Usage:
#   ./run.sh              # full pipeline (experiments + analyze)
#   ./run.sh dry          # build prompts only, no model calls
#   ./run.sh analyze      # analyze existing data/raw_runs.jsonl
#   ./run.sh experiments  # run experiments only (no analyze)
set -euo pipefail
cd "$(dirname "$0")"

if [ -f .env ]; then
  set -a; . ./.env; set +a
fi

if [ -z "${OLLAMA_API_KEY:-}" ]; then
  echo "ERROR: OLLAMA_API_KEY not set (check .env)" >&2; exit 1
fi

if [ -z "${VENV_ACTIVATE:-}" ] || [ ! -f "$VENV_ACTIVATE" ]; then
  echo "ERROR: VENV_ACTIVATE not set or missing (check .env)" >&2; exit 1
fi
. "$VENV_ACTIVATE"

mode="${1:-all}"

case "$mode" in
  dry)
    python -m runner.run_experiments --dry-run
    ;;
  experiments)
    python -m runner.run_experiments
    ;;
  analyze)
    python -m analyze.analyze
    ;;
  all)
    python -m runner.run_experiments
    python -m analyze.analyze
    ;;
  *)
    echo "Unknown mode: $mode (use: all|dry|experiments|analyze)" >&2; exit 2
    ;;
esac