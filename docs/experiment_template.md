# Experiment: <Title>

**Date:** YYYY-MM-DD  
**Goal:** <What are you measuring or validating?>

## Setup
- **OS:** <e.g. Ubuntu 22.04 via WSL2 / Windows 11>
- **GPU:** <e.g. NVIDIA RTX 4060 8 GB>
- **Docker images:** `llm-mini-app` (local build)
- **Model:** <e.g. qwen3.5:9b>
- **Ollama:** <version / source>
- **Context length:** <default or custom>

## Commands
- Start service:
  ```bash
  docker compose up --build
  ```
- Smoke test:
  ```bash
  ./scripts/smoke_test.sh
  ```
- Benchmark & Monitor GPU:
  ```bash
  # In terminal 1
  nvidia-smi -l 1

  # In terminal 2
  ./scripts/run_bench.sh
  ```
- Stop service:
  ```bash
  docker compose down
  ```

## Results
- **Avg latency (sec):** X.X
- **p50 / p90 / p99 latency:** X.X / X.X / X.X
- **Tokens/sec (avg):** Y.Y
- **GPU memory used (GB, peak):** Z.Z
- **Errors:** <none / describe>

## Observations
- How performance compares to expectations.
- GPU utilization pattern.
- Any bottlenecks (GPU memory, CPU, etc.).

## Next Steps
- What to change next time (concurrency, model, context, etc.).
