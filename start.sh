#!/usr/bin/env bash
set -euo pipefail

OUTPUT_CSV="./data/output-data.csv"

# Load .env
set -a
source ".env"
set +a

# Activate venv and run program (blocks until finished; non-zero exit aborts script)
source ".venv/bin/activate"
python "main.py"

[[ -f "$OUTPUT_CSV" ]] || { echo "Output CSV not found: $OUTPUT_CSV" >&2; exit 1; }

export OUTPUT_CSV
python "export.py"