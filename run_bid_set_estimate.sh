#!/bin/bash
# Run estimate from Revised Bid Set + scope transcript.
# Usage: export OPENAI_API_KEY=your_key; bash run_bid_set_estimate.sh

set -e
cd "$(dirname "$0")"

TRANSCRIPT="estimate_from_bid_set_scope.txt"
BID_SET="/Users/bhakt/Downloads/2026.02.25-REVISED BID SET.pdf"
MASTER_PRICING="Master Pricing Sheet - Q1 - 2025 (2).pdf"

if [ ! -f "$BID_SET" ]; then
  echo "ERROR: Bid set not found at $BID_SET"
  exit 1
fi
if [ -z "$OPENAI_API_KEY" ]; then
  echo "ERROR: Set OPENAI_API_KEY first."
  echo "  export OPENAI_API_KEY=sk-your-key"
  exit 1
fi

echo "[1/3] Running estimation pipeline (scope transcript + Revised Bid Set)..."
python3 run_chunked_estimation.py \
  --transcript "$TRANSCRIPT" \
  --polycam "$BID_SET" \
  --master_pricing "$MASTER_PRICING" \
  --prompt_file estimation_prompt.txt

echo "[2/3] Running comprehensive cleanup (latest run)..."
python3 comprehensive_cleanup.py

echo "[3/3] Done. Check chunked_outputs/ for latest run and comprehensive_clean_estimate_final.xlsx"
