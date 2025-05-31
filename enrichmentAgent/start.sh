#!/bin/bash

echo "[start.sh] RUN_MODE: ${RUN_MODE:-prod}"

if [ "$RUN_MODE" = "test" ]; then
  echo "[start.sh] Running test_vector_push.py..."
  python3 -m src.services.test_vector_push
else
  echo "[start.sh] Running enrichment agent (main.py)..."
  python3 -m src.main
fi
