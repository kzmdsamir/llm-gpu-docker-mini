# llm-gpu-docker-mini

A containerized FastAPI service that calls local Ollama models (e.g., `qwen3.5:9b`) with GPU acceleration, complete with benchmarking, structured logging, GPU monitoring instructions, and experimentation templates.

This project is designed as prep for an AI infrastructure internship focused on:
- Containerized AI deployments
- Inference engines and model serving
- GPU monitoring and benchmarking
- Engineering documentation and experimentation

---

## Repository Structure

```text
llm-gpu-docker-mini/
├── README.md
├── LICENSE
├── .gitignore
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── logging_config.py
├── docker-compose.yml
├── Dockerfile
├── scripts/
│   ├── benchmark.py
│   ├── run_bench.sh
│   ├── bench_sweep.sh
│   └── smoke_test.sh
├── docs/
│   ├── experiment_template.md
│   └── experiment_01_qwen3_5_9b_gpu.md
├── logs/
│   └── .gitkeep
└── results/
    └── .gitkeep
```

---

## Requirements

- **OS**: Windows 11 + WSL2 (Ubuntu) + Docker Desktop with WSL2 integration
- **GPU**: NVIDIA GPU with drivers + `nvidia-smi` working in WSL2
- **Ollama**: Installed and running locally (or in Docker)
- **Model**: `qwen3.5:9b` pulled (`ollama pull qwen3.5:9b`)

---

## Quick Start

### 1. Verify Ollama & Model

Check if Ollama is running and the model is pulled:

```bash
ollama list
# Should show: qwen3.5:9b
```

Test manually:

```bash
ollama run qwen3.5:9b "Explain Docker in 2 sentences."
```

### 2. Build and Run with Docker Compose

From the project root:

```bash
docker compose up --build -d
```

This starts the `llm-mini-app` container (FastAPI service).

> **Note on Host Ollama vs Dockerized Ollama:**  
> By default, `docker-compose.yml` connects to Ollama running on your host machine via `http://host.docker.internal:11434/api/generate`. If you prefer to run Ollama inside Docker, uncomment the `ollama` service block in `docker-compose.yml` and update `OLLAMA_URL` to `http://ollama:11434/api/generate`.

### 3. Test Endpoints

```bash
# Health check (Liveness)
curl http://localhost:8000/health

# Readiness check (Ollama reachability)
curl http://localhost:8000/ready

# Text Generation (with optional max_tokens limit)
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain Docker in 2 sentences.","model":"qwen3.5:9b","max_tokens":256}'
```

Alternatively, run the automated smoke test script:

```bash
./scripts/smoke_test.sh
```

### 4. Run Benchmarks & Concurrency Sweeps

Run standard benchmark test (`MAX_WORKERS=2` default):

```bash
python scripts/benchmark.py
```

or using the shell wrapper:

```bash
./scripts/run_bench.sh
```

Run a full concurrency sweep across multiple worker counts (`1`, `2`, `4`):

```bash
./scripts/bench_sweep.sh
```

Results are saved to:
- `results/benchmark_results.csv` (Per-request raw data)
- `results/benchmark_summary.json` (Aggregated latency & throughput stats)
- `results/benchmark_summary_workers_<N>.json` (Concurrency sweep summaries)

---

## Configuration (Environment Variables)

### FastAPI App Config
- `OLLAMA_URL`: Ollama generate endpoint (default: `http://host.docker.internal:11434/api/generate`)
- `DEFAULT_MODEL`: Default LLM model name (default: `qwen3.5:9b`)
- `REQUEST_TIMEOUT`: Timeout in seconds for Ollama HTTP calls (default: `180`)
- `LOG_LEVEL`: Logging verbosity level (default: `INFO`)

### Benchmark Script Config
- `BASE_URL`: FastAPI service base URL (default: `http://localhost:8000`)
- `PROMPT`: Prompt text for benchmark requests (default: `"Explain Docker in 2 sentences."`)
- `MODEL`: Model name to benchmark (default: `qwen3.5:9b`)
- `N_REQUESTS`: Total number of requests to execute (default: `20`)
- `MAX_WORKERS`: Concurrency level / thread pool size (default: `2`)
- `MAX_TOKENS`: Optional maximum output tokens to limit generation length
- `OUTPUT_DIR`: Directory to write benchmark artifacts (default: `results`)

---

## Monitoring GPU Usage

While running benchmarks or inference, monitor VRAM and GPU utilization in real time:

```bash
nvidia-smi -l 1
```

Watch VRAM allocation, GPU core utilization, and temperature during concurrent model calls.

---

## Documentation & Experiments

See the `docs/` directory for experiment logs and templates:
- `docs/experiment_template.md`: Template for recording benchmark parameters and hardware metrics.
- `docs/experiment_01_qwen3_5_9b_gpu.md`: Recorded experiment run notes and 20/20 success metrics for `qwen3.5:9b` on RTX 4060 8GB.

---

## License

[MIT](LICENSE)
