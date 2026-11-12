#!/usr/bin/env bash
set -e

# Start the Rust Axum backend on port 8080.
# Must run from this folder: the data paths in storage_service.rs are relative.
cd "$(dirname "${BASH_SOURCE[0]}")"
export PATH="$PATH:$HOME/.cargo/bin"

exec cargo run
