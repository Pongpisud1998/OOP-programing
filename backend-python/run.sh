#!/usr/bin/env bash
set -e

# Start the Python FastAPI backend on port 8000.
cd "$(dirname "${BASH_SOURCE[0]}")"

if [ ! -d venv ]; then
    python3 -m venv venv
fi
venv/bin/pip install --quiet -r requirements.txt

exec venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
