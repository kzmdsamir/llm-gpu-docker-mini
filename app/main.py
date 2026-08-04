import os
import time
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

try:
    from app.logging_config import setup_logging
except ImportError:
    from logging_config import setup_logging

app = FastAPI(
    title="LLM GPU Docker Mini Service",
    description="Containerized FastAPI AI inference service interfacing with Ollama",
    version="1.0.0",
)

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logger = setup_logging(LOG_LEVEL)

# Configuration from Environment Variables
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen3.5:9b")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "180"))


class PromptRequest(BaseModel):
    prompt: str
    model: str = DEFAULT_MODEL
    max_tokens: int | None = None


class PromptResponse(BaseModel):
    text: str
    latency_sec: float
    tokens: int
    tokens_per_sec: float
    request_id: str


@app.get("/health")
def health():
    """Liveness probe: verifies the FastAPI application is running."""
    return {"status": "ok"}


@app.get("/ready")
def ready():
    """Readiness probe: verifies the upstream Ollama service is reachable."""
    # OLLAMA_URL is like: http://host.docker.internal:11434/api/generate
    base = OLLAMA_URL.replace("/api/generate", "")
    # base should be: http://host.docker.internal:11434
    tags_url = f"{base}/api/tags"
    try:
        resp = requests.get(tags_url, timeout=5)
        resp.raise_for_status()
        return {"status": "ok", "ollama": "reachable"}
    except Exception as e:
        logger.error("Ollama not reachable", extra={"extra_data": {"error": str(e)}})
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/generate", response_model=PromptResponse)
def generate(req: PromptRequest):
    """Text generation endpoint: relays prompts to Ollama with GPU acceleration."""
    request_id = str(uuid.uuid4())
    log_extra = {
        "request_id": request_id,
        "extra_data": {
            "model": req.model,
            "prompt_len": len(req.prompt),
        },
    }
    logger.info("generate_start", extra=log_extra)

    payload = {
        "model": req.model,
        "prompt": req.prompt,
        "stream": False,
    }
    if req.max_tokens is not None:
        payload["options"] = {"num_predict": req.max_tokens}
    start = time.time()
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.error("ollama_call_failed", extra={
            "request_id": request_id,
            "extra_data": {"error": str(e), "model": req.model}
        })
        raise HTTPException(status_code=500, detail=f"Ollama call failed: {str(e)}")

    latency = time.time() - start
    text = data.get("response", "")
    tokens = data.get("eval_count", 0)
    tps = tokens / latency if latency > 0 else 0.0

    log_extra["extra_data"].update({
        "latency_sec": round(latency, 4),
        "tokens": tokens,
        "tokens_per_sec": round(tps, 2),
    })
    logger.info("generate_done", extra=log_extra)

    return PromptResponse(
        text=text,
        latency_sec=round(latency, 4),
        tokens=tokens,
        tokens_per_sec=round(tps, 2),
        request_id=request_id,
    )
