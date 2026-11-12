#!/usr/bin/env bash
set -e

# Antigravity MapLibre GIS Learning Studio Start Script
# Runs Python FastAPI (8000), Rust Axum (8080), and React Frontend (5173)

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "🗺️  MapLibre GIS Studio & Dual-Backend API Hub"
echo "=========================================================="
echo "• Frontend (React TS + Geoman): http://localhost:5173"
echo "• Backend 1: Rust (LTAX Khon Kaen) : http://localhost:8080"
echo "• Backend 2: Python (DPT Satun)    : http://localhost:8000"
echo "=========================================================="

# Trap SIGINT/SIGTERM to kill all background subprocesses cleanly
cleanup() {
    echo ""
    echo "🛑 Shutting down all servers..."
    kill 0
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 1. Start Python FastAPI
echo "🐍 Starting Python FastAPI (Port 8000)..."
(
    cd backend-python
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        venv/bin/pip install -r requirements.txt
    fi
    venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
) &
PY_PID=$!

# 2. Start Rust Axum
echo "🦀 Starting Rust Axum (Port 8080)..."
(
    cd backend-rust
    export PATH=$PATH:~/.cargo/bin
    cargo run --release
) &
RUST_PID=$!

# 3. Start Frontend Vite
echo "⚛️  Starting Frontend Vite (Port 5173)..."
(
    source ~/.nvm/nvm.sh 2>/dev/null || true
    nvm use 22 2>/dev/null || nvm use 20 2>/dev/null || true
    cd frontend
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    npm run dev
) &
FRONTEND_PID=$!

# Wait for background processes
wait

