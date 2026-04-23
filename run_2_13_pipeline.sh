#!/bin/bash
# Run estimation pipeline for textfile (16).txt + Polycam 2_13_2026, then cleanup and verify.
# Usage: export OPENAI_API_KEY=your_key; bash run_2_13_pipeline.sh

set -e
cd "$(dirname "$0")"

TRANSCRIPT="/Users/bhakt/Downloads/textfile (16).txt"
POLYCAM="/Users/bhakt/Downloads/[Polycam Spatial Report] 2_13_2026.pdf"

if [ -z "$OPENAI_API_KEY" ]; then
  echo "ERROR: Set OPENAI_API_KEY first: export OPENAI_API_KEY=your_key"
  exit 1
fi

echo "[1/3] Running estimation pipeline..."
python3 run_chunked_estimation.py \
  --transcript "$TRANSCRIPT" \
  --polycam "$POLYCAM" \
  --master_pricing "master_pricing_data.csv" \
  --prompt_file "estimation_prompt.txt" \
  --api_key "$OPENAI_API_KEY"

echo "[2/3] Running comprehensive cleanup (latest run)..."
python3 comprehensive_cleanup.py

echo "[3/3] Running verification..."
python3 verify_estimate_against_transcript.py

echo "Done. Check chunked_outputs/ for the latest run and comprehensive_clean_estimate_final.xlsx"
