import os
import time
import csv
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean, quantiles

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
PROMPT = os.getenv("PROMPT", "Explain Docker in 2 sentences.")
MODEL = os.getenv("MODEL", "qwen3.5:9b")
N_REQUESTS = int(os.getenv("N_REQUESTS", "20"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "2"))
MAX_TOKENS = os.getenv("MAX_TOKENS", None)
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "results")


def send_request():
    start = time.time()
    try:
        payload = {"prompt": PROMPT, "model": MODEL}
        if MAX_TOKENS is not None:
            payload["max_tokens"] = int(MAX_TOKENS)
        resp = requests.post(
            f"{BASE_URL}/generate",
            json=payload,
            timeout=180,
        )
        resp.raise_for_status()
        latency = time.time() - start
        data = resp.json()
        return {
            "success": True,
            "latency_sec": latency,
            "tokens": data.get("tokens", 0),
            "tokens_per_sec": data.get("tokens_per_sec", 0.0),
        }
    except Exception as e:
        latency = time.time() - start
        return {
            "success": False,
            "latency_sec": latency,
            "tokens": 0,
            "tokens_per_sec": 0.0,
            "error": str(e),
        }


def main():
    print(f"Starting benchmark: {N_REQUESTS} requests, concurrency={MAX_WORKERS}, model='{MODEL}'")
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(send_request) for _ in range(N_REQUESTS)]
        for f in as_completed(futures):
            results.append(f.result())

    successful_results = [r for r in results if r.get("success", True)]
    latencies = [r["latency_sec"] for r in successful_results]
    tps_list = [r["tokens_per_sec"] for r in successful_results]

    if latencies:
        avg_latency = mean(latencies)
        avg_tps = mean(tps_list)
        if len(latencies) >= 2:
            p = quantiles(latencies, n=100)
            p50 = p[49]
            p90 = p[89]
            p99 = p[98] if len(p) > 98 else p90
        else:
            p50 = p90 = p99 = avg_latency
    else:
        avg_latency = p50 = p90 = p99 = avg_tps = 0.0

    summary = {
        "model": MODEL,
        "prompt": PROMPT,
        "n_requests": N_REQUESTS,
        "successful_requests": len(successful_results),
        "failed_requests": len(results) - len(successful_results),
        "max_workers": MAX_WORKERS,
        "avg_latency_sec": round(avg_latency, 4),
        "p50_latency_sec": round(p50, 4),
        "p90_latency_sec": round(p90, 4),
        "p99_latency_sec": round(p99, 4),
        "avg_tokens_per_sec": round(avg_tps, 2),
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # CSV export
    output_file = os.path.join(OUTPUT_DIR, "benchmark_results.csv")
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["latency_sec", "tokens", "tokens_per_sec"])
        writer.writeheader()
        for r in results:
            writer.writerow({
                "latency_sec": round(r["latency_sec"], 4),
                "tokens": r["tokens"],
                "tokens_per_sec": round(r["tokens_per_sec"], 2),
            })

    # JSON summary export
    summary_file = os.path.join(OUTPUT_DIR, "benchmark_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n--- Benchmark Summary ---")
    print(f"Total Requests:      {N_REQUESTS} (Success: {len(successful_results)}, Failed: {len(results) - len(successful_results)})")
    print(f"Avg latency (sec):   {avg_latency:.4f}")
    print(f"p50 latency (sec):   {p50:.4f}")
    print(f"p90 latency (sec):   {p90:.4f}")
    print(f"p99 latency (sec):   {p99:.4f}")
    print(f"Avg tokens/sec:      {avg_tps:.2f}")
    print(f"\nResults saved to '{output_file}' and '{summary_file}'")


if __name__ == "__main__":
    main()
