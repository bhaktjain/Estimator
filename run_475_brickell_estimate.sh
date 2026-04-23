#!/bin/bash
# Run estimation pipeline for 475 Brickell transcript + Polycam.
# Usage: export OPENAI_API_KEY=your_key; bash run_475_brickell_estimate.sh
#    or: OPENAI_API_KEY=your_key bash run_475_brickell_estimate.sh

set -e
cd "$(dirname "$0")"

TRANSCRIPT="/Users/bhakt/Downloads/Chapter_ Walk-Through at  475 Brickell _ Transcript.txt"
POLYCAM="/Users/bhakt/Downloads/[Polycam Spatial Report] 2_25_2026 (1).pdf"
MASTER_PRICING="Master Pricing Sheet - Q1 - 2025 (2).pdf"
if [ ! -f "$MASTER_PRICING" ]; then
  MASTER_PRICING="/Users/bhakt/Documents/Master Pricing Sheet - Q1 - 2025 (2).pdf"
fi

if [ -z "$OPENAI_API_KEY" ]; then
  echo "ERROR: Set OPENAI_API_KEY first."
  echo "  export OPENAI_API_KEY=sk-your-key"
  echo "  bash run_475_brickell_estimate.sh"
  exit 1
fi

echo "[1/3] Running estimation pipeline (transcript + Polycam)..."
python3 run_chunked_estimation.py \
  --transcript "$TRANSCRIPT" \
  --polycam "$POLYCAM" \
  --master_pricing "$MASTER_PRICING" \
  --prompt_file estimation_prompt.txt

echo "[2/3] Running comprehensive cleanup (latest run)..."
python3 comprehensive_cleanup.py

echo "[3/3] Done. Check chunked_outputs/ for the latest run and comprehensive_clean_estimate_final.xlsx"
