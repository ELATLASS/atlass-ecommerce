#!/bin/bash
# Cron script: Run trend research pipeline
# Schedule: every 6 hours (0 */6 * * *)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "[$(date -u)] Running trend research pipeline..."

python trend_research.py

echo "[$(date -u)] Pipeline complete."
