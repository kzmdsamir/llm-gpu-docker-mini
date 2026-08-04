#!/usr/bin/env bash
set -euo pipefail

export BASE_URL="${BASE_URL:-http://localhost:8000}"
export MODEL="${MODEL:-qwen3.5:9b}"
export N_REQUESTS="${N_REQUESTS:-20}"
export MAX_WORKERS="${MAX_WORKERS:-2}"

python scripts/benchmark.py
