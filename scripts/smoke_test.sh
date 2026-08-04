#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "Waiting for service to be healthy..."

for i in {1..30}; do
  if curl -sf "$BASE_URL/health" > /dev/null; then
    echo "Health OK"
    break
  fi
  sleep 1
done

echo "Testing /ready..."
READY_RESP=$(curl -sf "$BASE_URL/ready")
if [ -z "$READY_RESP" ]; then
  echo "/ready returned empty response"
  exit 1
fi
echo "$READY_RESP" | python -m json.tool || {
  echo "/ready response is not valid JSON:"
  echo "$READY_RESP"
  exit 1
}

echo "Testing /generate..."
GEN_RESP=$(curl -sf -X POST "$BASE_URL/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello, world!","model":"qwen3.5:9b"}')
if [ -z "$GEN_RESP" ]; then
  echo "/generate returned empty response"
  exit 1
fi
echo "$GEN_RESP" | python -m json.tool || {
  echo "/generate response is not valid JSON:"
  echo "$GEN_RESP"
  exit 1
}

echo "Smoke test passed."
