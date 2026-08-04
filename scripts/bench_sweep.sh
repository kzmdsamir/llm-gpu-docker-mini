#!/usr/bin/env bash
set -euo pipefail

export BASE_URL="${BASE_URL:-http://localhost:8000}"
export MODEL="${MODEL:-qwen3.5:9b}"
export N_REQUESTS="${N_REQUESTS:-20}"
export PROMPT="${PROMPT:-Explain Docker in 2 sentences.}"

for workers in 1 2 4; do
  echo "=========================================="
  echo " Running Concurrency Sweep: MAX_WORKERS=$workers"
  echo "=========================================="
  export MAX_WORKERS=$workers
  python scripts/benchmark.py
  if [ -f results/benchmark_summary.json ]; then
    cp results/benchmark_summary.json "results/benchmark_summary_workers_${workers}.json"
    echo "Saved summary to results/benchmark_summary_workers_${workers}.json"
  fi
  echo ""
done
