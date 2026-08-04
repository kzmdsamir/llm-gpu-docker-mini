# Experiment: Ollama + Qwen3.5 9B with GPU in Docker

**Date:** 2026-08-04  
**Goal:** Measure latency and throughput of `qwen3.5:9b` served via FastAPI + Ollama containerized setup on NVIDIA RTX 4060 8 GB at concurrency=2.

## Setup
- **OS:** Windows 11 + WSL2 (Ubuntu)
- **GPU:** NVIDIA RTX 4060 8 GB VRAM
- **Docker images:**
  - `llm-mini-app` (local build)
- **Model:** `qwen3.5:9b`
- **Ollama:** Host Ollama via `host.docker.internal:11434`
- **Prompt:** `"Explain Docker in 2 sentences."`
- **Concurrency (MAX_WORKERS):** 2
- **Total Requests:** 20

## Commands
- Start service:
  ```bash
  docker compose up --build -d
  ```
- Smoke test:
  ```bash
  ./scripts/smoke_test.sh
  ```
- Benchmark & Monitor GPU:
  ```bash
  # Monitor GPU:
  nvidia-smi -l 1

  # Run benchmark:
  python scripts/benchmark.py
  ```
- Concurrency Sweep:
  ```bash
  ./scripts/bench_sweep.sh
  ```

## Measured Results
- **Total Requests:** 20 (Success: 20, Failed: 0 - 100% Success Rate)
- **Avg latency (sec):** 86.46s
- **p50 latency (sec):** 87.36s
- **p90 latency (sec):** 107.64s
- **p99 latency (sec):** 139.81s
- **Avg tokens/sec:** 13.20 t/s
- **Typical output tokens:** ~1,000–1,500 tokens per request (long completions)
- **Errors:** 0

## Engineering Observations
- **Stability under load:** Zero failed requests or timeouts at `MAX_WORKERS=2`.
- **Latency characteristics:** High overall request latency (~86s) is driven by output generation length (~1000+ tokens) rather than model load failure.
- **Tail Latency:** p90 (107.6s) and p99 (139.8s) exhibit expected tail latency increases due to VRAM resource contention and single-GPU batching behavior under concurrent requests.

## Next Steps
- Execute full concurrency sweep (`1`, `2`, `4` workers) via `./scripts/bench_sweep.sh`.
- Test token output bounds (`max_tokens` / `num_predict: 256`) to isolate generation speed from completion length.
