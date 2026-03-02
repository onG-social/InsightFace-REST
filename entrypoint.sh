#!/bin/bash
set -e

# Set safe defaults if Railway variables not defined
LOG_LEVEL=${LOG_LEVEL:-info}
NUM_WORKERS=${NUM_WORKERS:-2}
PORT=${PORT:-8080}

echo "Starting InsightFace-REST using $NUM_WORKERS workers on port $PORT."

exec gunicorn \
  --log-level ${LOG_LEVEL:-info} \
  -w ${NUM_WORKERS:-2} \
  -k uvicorn.workers.UvicornWorker \
  --keep-alive 60 \
  --timeout 60 \
  if_rest.api.main:app \
  -b 0.0.0.0:${PORT}
